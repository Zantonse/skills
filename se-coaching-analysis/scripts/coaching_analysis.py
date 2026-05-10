#!/usr/bin/env python3
"""SE coaching analysis — transcript → structured CoachingAnalysis JSON.

Usage:
    python3 coaching_analysis.py /path/to/call.vtt --account "NetApp"
    python3 coaching_analysis.py /path/to/call.txt --account "Deel" --date 2026-03-05
    python3 coaching_analysis.py /path/to/call.txt --account "Deel" --json
"""

import argparse
import json
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
PROMPT_FILE = SKILL_DIR / "references" / "coaching-prompt.md"
OBSIDIAN_COACHING = Path.home() / "Documents" / "ObsidianNotes" / "Claude-Research" / "coaching"
DEFAULT_MODEL = "claude-4-6-sonnet"

# Default JSON output directory for the Coaching dashboard
COACHING_DASHBOARD_DATA = Path.home() / "Documents" / "Work" / "Okta" / "SalesEngineering" / "Coaching" / "data" / "analyses"

# ---------------------------------------------------------------------------
# VTT Parser (same as analyze-transcript)
# ---------------------------------------------------------------------------

def parse_vtt(content: str) -> str:
    """Parse VTT transcript into clean Speaker: text format."""
    lines = content.splitlines()
    result = []
    current_speaker = None
    current_text = []

    for line in lines:
        line = line.strip()
        if not line or line == "WEBVTT" or line.startswith("NOTE"):
            continue
        if re.match(r'\d{2}:\d{2}', line) and '-->' in line:
            continue
        if re.match(r'^\d+$', line):
            continue

        v_match = re.match(r'<v\s+([^>]+)>(.*?)(?:</v>)?$', line)
        if v_match:
            speaker = v_match.group(1).strip()
            text = v_match.group(2).strip()
        else:
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

def analyze_with_claude(transcript: str, account: str, date: str, model: str) -> dict:
    """Send transcript to Claude for coaching analysis. Returns parsed JSON."""
    from anthropic import Anthropic

    api_key = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("LITELLM_KEY")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://llm.atko.ai")

    if not api_key:
        print("Error: ANTHROPIC_AUTH_TOKEN or LITELLM_KEY required in env.", file=sys.stderr)
        print("Check ~/.claude-litellm.env", file=sys.stderr)
        sys.exit(1)

    client = Anthropic(api_key=api_key, base_url=base_url)

    if PROMPT_FILE.exists():
        system_prompt = PROMPT_FILE.read_text()
    else:
        print("Warning: coaching-prompt.md not found, using fallback prompt.", file=sys.stderr)
        system_prompt = (
            "You are a senior SE coach. Analyze this call transcript and produce a "
            "CoachingAnalysis JSON object scoring the SE's performance across 7 dimensions."
        )

    user_msg = f"""## Account: {account}
## Call Date: {date}

---

## Transcript

{transcript}"""

    print(f"Analyzing with {model}...", file=sys.stderr)
    response = client.messages.create(
        model=model,
        max_tokens=12000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )

    result_text = response.content[0].text
    usage = response.usage
    print(
        f"Tokens — input: {usage.input_tokens:,}, output: {usage.output_tokens:,}",
        file=sys.stderr,
    )

    # Extract JSON from response — handle potential markdown fencing
    json_text = result_text.strip()
    if json_text.startswith("```"):
        # Strip markdown code fence
        lines = json_text.splitlines()
        # Remove first line (```json or ```) and last line (```)
        if lines[-1].strip() == "```":
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        json_text = "\n".join(lines)

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"Error: Claude returned invalid JSON: {e}", file=sys.stderr)
        print(f"Raw output (first 500 chars): {result_text[:500]}", file=sys.stderr)
        sys.exit(1)

    return data

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = [
    "id", "date", "callType", "duration", "attendees", "overall",
    "dimensions", "metrics", "strengths", "development",
    "learningPoints", "nextTimeActions", "selfReflection",
]

VALID_CALL_TYPES = {"discovery", "demo", "poc", "competitive", "executive", "qbr", "follow-up"}


