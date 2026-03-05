#!/usr/bin/env python3
"""Deep research via Gemini 3.1 Pro Preview through LiteLLM proxy.

Sends a research query (with optional context) to Gemini's large context window
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

Environment:
    LITELLM_API_KEY + LITELLM_BASE_URL (set in ~/.claude-litellm.env)
"""

import argparse
import json
import os
import subprocess
import sys
from typing import Optional


def _load_env_file():
    """Auto-load credentials from ~/.claude-litellm.env if env vars are missing."""
    if os.environ.get("LITELLM_API_KEY"):
        return
    env_file = os.path.expanduser("~/.claude-litellm.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export ") and "=" in line:
                    line = line[7:]
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    if value.startswith("$"):
                        ref_var = value[1:]
                        value = os.environ.get(ref_var, "")
                    if key and value:
                        os.environ[key] = value


_load_env_file()


def ensure_openai():
    """Install openai package if not available."""
    try:
        import openai  # noqa: F401
    except ImportError:
        print("Installing openai package...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "openai", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to install openai: {e.stderr.decode() if e.stderr else 'unknown'}", file=sys.stderr)
            sys.exit(1)


DEFAULT_MODEL = "gemini-3.1-pro-preview"

DEFAULT_SYSTEM = """You are a deep research analyst. Produce thorough, well-structured research.

Guidelines:
- Lead with key findings and executive summary
- Organize by topic with clear headers
- Cite specific facts, numbers, and dates when available
- Flag uncertainties and knowledge gaps explicitly
- End with actionable recommendations or next steps
- Use markdown formatting for readability"""

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
    max_tokens: int = 16000,
) -> str:
    """Send a research query to Gemini via LiteLLM and return the response."""
    from openai import OpenAI

    api_key = os.environ.get("LITELLM_API_KEY")
    base_url = os.environ.get("LITELLM_BASE_URL")

    if not api_key or not base_url:
        print(
            "Error: LITELLM_API_KEY and LITELLM_BASE_URL must be set.\n"
            "These should be configured in ~/.claude-litellm.env",
            file=sys.stderr,
        )
        sys.exit(1)

    base_url = base_url.rstrip("/")
    if not base_url.endswith("/v1"):
        base_url += "/v1"

    client = OpenAI(api_key=api_key, base_url=base_url)

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

    messages = [
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": user_msg},
    ]

    print(f"Researching with {model}...", file=sys.stderr)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.3,  # Lower temp for factual research
        )
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

    result = response.choices[0].message.content
    if not result:
        print("Warning: Empty response from model", file=sys.stderr)
        return ""

    token_usage = getattr(response, "usage", None)
    if token_usage:
        print(
            f"Tokens — prompt: {token_usage.prompt_tokens:,}, "
            f"completion: {token_usage.completion_tokens:,}, "
            f"total: {token_usage.total_tokens:,}",
            file=sys.stderr,
        )

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Deep research via Gemini 3.1 Pro Preview. "
        "Sends queries to Gemini's large context window for thorough analysis."
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

    ensure_openai()

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
