---
name: analyze-transcript
description: "SE account team call debrief from VTT/TXT transcripts or pasted transcript text. Auto-detects call type (discovery, demo, roadmap-review, qbr, renewal, internal-prep, executive-briefing, discussion-sync) and produces adaptive structured debriefs with MEDDPICC scorecards, competitive signals, relationship mapping, role-tagged action items, call-over-call delta reports, Slack team summaries, and a combined AE+SE follow-up email draft. Integrates with existing account-research briefs by appending Call Log entries. Use when the user asks to analyze a transcript, debrief a call, review a meeting recording, extract insights from a conversation, score a deal, or run MEDDPICC qualification. Triggers on: 'analyze transcript', 'debrief this call', 'analyze call', 'what happened in this call', 'review this meeting', 'MEDDPICC', 'deal qualification', 'call follow-up', 'post-call', any request combining a file path (.vtt/.txt) with analysis, debrief, or call review intent, OR when the user pastes transcript text directly (e.g., 'here's the transcript') with an account context."
---

# Analyze Transcript

Produce adaptive SE account team call debriefs from VTT/TXT transcripts, with MEDDPICC scoring, delta reports, Slack summaries, and a combined AE+SE follow-up email draft.

## How It Works

The skill uses a two-pass architecture in `scripts/analyze_transcript.py`:

**Before Pass 1**, the script auto-loads the most recent prior debrief for the same account (within 90 days) from the Obsidian vault and appends it as context to the analysis prompt. If no prior debrief exists, the delta section is omitted and a "First recorded call for this account" note is included.

**Pass 1 — Analysis** (`claude-4-6-sonnet`, up to 12,000 output tokens):
1. Read and preprocess the transcript (VTT speaker label parsing, timestamp stripping)
2. Auto-detect call type from transcript content (discovery, demo, roadmap-review, qbr, renewal, internal-prep, executive-briefing, discussion-sync)
3. Produce a structured debrief adapted to the detected call type, including: executive summary, Slack summary, participants and roles, discovery findings, competitive signals, relationship map, MEDDPICC scorecard, delta report (if prior exists), role-tagged action items (`[SE]`, `[AE]`, `[CSM]`, `[TEAM]`), discovery quality assessment, key quotes, and key metrics
4. Extract metadata: call type, MEDDPICC score, participant names

**Pass 2 — Follow-Up Email** (`claude-4-6-sonnet`, up to 4,000 output tokens):
- Input is the Pass 1 debrief text (not the raw transcript)
- Generates a single combined AE+SE follow-up email draft (collaborative "we" voice, 200-350 words) covering both the business relationship and technical follow-through
- Skipped entirely for `internal-prep` call types

**After both passes**, the script:
- Combines Pass 1 and Pass 2 output into a single Obsidian note with enhanced frontmatter (call-type, participants, meddpicc-score, prior-debrief)
- Prints the Slack summary block to stderr for easy copy-paste
- Appends a Call Log entry to the existing account-research brief (if one exists)
- Prints the output file path to stdout

## Usage

```bash
python3 <skill-path>/scripts/analyze_transcript.py /path/to/call.vtt --account "NetApp"
python3 <skill-path>/scripts/analyze_transcript.py /path/to/call.txt --account "Deel" --date 2026-03-05
```

Replace `<skill-path>` with: `/Users/craigverzosa/.claude/skills/analyze-transcript`

## Invocation

Parse the user's request to extract:
1. **Transcript source** (required — one of the following):
   - A **file path** to a VTT or TXT transcript file
   - **Pasted text** directly in the conversation (the user copies the transcript into the prompt window)
2. **Account name** (required — infer from context if user says "analyze this Deel call")
3. **Date** (optional — defaults to today)

**Detecting pasted text vs. file path:**
- If the user provides a path ending in `.vtt` or `.txt` → use the file path directly
- If the user pastes raw transcript text in their message (no file path, just conversation content) → save it to a temp file first using the Write tool: `/tmp/{account-slug}-transcript.txt`, then pass that path to the script
- If ambiguous, check if the text looks like a file path or like transcript content (speaker turns, dialogue)

Then dispatch:

```
Task tool (Bash subagent, model: "sonnet"):
  prompt: |
    Run: python3 /Users/craigverzosa/.claude/skills/analyze-transcript/scripts/analyze_transcript.py "{FILE_PATH}" --account "{ACCOUNT}" [--date "{DATE}"]
    Report the output path from stdout and any errors from stderr.
```

## After Running

1. Report the debrief file path
2. Summarize conversationally:
   - Call type detected (e.g., "discovery", "demo", "internal-prep")
   - MEDDPICC overall score (e.g., "62% — Metrics and Champion are green; Economic Buyer and Decision Criteria need work")
   - Key findings: top pain points, competitive signals, relationship map highlights
   - Action items by role (`[SE]`, `[AE]`, `[CSM]`, `[TEAM]`)
3. Note if a delta report was generated (i.e., a prior debrief was found and compared) or if this was the first recorded call for the account
4. Mention that the Slack summary was printed to stderr and is ready to copy-paste into the team channel
5. Note if the combined AE+SE follow-up email draft was generated and appended to the debrief, or confirm it was skipped (internal-prep calls skip email drafts by design)
6. Mention if the Call Log was integrated into an existing account-research brief

## Output Location

- Debriefs: `~/Documents/ObsidianNotes/Claude-Research/call-debriefs/{account-slug}-{YYYY-MM-DD}.md`
- Account integration: Appends `## Call Log` entry to existing account brief

## Dependencies

- Python 3 with `anthropic` (auto-installed if missing)
- Credentials in `~/.claude-litellm.env` (ANTHROPIC_AUTH_TOKEN + ANTHROPIC_BASE_URL)
- Obsidian vault at `~/Documents/ObsidianNotes/`