def validate_analysis(data: dict, date: str) -> dict:
    """Validate and fix the CoachingAnalysis JSON. Returns cleaned data."""
    # Check required fields
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        print(f"Warning: Missing fields from Claude output: {missing}", file=sys.stderr)
        # Add defaults for missing fields
        defaults = {
            "id": "",
            "date": date,
            "callType": "discovery",
            "duration": 0,
            "attendees": {"se": "Craig", "customer": []},
            "overall": 0,
            "dimensions": [],
            "metrics": {
                "talkRatioSE": 50, "talkRatioCustomer": 50,
                "questionsAsked": 0, "openQuestions": 0, "closedQuestions": 0,
                "longestMonologue": 0, "customerQuestions": 0,
                "nextStepQuality": "none",
            },
            "strengths": [],
            "development": [],
            "learningPoints": [],
            "nextTimeActions": [],
            "selfReflection": "",
        }
        for f in missing:
            data[f] = defaults.get(f, "")

    # Normalize callType
    ct = data.get("callType", "discovery")
    if ct not in VALID_CALL_TYPES:
        # Try common variations
        ct_map = {
            "follow_up": "follow-up",
            "followup": "follow-up",
            "discussion-sync": "follow-up",
            "discussion_sync": "follow-up",
        }
        data["callType"] = ct_map.get(ct, "discovery")
        print(f"  -> Normalized callType '{ct}' to '{data['callType']}'", file=sys.stderr)

    # Ensure date matches
    data["date"] = date

    # Ensure overall is sum of dimension scores
    if data.get("dimensions"):
        computed_total = sum(d.get("score", 0) for d in data["dimensions"])
        if computed_total != data.get("overall", 0):
            print(
                f"  -> Corrected overall: {data.get('overall')} -> {computed_total} (sum of dimensions)",
                file=sys.stderr,
            )
            data["overall"] = computed_total

    # Ensure all 7 dimensions exist
    expected_dims = {
        "Discovery Depth", "Value Alignment", "Listening & Interactivity",
        "Objection Handling", "Technical Credibility", "Next Step Discipline",
        "Presence & Collaboration",
    }
    actual_dims = {d.get("name", "") for d in data.get("dimensions", [])}
    if actual_dims != expected_dims:
        missing_dims = expected_dims - actual_dims
        if missing_dims:
            print(f"  -> Warning: Missing dimensions: {missing_dims}", file=sys.stderr)

    # Defaults for new optional fields
    if "missedSignals" not in data:
        data["missedSignals"] = []
    if "championScore" not in data:
        data["championScore"] = {
            "score": 0,
            "championIdentified": False,
            "equippedWithValueNarrative": False,
            "internalPitchBuilt": False,
            "reasoning": "Not assessed",
        }
    if "engagementSignals" not in data:
        data["engagementSignals"] = []

    # Clamp championScore.score to 0-10 and derive stage from booleans
    cs = data.get("championScore", {})
    if isinstance(cs, dict) and "score" in cs:
        cs["score"] = max(0, min(10, cs["score"]))
        # Derive MEDDIC champion stage if missing
        if "stage" not in cs:
            if cs.get("internalPitchBuilt"):
                cs["stage"] = "test"
            elif cs.get("equippedWithValueNarrative"):
                cs["stage"] = "develop"
            elif cs.get("championIdentified"):
                cs["stage"] = "identify"
            else:
                cs["stage"] = "none"

    # Strip wastedDemo for non-demo calls; default to None if absent
    ct = data.get("callType", "discovery")
    if ct != "demo":
        data.pop("wastedDemo", None)
    elif "wastedDemo" not in data:
        data["wastedDemo"] = None

    # Ensure each development entry has talkTracks
    for d in data.get("development", []):
        if "talkTracks" not in d:
            d["talkTracks"] = []

    # Validate score ranges
    overall = data.get("overall", 0)
    if not (0 <= overall <= 100):
        data["overall"] = max(0, min(100, overall))
        print(f"  -> Clamped overall to {data['overall']}", file=sys.stderr)

    return data

# ---------------------------------------------------------------------------
# Output functions
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def write_json(data: dict, account: str, date: str) -> Path:
    """Write CoachingAnalysis JSON to the dashboard data directory."""
    COACHING_DASHBOARD_DATA.mkdir(parents=True, exist_ok=True)

    call_type = data.get("callType", "discovery")
    filename = f"{date}-{call_type}.json"
    out_path = COACHING_DASHBOARD_DATA / filename

    # Handle duplicate filenames
    counter = 2
    while out_path.exists():
        filename = f"{date}-{call_type}-{counter}.json"
        out_path = COACHING_DASHBOARD_DATA / filename
        counter += 1

    # Set the id to match filename stem
    data["id"] = out_path.stem

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    return out_path


