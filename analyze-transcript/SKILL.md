---
name: analyze-transcript
description: "SE call debrief from VTT/TXT transcripts. Identifies speakers, produces structured debriefs with discovery findings, competitive signals, relationship mapping, action items, and discovery quality scoring. Integrates with existing account-research briefs by appending Call Log entries. Use when the user asks to analyze a transcript, debrief a call, review a meeting recording, or extract insights from a conversation. Triggers on: 'analyze transcript', 'debrief this call', 'analyze call', 'what happened in this call', 'review this meeting', or any request combining a file path (.vtt/.txt) with analysis, debrief, or call review intent."
---

# Analyze Transcript

Produce SE call debriefs from VTT/TXT transcripts and integrate with account-research briefs.

## How It Works

The skill uses `scripts/analyze_transcript.py` to:
1. Read and preprocess the transcript (VTT speaker label parsing, timestamp stripping)
2. Send the full transcript to Claude (via Anthropic SDK through LiteLLM proxy)
3. Produce a structured debrief with discovery findings, competitive signals, relationship map, action items
4. Write to `~/Documents/ObsidianNotes/Claude-Research/call-debriefs/`
5. Append a Call Log entry to the existing account-research brief (if one exists)

## Usage

```bash
python3 <skill-path>/scripts/analyze_transcript.py /path/to/call.vtt --account "NetApp"
python3 <skill-path>/scripts/analyze_transcript.py /path/to/call.txt --account "Deel" --date 2026-03-05
```

Replace `<skill-path>` with: `/Users/craigverzosa/.claude/skills/analyze-transcript`

## Invocation

Parse the user's request to extract:
1. **File path** (required — the VTT or TXT transcript)
2. **Account name** (required — infer from context if user says "analyze this Deel call")
3. **Date** (optional — defaults to today)

Then dispatch:

```
Task tool (Bash subagent, model: "sonnet"):
  prompt: |
    Run: python3 /Users/craigverzosa/.claude/skills/analyze-transcript/scripts/analyze_transcript.py "{FILE_PATH}" --account "{ACCOUNT}" [--date "{DATE}"]
    Report the output path from stdout and any errors from stderr.
```

## After Running

1. Report the debrief file path
2. Summarize key findings conversationally: executive summary, top pain points, competitive signals, action items
3. Mention if the Call Log was integrated into an existing account brief
4. Note the discovery quality score
5. User can open the full debrief in Obsidian

## Output Location

- Debriefs: `~/Documents/ObsidianNotes/Claude-Research/call-debriefs/{account-slug}-{YYYY-MM-DD}.md`
- Account integration: Appends `## Call Log` entry to existing account brief

## Dependencies

- Python 3 with `anthropic` (auto-installed if missing)
- Credentials in `~/.claude-litellm.env` (ANTHROPIC_AUTH_TOKEN + ANTHROPIC_BASE_URL)
- Obsidian vault at `~/Documents/ObsidianNotes/`
