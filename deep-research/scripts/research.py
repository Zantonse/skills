#!/usr/bin/env python3
"""Deep research via Claude Sonnet through LiteLLM proxy (OCM auth).

Sends a research query (with optional context) to Claude with extended thinking
for deep analysis and synthesis. Outputs structured markdown.

Usage:
    # Simple query
    python3 research.py --query "What is NetApp's competitive positioning vs Pure Storage?"

    # With context files
    python3 research.py --query "Analyze this company's tech stack" --context notes.md website.txt

    # With stdin context (pipe from other tools)
    echo "company data here" | python3 research.py --query "Summarize key findings" --stdin

    # Custom system prompt
    python3 research.py --query "Build an account overview" --system "You are an SE researching a prospect"

    # Save to file
    python3 research.py --query "Deep dive on Kubernetes adoption" --output research.md

Auth:
    Uses OCM auth via /usr/local/bin/ocm. Requires ocm to be installed and authenticated.
"""

import argparse
import json
import os
import subprocess
import sys
from typing import Optional

OCM_BINARY = "/usr/local/bin/ocm"
LITELLM_BASE_URL = "https://llm.atko.ai"
LITELLM_HOST = "llm.atko.ai"


def _get_ocm_token() -> str:
    """Get a LiteLLM auth token via OCM."""
    try:
        result = subprocess.run(
            [OCM_BINARY, "auth", "litellm", "-s", LITELLM_HOST],
            capture_output=True,
            text=True,
            check=True,
        )
        token = result.stdout.strip()
        if not token:
            print(
                "Error: ocm auth returned an empty token. Try running:\n"
                f"  {OCM_BINARY} auth login",
                file=sys.stderr,
            )
            sys.exit(1)
        return token
    except FileNotFoundError:
        print(
            f"Error: ocm binary not found at {OCM_BINARY}.\n"
            "Install ocm or check your PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(
            f"Error: ocm auth failed: {e.stderr.strip()}\n"
            f"Try running: {OCM_BINARY} auth login",
            file=sys.stderr,
        )
        sys.exit(1)


def ensure_anthropic():
    """Install anthropic package if not available."""
    try:
        import anthropic  # noqa: F401
    except ImportError:
        print("Installing anthropic package...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "anthropic", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to install anthropic: {e.stderr.decode() if e.stderr else 'unknown'}", file=sys.stderr)
            sys.exit(1)


DEFAULT_MODEL = "claude-4-6-sonnet"

DEFAULT_SYSTEM = """You are a senior research analyst at a leading advisory firm, specializing in \
cybersecurity, identity management, and enterprise technology.

Produce thorough, well-structured research briefs that meet these standards:

## Structure
- Open with a 2-3 sentence executive summary of key findings
- Organize by topic with clear markdown headers
- End with a prioritized "Recommendations & Next Steps" section
- Include a "Knowledge Gaps & Limitations" section before recommendations

## Analytical Depth
- Go beyond surface descriptions — compare, contrast, and explain *why*
- Identify non-obvious patterns, second-order effects, and emerging trends
- When comparing vendors or approaches, provide a clear framework for comparison

## Factual Grounding (CRITICAL — this is the most important quality)
- Every major claim must be backed by a specific fact: a number, date, percentage, or named source
- Attribute data to sources (e.g., "according to Gartner's 2025 Magic Quadrant...", "per Forrester's Q3 2025 report...")
- Clearly distinguish established facts from your inferences — use phrases like "Based on available data..." vs "It is estimated that..."
- When statistics are cited, always include the year or quarter they refer to
- Do NOT make vague claims like "the market is growing rapidly" — instead say "the market grew 18% YoY to $X billion in 2025"
- Include specific product versions, release dates, and technical specifications where relevant

## Actionability
- Recommendations must be concrete and specific, not generic advice
- Each recommendation should reference evidence from the analysis
- Prioritize recommendations by impact and feasibility

## Gaps & Limitations
- Explicitly flag where data is incomplete, outdated, or uncertain
- Rate confidence as high/medium/low for major claims
- Suggest specific follow-up research to fill identified gaps
- Note where data may be stale (e.g., "market share figures are from 2024 and may have shifted")
- Identify perspectives or stakeholder viewpoints not covered in the analysis"""