def write_obsidian(data: dict, account: str, date: str) -> Path:
    """Write a coaching report to Obsidian as a readable markdown note."""
    OBSIDIAN_COACHING.mkdir(parents=True, exist_ok=True)

    slug = slugify(account)
    call_type = data.get("callType", "discovery")
    out_path = OBSIDIAN_COACHING / f"{slug}-{date}.md"

    overall = data.get("overall", 0)
    dims = data.get("dimensions", [])
    metrics = data.get("metrics", {})

    # Build markdown
    lines = []
    lines.append("---")
    lines.append(f"date: {date}")
    lines.append("tags:")
    lines.append("  - coaching")
    lines.append(f"  - {slug}")
    lines.append(f"  - {call_type}")
    lines.append("source: claude-code")
    lines.append("project: se-coaching")
    lines.append(f"account: {account}")
    lines.append(f"call-type: {call_type}")
    lines.append(f"score: {overall}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Coaching Analysis: {account} — {date}")
    lines.append("")
    lines.append(f"> Call Type: {call_type} | Duration: ~{data.get('duration', '?')} min | Score: **{overall}/100**")
    lines.append("")

    # Self-reflection (at the top, before the analysis)
    reflection = data.get("selfReflection", "")
    if reflection:
        lines.append("## Self-Reflection")
        lines.append("")
        lines.append(f"> *{reflection}*")
        lines.append("")

    # Dimensions
    lines.append("## Dimension Scores")
    lines.append("")
    lines.append("| Dimension | Score | Weight | % |")
    lines.append("|-----------|-------|--------|---|")
    for d in dims:
        name = d.get("name", "")
        score = d.get("score", 0)
        weight = d.get("weight", 0)
        pct = round(score / weight * 100) if weight > 0 else 0
        lines.append(f"| {name} | {score} | {weight} | {pct}% |")
    lines.append("")

    # Metrics
    lines.append("## Key Metrics")
    lines.append("")
    lines.append(f"- **Talk ratio:** SE {metrics.get('talkRatioSE', '?')}% / Customer {metrics.get('talkRatioCustomer', '?')}%")
    lines.append(f"- **Questions asked:** {metrics.get('questionsAsked', '?')} (open: {metrics.get('openQuestions', '?')}, closed: {metrics.get('closedQuestions', '?')})")
    lines.append(f"- **Longest monologue:** {metrics.get('longestMonologue', '?')} min")
    lines.append(f"- **Customer questions:** {metrics.get('customerQuestions', '?')}")
    lines.append(f"- **Next step quality:** {metrics.get('nextStepQuality', '?')}")
    lines.append("")

    # Strengths
    strengths = data.get("strengths", [])
    if strengths:
        lines.append("## Strengths")
        lines.append("")
        for s in strengths:
            lines.append(f"### {s.get('label', '')} (+{s.get('scoreContribution', 0)} pts, {s.get('dimension', '')})")
            lines.append("")
            lines.append(f"**Situation:** {s.get('situation', '')}")
            lines.append("")
            lines.append(f"**Behavior:** {s.get('behavior', '')}")
            lines.append("")
            lines.append(f"**Impact:** {s.get('impact', '')}")
            lines.append("")
            lines.append(f"*Pattern to reinforce: {s.get('pattern', '')}*")
            lines.append("")

    # Development
    dev = data.get("development", [])
    if dev:
        lines.append("## Development Areas")
        lines.append("")
        for d in dev:
            lines.append(f"### {d.get('label', '')} ({d.get('scoreImpact', 0)} pts, {d.get('dimension', '')})")
            lines.append("")
            lines.append(f"**Situation:** {d.get('situation', '')}")
            lines.append("")
            lines.append(f"**Behavior:** {d.get('behavior', '')}")
            lines.append("")
            lines.append(f"**Impact:** {d.get('impact', '')}")
            lines.append("")
            lines.append(f"> **Alternative approach:** {d.get('alternative', '')}")
            lines.append("")
            # Talk tracks for this development area
            tracks = d.get("talkTracks", [])
            if tracks:
                for t in tracks:
                    lines.append(f"**🎯 {t.get('label', '')}** — *{t.get('context', '')}*")
                    lines.append(f"> \"{t.get('line', '')}\"")
                    lines.append("")

    # Missed Signals
    signals = data.get("missedSignals", [])
    if signals:
        lines.append("## Missed Signals")
        lines.append("")
        for s in signals:
            lines.append(f"### \"{s.get('quote', '')}\" — {s.get('speaker', '')} ({s.get('signalType', '')})")
            lines.append("")
            lines.append(f"**Missed opportunity:** {s.get('missedOpportunity', '')}")
            lines.append("")
            lines.append(f"**Follow-up to ask:** \"{s.get('suggestedQuestion', '')}\"")
            lines.append("")
            lines.append(f"*Dimension: {s.get('dimension', '')}*")
            lines.append("")

    # Champion Score
    cs = data.get("championScore", {})
    if cs and isinstance(cs, dict):
        lines.append("## Champion Score")
        lines.append("")
        score = cs.get("score", 0)
        lines.append(f"**Score: {score}/10**")
        lines.append("")
        ci = "Yes" if cs.get("championIdentified") else "No"
        vn = "Yes" if cs.get("equippedWithValueNarrative") else "No"
        ip = "Yes" if cs.get("internalPitchBuilt") else "No"
        lines.append(f"- Champion identified: {ci}")
        lines.append(f"- Equipped with value narrative: {vn}")
        lines.append(f"- Internal pitch built: {ip}")
        lines.append("")
        if cs.get("reasoning"):
            lines.append(f"*{cs['reasoning']}*")
            lines.append("")

    # Engagement Signals
    engagement = data.get("engagementSignals", [])
    if engagement:
        lines.append("## Engagement Signals")
        lines.append("")
        lines.append("| Attendee | Phase | Engagement | Evidence |")
        lines.append("|----------|-------|------------|----------|")
        for e in engagement:
            lines.append(f"| {e.get('attendee', '')} | {e.get('phase', '')} | {e.get('engagement', '')} | {e.get('evidence', '')} |")
        lines.append("")

    # Learning Points
    lps = data.get("learningPoints", [])
    if lps:
        lines.append("## Learning Points")
        lines.append("")
        for lp in lps:
            lines.append(f"### {lp.get('title', '')}")
            lines.append("")
            lines.append(f"{lp.get('whatHappened', '')}")
            lines.append("")
            lines.append(f"**Principle:** {lp.get('principle', '')}")
            lines.append("")
            lines.append(f"**Where this applies:** {lp.get('whereApplies', '')}")
            lines.append("")

    # Next-Time Actions
    ntas = data.get("nextTimeActions", [])
    if ntas:
        lines.append("## Next-Time Actions")
        lines.append("")
        for nta in ntas:
            lines.append(f"### {nta.get('label', '')}")
            lines.append("")
            lines.append(f"**Trigger:** {nta.get('trigger', '')}")
            lines.append("")
            lines.append(f"**Do this:** {nta.get('behavior', '')}")
            lines.append("")
            lines.append(f"**Practice:** {nta.get('practice', '')}")
            lines.append("")

    out_path.write_text("\n".join(lines))
    return out_path

