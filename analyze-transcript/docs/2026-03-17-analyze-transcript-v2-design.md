# analyze-transcript v2 — Design Spec

> Date: 2026-03-17 | Author: Craig Verzosa + Claude | Status: Approved

## Problem

The current `/analyze-transcript` skill produces SE-centric call debriefs but doesn't serve the broader account team. AEs need deal qualification signals, the team needs actionable follow-ups, and there's no longitudinal view of how an account evolves across calls.

## Goals

1. Auto-detect call type and adapt output structure accordingly
2. Produce MEDDPICC deal qualification scorecards that update cumulatively
3. Generate role-tagged action items ([SE], [AE], [CSM], [TEAM])
4. Generate a copy-paste Slack summary for the team channel
5. Generate a delta report showing what changed since the last call
6. Generate SE and AE follow-up email drafts (separate API call)
7. Support all call types: discovery, demo, roadmap review, QBR, renewal, internal prep, executive briefing, discussion/sync

## Non-Goals

- CRM integration (Salesforce push)
- Audio-to-text transcription (assumes VTT/TXT input)
- Real-time / streaming analysis
- Multi-language transcript support

## Architecture

Two-pass model with a shared Python script:

```
Transcript (VTT/TXT)
    │
    ├── [auto-load most recent prior debrief for same account]
    │
    ▼
Pass 1: Analysis (claude-4-6-sonnet, ~8000 max tokens → increase to 12000)
    │── Call type auto-detection
    │── Structured debrief (enhanced sections)
    │── MEDDPICC scorecard (cumulative if prior exists)
    │── Delta report (vs. prior debrief, if prior exists)
    │── Role-tagged action items
    │── Slack team summary
    │── Discovery quality assessment
    │── Key quotes + metrics
    │
    ▼
Pass 2: Follow-ups (claude-4-6-sonnet, ~4000 max tokens)
    │── Input: Pass 1 debrief text (NOT raw transcript)
    │── SE follow-up email draft
    │── AE follow-up email draft
    │
    ▼
Output:
    ├── Single Obsidian note (all sections)
    ├── Slack block printed to stderr (for easy copy)
    └── Account brief integration (Call Log append)
```

## Call Type Detection

Claude auto-detects from transcript content. No CLI flag required.

| Call Type | Detection Signals | Adaptive Behavior |
|-----------|------------------|-------------------|
| **discovery** | Open-ended questions, pain exploration, "tell me about" | Full MEDDPICC, expanded discovery quality assessment |
| **demo** | "Let me show you", feature walkthrough, screen sharing refs | Add feature resonance tracking, objection capture |
| **roadmap-review** | Product names, EA/GA timelines, "coming in Q2" | Add Interest Heatmap (features × attendee reactions) |
| **qbr** | Metrics, adoption, "since last quarter", renewal refs | Add Adoption Health section with churn/expansion signals |
| **renewal** | Pricing, contract, terms, commercial negotiation | Add commercial risk assessment, competitive leverage |
| **internal-prep** | All speakers are internal, strategy discussion, "for the call" | SKIP MEDDPICC + Competitive. ADD Preparation Strategy (role assignments, talk track, presentation sequencing) |
| **executive-briefing** | C-level attendees, strategic vision, partnership themes | Emphasize relationship mapping, executive sentiment, strategic alignment |
| **discussion-sync** | Status updates, check-ins, "touch base", mixed topics | Balanced output, lighter structure, emphasize anything new/changed |

## Prior Debrief Loading

On each run, the script searches `OBSIDIAN_DEBRIEFS / {account-slug}-*.md`:

1. Sort by filename date descending
2. Load the most recent one within 90 days
3. Extract via regex: executive summary, MEDDPICC scorecard, relationship map, action items
4. Append as `## Prior Debrief Context ({date})` to the user message sent to Claude

Edge cases:
- No prior debrief → skip delta section, note "First recorded call for this account"
- Prior debrief >90 days old → include but flag as potentially stale
- Multiple debriefs → only load the most recent
- Prior debrief is v1 format (missing MEDDPICC, delta, etc.) → graceful degradation: extract only sections that exist, omit missing ones from context, log which sections were found vs. skipped to stderr

## Output Structure

### Enhanced Frontmatter

