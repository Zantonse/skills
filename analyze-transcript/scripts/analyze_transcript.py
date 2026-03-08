#!/usr/bin/env python3
"""SE call transcript analysis — VTT/TXT parsing + Claude debrief synthesis.

Usage:
    python3 analyze_transcript.py /path/to/call.vtt --account "NetApp"
    python3 analyze_transcript.py /path/to/call.txt --account "Deel" --date 2026-03-05
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Environment & dependency helpers
# ---------------------------------------------------------------------------

def _load_env_file():
    """Auto-load credentials from ~/.claude-litellm.env if env vars are missing."""
    if os.environ.get("LITELLM_API_KEY"):
        return
    env_file = os.path.expanduser("~/.claude-litellm.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export ") and "=" in line:
                    line = line[7:]
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"")
                # Resolve $VAR references
                if value.startswith("$"):
                    ref_var = value[1:]
                    value = os.environ.get(ref_var, "")
                if key and value:
                    os.environ[key] = value


_load_env_file()


def _ensure_packages():
    for pkg, import_name in [("anthropic", "anthropic")]:
        try:
            __import__(import_name)
        except ImportError:
            print(f"Installing {pkg}...", file=sys.stderr)
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            )

_ensure_packages()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
PROMPT_FILE = SKILL_DIR / "references" / "debrief-prompt.md"
OBSIDIAN_DEBRIEFS = Path.home() / "Documents" / "ObsidianNotes" / "Claude-Research" / "call-debriefs"
OBSIDIAN_ACCOUNTS = Path.home() / "Documents" / "ObsidianNotes" / "Claude-Research" / "accounts"
DEFAULT_MODEL = "claude-4-6-sonnet"

# ---------------------------------------------------------------------------
# VTT Parser
# ---------------------------------------------------------------------------

def parse_vtt(content: str) -> str:
    """Parse VTT transcript into clean Speaker: text format."""
    lines = content.splitlines()
    result = []
    current_speaker = None
    current_text = []

    for line in lines:
        line = line.strip()
        # Skip VTT header, empty lines, timestamps, NOTE blocks
        if not line or line == "WEBVTT" or line.startswith("NOTE"):
            continue
        if re.match(r'\d{2}:\d{2}', line) and '-->' in line:
            continue
        if re.match(r'^\d+$', line):
            continue

        # Extract speaker from <v Name> format
        v_match = re.match(r'<v\s+([^>]+)>(.*?)(?:</v>)?$', line)
        if v_match:
            speaker = v_match.group(1).strip()
            text = v_match.group(2).strip()
        else:
            # Try "Speaker Name: text" format
            colon_match = re.match(r'^([A-Z][^:]{1,40}):\s+(.+)', line)
            if colon_match:
                speaker = colon_match.group(1).strip()
                text = colon_match.group(2).strip()
            else:
                speaker = current_speaker
                text = line

        if speaker == current_speaker:
            current_text.append(text)
        else:
            if current_speaker and current_text:
                result.append(f"{current_speaker}: {' '.join(current_text)}")
            current_speaker = speaker
            current_text = [text] if text else []

    if current_speaker and current_text:
        result.append(f"{current_speaker}: {' '.join(current_text)}")

    return "\n\n".join(result)

# ---------------------------------------------------------------------------
# Claude API call
# ---------------------------------------------------------------------------

def analyze_with_claude(transcript: str, account: str, date: str, model: str) -> str:
    """Send transcript to Claude for debrief analysis."""
    from anthropic import Anthropic

    api_key = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("LITELLM_KEY")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://llm.atko.ai")

    if not api_key:
        print("Error: ANTHROPIC_AUTH_TOKEN or LITELLM_KEY required in env.", file=sys.stderr)
        print("Check ~/.claude-litellm.env", file=sys.stderr)
        sys.exit(1)

    client = Anthropic(api_key=api_key, base_url=base_url)

    system_prompt = ""
    if PROMPT_FILE.exists():
        system_prompt = PROMPT_FILE.read_text()
    else:
        system_prompt = "You are a Sales Engineer analyzing a call transcript. Produce a structured debrief."

    user_msg = f"""## Account: {account}
## Call Date: {date}

---

## Transcript

