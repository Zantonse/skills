#!/usr/bin/env python3
"""SE call transcript analysis — VTT/TXT parsing + Claude debrief synthesis.

Usage:
    python3 analyze_transcript.py /path/to/call.vtt --account "NetApp"
    python3 analyze_transcript.py /path/to/call.txt --account "Deel" --date 2026-03-05
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
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
FOLLOWUP_PROMPT_FILE = SKILL_DIR / "references" / "followup-prompt.md"
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
# Prior debrief loader
# ---------------------------------------------------------------------------

def load_prior_debrief(account: str, max_age_days: int = 90) -> Optional[tuple]:
    """Search OBSIDIAN_DEBRIEFS for the most recent debrief for this account.

    Returns (date_str, extracted_context_string) or None if no suitable file found.
    """
    if not OBSIDIAN_DEBRIEFS.is_dir():
        print("  No debriefs directory found, skipping prior debrief load.", file=sys.stderr)
        return None

    slug = slugify(account)
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')
    candidates = []

    for f in OBSIDIAN_DEBRIEFS.iterdir():
        if f.name.startswith(slug) and f.suffix == ".md":
            date_match = date_pattern.search(f.name)
            if date_match:
                candidates.append((date_match.group(1), f))

    if not candidates:
        print(f"  No prior debriefs found for {account}.", file=sys.stderr)
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    prior_date_str, prior_path = candidates[0]

    try:
        prior_date = datetime.strptime(prior_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"  Could not parse date from filename: {prior_path.name}", file=sys.stderr)
        return None

    age_days = (datetime.now() - prior_date).days
    stale_flag = age_days > max_age_days

    if stale_flag:
        print(
            f"  Prior debrief found but is {age_days} days old (>{max_age_days} days) — flagging as potentially stale.",
            file=sys.stderr,
        )
    else:
        print(f"  Loaded prior debrief: {prior_path.name} ({age_days} days ago)", file=sys.stderr)

    try:
        prior_text = prior_path.read_text()
    except Exception as e:
        print(f"  Could not read prior debrief: {e}", file=sys.stderr)
        return None

    sections_to_extract = [
        ("Executive Summary", r'## Executive Summary\s*\n(.*?)(?=\n## |\Z)'),
        ("MEDDPICC Scorecard", r'## MEDDPICC Scorecard\s*\n(.*?)(?=\n## |\Z)'),
        ("Relationship Map", r'## Relationship Map\s*\n(.*?)(?=\n## |\Z)'),
        ("Action Items", r'## Action Items[^\n]*\s*\n(.*?)(?=\n## |\Z)'),
    ]

    extracted_parts = []
    for section_name, pattern in sections_to_extract:
        match = re.search(pattern, prior_text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            extracted_parts.append(f"### {section_name}\n{content}")
            print(f"    -> Extracted section: {section_name}", file=sys.stderr)
        else:
            print(f"    -> Section not found (v1 format?), skipping: {section_name}", file=sys.stderr)

    if not extracted_parts:
        print("  No usable sections found in prior debrief.", file=sys.stderr)
        return None

    stale_notice = "\n\n> NOTE: This prior debrief is more than 90 days old and may be stale." if stale_flag else ""
    context = f"## Prior Debrief Context ({prior_date_str}){stale_notice}\n\n" + "\n\n".join(extracted_parts)

    return (prior_date_str, context)

# ---------------------------------------------------------------------------
# Claude API calls
# ---------------------------------------------------------------------------

def analyze_with_claude(
    transcript: str,
    account: str,
    date: str,
    model: str,
    prior_context: Optional[str] = None,
) -> str:
    """Send transcript to Claude for debrief analysis (Pass 1)."""
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

    if prior_context:
        user_msg += f"\n\n---\n\n{prior_context}"

    print(f"Pass 1: Analyzing with {model}...", file=sys.stderr)
    response = client.messages.create(
        model=model,
        max_tokens=12000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )

    result = response.content[0].text
    usage = response.usage
    print(
        f"Pass 1 tokens — input: {usage.input_tokens:,}, output: {usage.output_tokens:,}",
        file=sys.stderr,
    )
    return result


def generate_followups(debrief: str, account: str, model: str) -> str:
    """Send Pass 1 debrief to Claude for combined AE+SE follow-up email draft (Pass 2)."""
    from anthropic import Anthropic

    api_key = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("LITELLM_KEY")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://llm.atko.ai")

    if not api_key:
        print("Error: ANTHROPIC_AUTH_TOKEN or LITELLM_KEY required in env.", file=sys.stderr)
        sys.exit(1)

    client = Anthropic(api_key=api_key, base_url=base_url)

    if FOLLOWUP_PROMPT_FILE.exists():
        system_prompt = FOLLOWUP_PROMPT_FILE.read_text()
    else:
        system_prompt = (
            "You are drafting a combined AE+SE follow-up email based on a structured call debrief. "
            "Produce a single follow-up email co-sent by the AE and SE, 200-350 words."
        )

    user_msg = f"""## Account: {account}

## Call Debrief