SALES_ACCOUNT_SYSTEM = """You are a Sales Engineer researching a prospect account. Produce a comprehensive account overview.

Structure your research as:
## Executive Summary
One paragraph overview of the company and opportunity.

## Company Overview
- Founded, HQ, size, revenue, funding, public/private
- Industry, vertical, key products/services
- Recent news, earnings, announcements

## Technical Landscape
- Known tech stack, infrastructure, cloud providers
- Key platforms, tools, frameworks in use
- Technical initiatives, modernization efforts, digital transformation

## Business Challenges & Pain Points
- Industry-specific challenges
- Publicly stated priorities (earnings calls, press releases, job postings)
- Competitive pressures

## Opportunity Analysis
- Where our solution fits their needs
- Potential use cases and value drivers
- Champions and decision makers (titles/roles, not names)

## Competitive Landscape
- Existing vendors in our space
- Displacement opportunities
- Differentiation points

## Conversation Starters
- 3-5 discovery questions tailored to their situation
- Technical deep-dive topics
- Business value angles

## Sources & Confidence
- List sources used
- Flag areas where information is uncertain or outdated"""


def research(
    query: str,
    context: Optional[str] = None,
    system_prompt: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    mode: str = "general",
    max_tokens: int = 24000,
) -> str:
    """Send a research query to Claude with extended thinking via LiteLLM proxy (OCM auth)."""
    from anthropic import Anthropic

    token = _get_ocm_token()
    client = Anthropic(
        api_key=token,
        base_url=LITELLM_BASE_URL,
        default_headers={"x-litellm-api-key": f"Bearer {token}"},
    )

    # Select system prompt based on mode
    if system_prompt:
        sys_msg = system_prompt
    elif mode == "account":
        sys_msg = SALES_ACCOUNT_SYSTEM
    else:
        sys_msg = DEFAULT_SYSTEM

    # Build user message with optional context
    user_msg = query
    if context:
        user_msg = f"## Research Context\n\n{context}\n\n---\n\n## Research Query\n\n{query}"

    messages = [{"role": "user", "content": user_msg}]

    print(f"Researching with {model} (extended thinking)...", file=sys.stderr)

    try:
        # Use streaming to avoid timeout with extended thinking + large output
        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=sys_msg,
            messages=messages,
            temperature=1,  # Required for extended thinking
            thinking={
                "type": "enabled",
                "budget_tokens": 8000,
            },
        ) as stream:
            for event in stream:
                pass  # consume the stream

        response = stream.get_final_message()
    except Exception as e:
        msg = str(e).lower()
        if "429" in msg or "rate limit" in msg:
            print(f"Rate limited. Wait and retry: {e}", file=sys.stderr)
            sys.exit(1)
        elif "401" in msg or "403" in msg or "not allowed" in msg:
            print(f"Auth error. Check LITELLM_API_KEY has access to {model}: {e}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"API error: {e}", file=sys.stderr)
            sys.exit(1)

    # Extract text block (skip thinking blocks)
    result = ""
    for block in response.content:
        if block.type == "text":
            result = block.text
            break

    if not result:
        print("Warning: Empty response from model", file=sys.stderr)
        return ""

    usage = response.usage
    if usage:
        print(
            f"Tokens — input: {usage.input_tokens:,}, "
            f"output: {usage.output_tokens:,}",
            file=sys.stderr,
        )

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Deep research via Claude Sonnet with extended thinking. "
        "Uses extended thinking for deeper analysis before writing."
    )
    parser.add_argument("--query", "-q", required=True, help="Research query or question")
    parser.add_argument(
        "--context", "-c", nargs="*", default=[], help="Context files to include (paths)"
    )
    parser.add_argument("--stdin", action="store_true", help="Read additional context from stdin")
    parser.add_argument("--system", "-s", default=None, help="Custom system prompt")
    parser.add_argument(
        "--mode",
        "-m",
        choices=["general", "account"],
        default="general",
        help="Research mode: 'general' for any topic, 'account' for sales account overview",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name (default: {DEFAULT_MODEL})",
    )
    parser.add_argument("--output", "-o", default=None, help="Save output to file (markdown)")
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=16000,
        help="Max response tokens (default: 16000)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON with metadata (for programmatic use)",
    )
    args = parser.parse_args()

    ensure_anthropic()

    # Gather context from files and stdin
    context_parts = []
    for filepath in args.context:
        try:
            with open(filepath) as f:
                content = f.read()
            context_parts.append(f"### File: {os.path.basename(filepath)}\n\n{content}")
        except (FileNotFoundError, PermissionError) as e:
            print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)

    if args.stdin and not sys.stdin.isatty():
        stdin_data = sys.stdin.read()
        if stdin_data.strip():
            context_parts.append(f"### Piped Input\n\n{stdin_data}")

    context = "\n\n---\n\n".join(context_parts) if context_parts else None

    result = research(
        query=args.query,
        context=context,
        system_prompt=args.system,
        model=args.model,
        mode=args.mode,
        max_tokens=args.max_tokens,
    )

    if args.json:
        output = json.dumps(
            {"query": args.query, "model": args.model, "mode": args.mode, "result": result},
            indent=2,
        )
    else:
        output = result

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