```yaml
---
date: 2026-03-17
tags: [call-debrief, {account-slug}, {call-type}]
source: claude-code
project: se-accounts
account: {Account}
call-type: {auto-detected type}
participants: ["Alice", "Bob"]  # inline JSON-style list (Python serializes via json.dumps)
meddpicc-score: {0-100}
prior-debrief: {slug-date or null}
---
```

### Section Order

1. **Header + Executive Summary** — Call type badge, 3-4 sentence brief
2. **Slack Summary** — Copy-paste block, <150 words, emoji header (placed early for quick access)
3. **Participants & Roles** — Table with speaker, inferred role, key signals
4. **Discovery Findings** — Pain points (with quotes + business impact), business goals, technical environment
5. **Competitive Signals** — Vendor mentions, existing relationships, displacement opportunities
6. **Relationship Map** — Champions, blockers, decision makers, influencers
7. **MEDDPICC Scorecard** — 8-element table with 🟢/🟡/🔴 status, evidence, gaps, overall percentage
8. **Delta Report** — New stakeholders, shifted priorities, resolved items, new blockers, momentum direction (conditional on prior debrief)
9. **Action Items & Next Steps** — Role-tagged: `[SE]`, `[AE]`, `[CSM]`, `[TEAM]`
10. **Follow-Up Emails** (from Pass 2) — SE draft + AE draft, 150-250 words each
11. **Discovery Quality Assessment** — Strong questions, gaps, talk/listen balance, score
12. **Key Quotes** — Verbatim with speaker attribution and topic
13. **Key Metrics Captured** — Table of quantitative data points

### Adaptive Sections by Call Type

| Section | discovery | demo | roadmap | qbr | renewal | internal-prep | exec-briefing | discussion-sync |
|---------|-----------|------|---------|-----|---------|---------------|---------------|-----------------|
| MEDDPICC | ✅ Full | ✅ | ✅ | ✅ | ✅ | ❌ Skip | ✅ | ✅ Light |
| Competitive | ✅ | ✅ | ✅ | ✅ | ✅ Full | ❌ Skip | ✅ | ✅ |
| Discovery Quality | ✅ Full | ✅ Light | ✅ Light | ✅ Light | ✅ Light | ❌ Skip | ✅ Light | ✅ Light |
| Interest Heatmap | ❌ | ❌ | ✅ Add | ❌ | ❌ | ❌ | ❌ | ❌ |
| Adoption Health | ❌ | ❌ | ❌ | ✅ Add | ✅ Add | ❌ | ❌ | ❌ |
| Preparation Strategy | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Add | ❌ | ❌ |
| Follow-Up Emails | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ Skip | ✅ | ✅ |

## Prompt Files

### `references/debrief-prompt.md` (rewritten)

System prompt for Pass 1. Contains:
- Role definition (senior SE reviewing a call transcript for the full account team)
- Call type classification instructions — Claude must emit exactly `**Call Type: {type}**` as the first line of output (e.g., `**Call Type: discovery**`). Regex: `r'\*\*Call Type:\s*([\w-]+)\*\*'`
- Speaker identification rules (same as current)
- Full report structure with all sections
- Adaptive section instructions keyed to call type
- MEDDPICC scoring rubric (🟢=1, 🟡=0.5, 🔴=0, percentage = sum/8×100). Claude must emit the summary line as exactly `**Overall: {N}%**` (e.g., `**Overall: 62%**`). Regex: `r'\*\*Overall:\s*(\d+)%\*\*'`
- **MEDDPICC Light** (for discussion-sync calls): Include the 8-element table with status and evidence columns only — omit the Gaps column and any delta-vs-prior commentary. Still emit the `**Overall: {N}%**` summary line
- Delta report instructions (conditional on prior context presence)
- Slack summary format constraints (<150 words, emoji header, bullets)
- Action item role-tagging rules
- Guidelines (same spirit as current: specific quotes, business impact, honest assessment)

### `references/followup-prompt.md` (new)