{debrief}"""

    print(f"Pass 2: Generating follow-ups with {model}...", file=sys.stderr)
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )

    result = response.content[0].text
    usage = response.usage
    print(
        f"Pass 2 tokens — input: {usage.input_tokens:,}, output: {usage.output_tokens:,}",
        file=sys.stderr,
    )
    return result

# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

def extract_call_type(debrief: str) -> str:
    """Extract the call type from the Pass 1 debrief output."""
    match = re.search(r'\*\*Call Type:\s*([\w-]+)\*\*', debrief)
    if match:
        return match.group(1).strip()
    return "discussion-sync"


def extract_meddpicc_score(debrief: str) -> Optional[int]:
    """Extract the overall MEDDPICC percentage from the Pass 1 debrief output."""
    match = re.search(r'\*\*Overall:\s*(\d+)%\*\*', debrief)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None


def extract_participants(debrief: str) -> list:
    """Extract participant names from the Participants & Roles markdown table."""
    participants = []
    in_table = False
    header_found = False

    for line in debrief.splitlines():
        if re.search(r'## Participants', line, re.IGNORECASE):
            in_table = True
            header_found = False
            continue
        if in_table:
            if line.strip().startswith("##"):
                break
            if not line.strip():
                continue
            if re.match(r'\s*\|[-| ]+\|\s*$', line):
                header_found = True
                continue
            if "|" in line:
                if not header_found:
                    header_found = True
                    continue
                cells = [c.strip() for c in line.split("|")]
                cells = [c for c in cells if c]
                if cells:
                    name = cells[0].strip()
                    if name and name.lower() not in ("name", "speaker", "participant"):
                        participants.append(name)

    return participants


def extract_slack_summary(debrief: str) -> str:
    """Extract the content of the Slack Summary section."""
    match = re.search(r'## Slack Summary\s*\n(.*?)(?=\n## |\Z)', debrief, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

# ---------------------------------------------------------------------------
# Output functions
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def write_debrief(
    account: str,
    date: str,
    content: str,
    call_type: str = "discussion-sync",
    participants: Optional[list] = None,
    meddpicc_score: Optional[int] = None,
    prior_debrief_date: Optional[str] = None,
) -> Path:
    """Write debrief to Obsidian call-debriefs folder with enhanced frontmatter."""
    slug = slugify(account)
    OBSIDIAN_DEBRIEFS.mkdir(parents=True, exist_ok=True)
    out_path = OBSIDIAN_DEBRIEFS / f"{slug}-{date}.md"

    participants_list = participants if participants else []
    participants_yaml = json.dumps(participants_list)

    meddpicc_line = f"meddpicc-score: {meddpicc_score}" if meddpicc_score is not None else "meddpicc-score: null"

    prior_debrief_value = f"{slug}-{prior_debrief_date}" if prior_debrief_date else "null"

    frontmatter = f"""---
date: {date}
tags:
  - call-debrief
  - {slug}
  - {call_type}
source: claude-code
project: se-accounts
account: {account}
call-type: {call_type}
participants: {participants_yaml}
{meddpicc_line}
prior-debrief: {prior_debrief_value}
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

    # 3. Load prior debrief
    prior_result = load_prior_debrief(args.account)
    prior_debrief_date = None
    prior_context = None
    if prior_result is not None:
        prior_debrief_date, prior_context = prior_result

    # 4. Pass 1: Analyze with Claude
    debrief = analyze_with_claude(
        transcript,
        args.account,
        args.date,
        args.model,
        prior_context=prior_context,
    )

    # 5. Extract metadata from debrief
    call_type = extract_call_type(debrief)
    meddpicc_score = extract_meddpicc_score(debrief)
    participants = extract_participants(debrief)

    print(f"  -> Call type: {call_type}", file=sys.stderr)
    if meddpicc_score is not None:
        print(f"  -> MEDDPICC score: {meddpicc_score}%", file=sys.stderr)
    if participants:
        print(f"  -> Participants: {', '.join(participants)}", file=sys.stderr)

    # 6. Pass 2: Generate follow-ups (skip for internal-prep)
    combined_debrief = debrief
    if call_type != "internal-prep":
        try:
            followups = generate_followups(debrief, args.account, args.model)
            combined_debrief = debrief + "\n\n---\n\n## Follow-Up Email\n\n" + followups
        except Exception as e:
            print(f"  Warning: Pass 2 follow-up generation failed: {e}", file=sys.stderr)
            combined_debrief = debrief
    else:
        print("  -> Skipping follow-up emails (internal-prep call type).", file=sys.stderr)

    # 7. Write debrief to Obsidian
    out_path = write_debrief(
        args.account,
        args.date,
        combined_debrief,
        call_type=call_type,
        participants=participants,
        meddpicc_score=meddpicc_score,
        prior_debrief_date=prior_debrief_date,
    )
    print(f"\nDebrief saved: {out_path}", file=sys.stderr)

    # 8. Print Slack summary to stderr
    slack_summary = extract_slack_summary(combined_debrief)
    if slack_summary:
        print("\n--- SLACK SUMMARY (copy-paste) ---", file=sys.stderr)
        print(slack_summary, file=sys.stderr)
        print("--- END SLACK SUMMARY ---\n", file=sys.stderr)

    # 9. Integrate with account brief
    integrate_with_account_brief(args.account, args.date, combined_debrief)

    # 10. Print path to stdout
    print(str(out_path))


if __name__ == "__main__":
    main()