{transcript}"""

    print(f"Analyzing with {model}...", file=sys.stderr)
    response = client.messages.create(
        model=model,
        max_tokens=8000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )

    result = response.content[0].text
    usage = response.usage
    print(
        f"Tokens — input: {usage.input_tokens:,}, output: {usage.output_tokens:,}",
        file=sys.stderr,
    )
    return result

# ---------------------------------------------------------------------------
# Output functions
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def write_debrief(account: str, date: str, content: str) -> Path:
    """Write debrief to Obsidian call-debriefs folder."""
    slug = slugify(account)
    OBSIDIAN_DEBRIEFS.mkdir(parents=True, exist_ok=True)
    out_path = OBSIDIAN_DEBRIEFS / f"{slug}-{date}.md"

    frontmatter = f"""---
date: {date}
tags:
  - call-debrief
  - {slug}
source: claude-code
project: se-accounts
account: {account}
---

> Related: [[accounts/{slug}]] [[call-debrief-index]]

"""
    out_path.write_text(frontmatter + content)
    return out_path


def integrate_with_account_brief(account: str, date: str, content: str):
    """Append a Call Log entry to the existing account-research brief."""
    slug = slugify(account)

    if not OBSIDIAN_ACCOUNTS.is_dir():
        print("  No accounts directory found, skipping integration.", file=sys.stderr)
        return

    brief_path = None
    for f in sorted(OBSIDIAN_ACCOUNTS.iterdir(), reverse=True):
        if f.name.startswith(slug) and f.suffix == ".md":
            brief_path = f
            break

    if not brief_path:
        print(f"  No existing brief for {account}, skipping integration.", file=sys.stderr)
        return

    brief_text = brief_path.read_text()

    # Extract summary from Executive Summary section
    exec_match = re.search(r'## Executive Summary\s*\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    summary = exec_match.group(1).strip()[:200] if exec_match else "See full debrief."

    # Extract participants
    participants_match = re.search(r'Participants:\s*(.+)', content)
    participants = participants_match.group(1).strip() if participants_match else "See debrief"

    # Extract action items (first 3)
    actions = re.findall(r'- \[[ x]\] (.+?)(?:\n|$)', content)
    next_steps = "; ".join(actions[:3]) if actions else "See debrief"

    entry = f"""
### {date} — Call Debrief
- **Participants:** {participants}
- **Key findings:** {summary}
- **Next steps:** {next_steps}
- **Debrief:** [[call-debriefs/{slug}-{date}]]
"""

    if "## Call Log" in brief_text:
        brief_text = brief_text.replace("## Call Log", f"## Call Log\n{entry}", 1)
    else:
        brief_text = brief_text.rstrip() + f"\n\n## Call Log\n{entry}"

    brief_path.write_text(brief_text)
    print(f"  -> Integrated with: {brief_path}", file=sys.stderr)

# ---------------------------------------------------------------------------
# CLI + main
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="SE call transcript analysis → structured debrief"
    )
    parser.add_argument("transcript", help="Path to VTT or TXT transcript file")
    parser.add_argument("--account", "-a", required=True, help="Account name")
    parser.add_argument("--date", "-d", default=None, help="Call date (YYYY-MM-DD, default today)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Claude model")
    args = parser.parse_args()
    if not args.date:
        args.date = datetime.now().strftime("%Y-%m-%d")
    return args


def main():
    args = parse_args()

    # 1. Read transcript
    transcript_path = Path(args.transcript).expanduser().resolve()
    if not transcript_path.exists():
        print(f"Error: File not found: {transcript_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading: {transcript_path}", file=sys.stderr)
    raw = transcript_path.read_text()

    # 2. Parse VTT if applicable
    if transcript_path.suffix.lower() == ".vtt":
        print("Parsing VTT format...", file=sys.stderr)
        transcript = parse_vtt(raw)
        print(f"  -> {len(transcript.splitlines())} speaker segments", file=sys.stderr)
    else:
        transcript = raw

    # 3. Analyze with Claude
    debrief = analyze_with_claude(transcript, args.account, args.date, args.model)

    # 4. Write debrief to Obsidian
    out_path = write_debrief(args.account, args.date, debrief)
    print(f"\nDebrief saved: {out_path}", file=sys.stderr)

    # 5. Integrate with account brief
    integrate_with_account_brief(args.account, args.date, debrief)

    # 6. Print path to stdout
    print(str(out_path))


if __name__ == "__main__":
    main()