# ---------------------------------------------------------------------------
# CLI + main
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="SE coaching analysis — transcript → scored CoachingAnalysis"
    )
    parser.add_argument("transcript", help="Path to VTT or TXT transcript file")
    parser.add_argument("--account", "-a", required=True, help="Account name")
    parser.add_argument("--date", "-d", default=None, help="Call date (YYYY-MM-DD, default today)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Claude model")
    parser.add_argument(
        "--json", dest="write_json", action="store_true",
        help="Write CoachingAnalysis JSON to the Coaching dashboard data directory",
    )
    parser.add_argument(
        "--json-dir", default=None,
        help="Override the JSON output directory (default: Coaching/data/analyses/)",
    )
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
    data = analyze_with_claude(transcript, args.account, args.date, args.model)

    # 4. Validate and fix
    data = validate_analysis(data, args.date)

    call_type = data.get("callType", "discovery")
    overall = data.get("overall", 0)
    print(f"  -> Call type: {call_type}", file=sys.stderr)
    print(f"  -> Overall score: {overall}/100", file=sys.stderr)

    # 5. Write Obsidian note (always)
    obsidian_path = write_obsidian(data, args.account, args.date)
    print(f"\nObsidian note: {obsidian_path}", file=sys.stderr)

    # 6. Write JSON (if --json flag)
    if args.write_json:
        if args.json_dir:
            global COACHING_DASHBOARD_DATA
            COACHING_DASHBOARD_DATA = Path(args.json_dir).expanduser().resolve()
        json_path = write_json(data, args.account, args.date)
        print(f"Dashboard JSON: {json_path}", file=sys.stderr)
    else:
        print("Tip: Use --json to also write to the Coaching dashboard.", file=sys.stderr)

    # 7. Print JSON to stdout for piping
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