System prompt for Pass 2. Contains:
- Role definition (drafting customer follow-up emails from a structured debrief)
- SE email spec: technical, warm, 150-250 words, propose technical next steps, no commercial language
- AE email spec: relationship-forward, commercially aware, 150-250 words, timeline-oriented next steps, no deep technical detail
- Shared rules: reference 1-2 specific things customer said, single clear CTA, use contact names, ready to send with minimal edits
- Instruction to skip follow-up emails entirely for internal-prep call types (secondary safeguard — primary skip is enforced in Python: `if call_type == "internal-prep": skip Pass 2 entirely`)

## Script Changes (`scripts/analyze_transcript.py`)

### New functions

- `load_prior_debrief(account: str, max_age_days: int = 90) -> Optional[tuple[str, str]]`
  Returns `(date, extracted_context)` or `None`. Searches `OBSIDIAN_DEBRIEFS` for most recent matching file, extracts key sections via regex.

- `generate_followups(debrief: str, account: str, model: str) -> str`
  Second Claude API call using `followup-prompt.md` as system prompt. Input is the Pass 1 debrief text. Returns SE + AE email markdown.

- `extract_call_type(debrief: str) -> str`
  Regex extract of `**Call Type: {type}**` from first line of Pass 1 output.

- `extract_meddpicc_score(debrief: str) -> Optional[int]`
  Regex extract of overall percentage from MEDDPICC section for frontmatter.

- `extract_participants(debrief: str) -> list[str]`
  Extract participant names from the Participants & Roles table for frontmatter.

- `extract_slack_summary(debrief: str) -> str`
  Extract the Slack Summary section content for stderr output.

### Modified functions

- `analyze_with_claude()` — Increase `max_tokens` from 8000 to 12000. Append prior debrief context to user message if available.

- `write_debrief()` — Enhanced frontmatter (call-type, participants, meddpicc-score, prior-debrief). Append Pass 2 follow-up emails to the debrief content before writing.

- `main()` — New flow:
  1. Read + parse transcript (unchanged)
  2. Load prior debrief (new)
  3. Pass 1: analysis call (enhanced prompt + prior context)
  4. Extract metadata (call type, MEDDPICC score, participants)
  5. Pass 2: follow-up email call (new, skip for internal-prep)
  6. Combine Pass 1 + Pass 2 output
  7. Write debrief to Obsidian (enhanced)
  8. Print Slack summary to stderr (new)
  9. Integrate with account brief (unchanged)
  10. Print output path to stdout (unchanged)

### Unchanged

- `parse_vtt()` — No changes needed
- `slugify()` — No changes needed
- `_load_env_file()` — No changes needed
- `_ensure_packages()` — No changes needed
- CLI interface — Same flags: `transcript`, `--account`, `--date`, `--model`

## SKILL.md Updates

Update description to reflect new capabilities:
```
SE account team call debrief from VTT/TXT transcripts. Auto-detects call type
(discovery, demo, roadmap, QBR, renewal, internal prep, executive briefing,
discussion/sync) and produces adaptive structured debriefs with MEDDPICC
scorecards, competitive signals, relationship mapping, role-tagged action items,
call-over-call delta reports, Slack team summaries, and SE/AE follow-up email
drafts. Integrates with existing account-research briefs.
```

Update invocation docs and "After Running" section to mention new outputs (Slack summary, email drafts, MEDDPICC score).

## Token Budget Estimate

- Pass 1 input: ~2000 tokens (system prompt) + transcript (~3000-15000 depending on call length) + prior context (~1500 if present) = ~6500-18500
- Pass 1 output: ~12000 max tokens
- Pass 2 input: ~500 tokens (system prompt) + Pass 1 output (~8000 typical) = ~8500
- Pass 2 output: ~4000 max tokens

Total per run: ~2 API calls, ~30K-45K input tokens, ~16K output tokens. Roughly 2x the current single-call cost.

**Note:** For long enterprise calls (90min, 8+ participants), VTT transcripts can exceed 25K tokens. With prior context + system prompt, Pass 1 input may reach ~28K tokens. This is within claude-4-6-sonnet's context window but worth monitoring. If transcripts consistently exceed 20K tokens, consider truncating to the most recent 80% of the call (early small talk is low-signal).

## Testing

Test with existing transcripts:
1. Deel 2026-03-11 (discovery/business review — has prior debrief to test delta)
2. Databricks internal prep (the tiger team transcript — tests internal-prep type detection)
3. A short discussion/sync transcript (tests lighter output)
