---
name: tone-sync
description: Voice analysis — sample outbound Slack + email, run the tone extraction prompt, produce or update output/_user/tone.md. Use when "update my tone", "tone sync", "refresh voice profile", "learn my voice", "calibrate tone".
version: 1.1
conversation_contract: exempt
council_gate: exempt
---

# Tone Sync — Voice Profile Extraction

Target: $ARGUMENTS

You analyze the user's outbound Slack and email to produce or update
`output/_user/tone.md`, a voice-replication specification that other
skills read during Phase 0 when drafting content in the user's voice.

The extraction methodology is embedded inline in this skill (see
**Extraction Methodology** section below). No external files are required.

This skill is **exempt** from the 4-phase conversation contract.
This skill is **exempt** from the council gate.

## Core Principles

1. **Never fabricate samples.** If MCPs fail or return empty, stop and
   report. Do not guess at voice patterns.
2. **Respect the living-document contract.** If `tone.md` exists, produce
   a delta update, not a rewrite. Preserve the existing version's update log.
3. **Do not smooth.** Typos, lowercase-i, casual punctuation — these are
   voice signatures, not noise. Preserve them in calibration samples.

## Argument Parsing

| Input | Action |
|-------|--------|
| (empty) | Default delta mode — sample last 30 days, update existing tone.md |
| `full` or `rebuild` | Full re-run — sample last 90 days, regenerate tone.md from scratch |
| `<N>d` (e.g. `60d`, `14d`) | Sample last N days. Delta if tone.md exists, fresh if not |
| `check` | Read-only — report sample counts available without running analysis |
| `show` | Display current tone.md without re-running |

---

## Execution Flow

### Step 0 — Preflight

**Resolve user identity** — call `mcp__slack__slack-slack_read_user_profile`
with no arguments to get the current user's profile. Extract:
- `display_name` or `real_name` → user's name
- `user_id` → Slack user ID for sample queries

If the Slack profile call fails, fall back to context from CLAUDE.md
(e.g., "Craig", role "Okta SE") and note the gap. The Slack user ID
`U03FZQJMG1F` is the hardcoded fallback if the API is unavailable.

**Check MCPs:**
- Slack MCP: call `mcp__slack__slack-slack_search_channels` with a test
  query. If unauthorized, warn and skip Slack samples (do not stop).
- Google Workspace MCP: call `mcp__google__google-list_calendars` as a
  probe. If unauthorized or unavailable, warn and skip email samples
  (do not stop).

**Check existing output:**
- Read `output/_user/tone.md` if it exists — determines delta vs. full mode.

If *both* MCPs are unavailable, stop: "Both Slack and Gmail MCPs
unavailable. Cannot produce a reliable tone profile. Run /mcp to
authorize, then re-run /tone-sync."

If only one MCP is available, proceed with reduced corpus and flag the gap
in Open Questions.

### Step 1 — Resolve mode and time window

- Parse `$ARGUMENTS` per the table above → `mode` + `window_days`
- If mode=delta and `output/_user/tone.md` does not exist → auto-upgrade
  to full mode, announce to user.
- If mode=full and `output/_user/tone.md` exists → confirm: "Full rebuild
  will regenerate tone.md from scratch. Continue?" Proceed only on yes.

### Step 2 — Pull samples

Announce: "PULLING SAMPLES — Slack (channels + DMs) and email, last <N> days."

#### Email samples (if Google MCP available)

```
query: from:me after:<YYYY/MM/DD> -subject:"Invitation:" -subject:"Accepted:"
       -subject:"Declined:" -subject:"Canceled:" -subject:"Tentative:"
       -subject:"Updated invitation"
page_size: 50
```

Fetch full content in batches of ≤20. Strip calendar boilerplate and
messages with no authored content above the signature line.

Target: 25–40 authored emails, roughly balanced external vs. internal.

#### Slack channel samples (if Slack MCP available)

`mcp__slack__slack-slack_search_public_and_private` with
`channel_types: public_channel,private_channel`,
`from:<slack_user_id> after:<YYYY-MM-DD>`. Pull 30–50 results.

#### Slack DM samples (if Slack MCP available)

`mcp__slack__slack-slack_search_public_and_private` with
`channel_types: im,mpim`, same author filter. Pull 30–50 results.

If >60% of DMs are with a single person, expand window or add a secondary
query to balance across recipients.

#### Minimum thresholds

- Email: min 10, target 25
- Slack channels: min 15, target 40
- Slack DMs: min 15, target 40

If below minimum: expand time window by 30 days and retry once, or proceed
with reduced confidence (noted in Open Questions).

If total corpus < 20 messages across all channels, do not run the
extraction. Report count and suggest expanding the window.

### Step 3 — Classify and deduplicate corpus

1. **Strip noise** — quoted reply chains (below `On <date>, <name> wrote:`),
   email signatures, Zoom/Teams boilerplate, calendar auto-generated text.
2. **Deduplicate** — repeated sign-offs or boilerplate count once.
3. **Tag each sample:**
   - `channel`: email-external | email-internal | slack-channel | slack-dm
   - `date`: ISO date
   - `purpose`: debrief | ask | commit | acknowledge | logistics | decline | announce | social
   - `audience`: external-customer | internal-peer | internal-senior | dm-partner

### Step 4 — Run the extraction (methodology inline below)

Assemble the input block, then execute the **Extraction Methodology**
section of this skill. Follow all 9 phases in order. Do not skip quality gates.

```
[CORPUS]
<all tagged samples, grouped by channel>

[EXISTING TONE.MD]
<contents of output/_user/tone.md if it exists — omit if not>

[USER CONTEXT]
Name: <from Slack profile or CLAUDE.md fallback>
Role: <from CLAUDE.md — e.g., Okta SE, Enterprise West>
Slack user_id: <resolved in Step 0>
Bilingual: <detect from corpus — presence of non-English>
Common recipients: <top 5 from Slack DMs and email To: fields>
```

### Step 5 — Version + back up + write output

1. Versioning:
   - First run → `1.0.0`
   - Delta, no contradictions → bump minor (e.g., `1.1.0`)
   - Delta with contradictions/deprecations → bump major
   - Full rebuild → bump major

2. If `output/_user/tone.md` exists:
   - Back it up to `output/_user/.tone-archive/tone-v<version>-<YYYY-MM-DD>.md`
   - Create `.tone-archive/` if needed.

3. Write the new `output/_user/tone.md` per the Output Specification below.

4. For delta runs, also write
   `output/_user/.tone-archive/delta-<YYYY-MM-DD>.md` as an audit trail.

### Step 6 — Report to user

```
TONE SYNC COMPLETE — v<new-version>

Samples analyzed:
  - Email: <N> (external: <N>, internal: <N>)
  - Slack channels: <N>
  - Slack DMs: <N>

Changes vs v<prior>:
  - CONFIRMED: <N rules>
  - EXTENDED: <N rules>
  - NEW: <N rules>
  - CONTRADICTED: <N rules> ⚠ needs your review
  - DEPRECATED: <N rules>

Calibration corpus: <N> verbatim samples across <N> register cells

Open questions (under-sampled areas):
  - <bullet list>

Next recommended sync: <30 days for delta / 90 days for full>

Output: output/_user/tone.md
```

If CONTRADICTED rules surfaced, list them and ask: "Are these genuine voice
shifts, or noise from thin sampling? Confirm each."

### Step 7 — Update tracking

1. Append to `output/.analytics/usage.jsonl`:
   `{ts, skill: "tone-sync", output_path: "output/_user/tone.md", account_status: "n/a"}`

2. If full rebuild, append to `output/.todos/global-actions.md`:
   `- [ ] Test tone.md v<new-version> on next content-drafting skill run.`

---

## Extraction Methodology

Execute these 9 phases against the assembled corpus + context block.

### Phase 1 — Structural patterns

For each register (email-external, email-internal, slack-channel, slack-dm),
measure and document:

- **Sentence length:** Typical word count per sentence. Note if short/punchy
  vs. elaborate/multi-clause.
- **Message length:** Typical paragraph or message length. One-liners vs.
  multi-paragraph.
- **Opening patterns:** How does the author typically start? (Salutation,
  direct statement, question, acknowledgment?)
- **Closing patterns:** Sign-offs, calls to action, or just stopping cold?
- **List vs. prose:** Does the author prefer bullets or flowing text?
- **Capitalization:** Standard title caps? Sentence case? Casual lowercase?

### Phase 2 — Linguistic fingerprints

Identify recurring micro-patterns across the full corpus:

- **Punctuation signature:** Em dash, ellipsis, Oxford comma, exclamation
  frequency, question marks as soft hedges.
- **Hedging vs. directness:** How often does the author hedge ("maybe",
  "I think", "could be") vs. assert ("do X", "this is", "we need")?
- **Filler/transition phrases:** Recurring connectors or softeners
  (e.g., "anyway", "honestly", "yeah", "so", "look").
- **Formality markers:** Contractions, slang, technical jargon density.
- **Emoji/reaction style:** None, minimal, expressive — and which ones recur?

### Phase 3 — Register separation

Document how voice shifts *across* registers. The goal is to capture the
delta — what changes from email-external to slack-dm, for example. Key axes:

- Formality level (1–5 scale, 1=most casual)
- Sentence length (short / medium / long)
- Hedging frequency (low / medium / high)
- Emoji use (none / rare / moderate)
- Typical message length

Produce a register matrix: one row per register, one column per axis.

### Phase 4 — Signature phrases and vocabulary

Pull 3–5 verbatim examples per register that best illustrate the voice.
These become the calibration corpus in tone.md. Criteria:
- Representative of typical length and tone
- Show real vocabulary choices (not sanitized)
- Cover different purposes (ask, commit, debrief, social)

Do not invent or clean up examples. Use exact text from the corpus.

### Phase 5 — Voice rules

Synthesize findings into 8–15 named rules. Each rule must:
- Have a short, memorable name (e.g., "Direct opener", "Low hedge", "DM terse")
- State the observed pattern in one sentence
- Note which registers it applies to
- Be backed by ≥2 corpus samples (cite by date/channel)

Format:

```
RULE: <name>
Applies to: <registers>
Pattern: <one sentence>
Evidence: <2+ sample citations>
```

### Phase 6 — Contradictions and gaps

Before writing output:

1. Scan all rules for contradictions against the corpus. A contradiction is
   a sample that clearly violates a stated rule. List each.
2. Identify under-sampled registers (< minimum threshold). Note which
   dimensions are weakly supported.

### Phase 7 — Delta comparison (delta mode only)

If `[EXISTING TONE.MD]` was provided, compare new findings against each
existing rule:

- **CONFIRMED:** New corpus supports the existing rule.
- **EXTENDED:** New corpus adds nuance or new evidence to the rule.
- **NEW:** Rule not present in existing tone.md.
- **CONTRADICTED:** New corpus conflicts with the existing rule.
- **DEPRECATED:** Rule no longer supported by recent corpus (e.g., behavior
  seems to have changed, or was based on thin evidence).

### Phase 8 — Quality gates

Before finalizing, verify:

1. Every rule has ≥2 supporting samples cited.
2. No fabricated examples — all calibration samples are verbatim from corpus.
3. Registers are kept separate — no blending of email-external and slack-dm
   rules unless the behavior genuinely holds across both.
4. Contradictions are documented, not hidden.
5. Under-sampled areas are flagged in Open Questions.

If any gate fails, revise before proceeding.

### Phase 9 — Write output per Output Specification

---

## Output Specification

`output/_user/tone.md` must follow this structure exactly:

```markdown
---
version: <semver>
last_updated: <YYYY-MM-DD>
sample_window: <N days>
corpus_size:
  email_external: <N>
  email_internal: <N>
  slack_channel: <N>
  slack_dm: <N>
---

# Voice Profile: <Name>

## Role & Context
<Name, role, territory — from USER CONTEXT block>

## Register Matrix

| Register | Formality | Sentence length | Hedging | Emoji | Msg length |
|---|---|---|---|---|---|
| email-external | | | | | |
| email-internal | | | | | |
| slack-channel | | | | | |
| slack-dm | | | | | |

## Voice Rules

<rules in RULE format from Phase 5>

## Calibration Corpus

### email-external
<3–5 verbatim samples with date and purpose tag>

### email-internal
<3–5 verbatim samples>

### slack-channel
<3–5 verbatim samples>

### slack-dm
<3–5 verbatim samples>

## Open Questions
<under-sampled areas, contradictions flagged for user review>

## Update Log
- <YYYY-MM-DD> v<X.Y.Z>: <what changed — "Initial run" / "Delta: N confirmed, M new">
```

---

## Do Not

- Fabricate signature phrases or examples.
- Merge registers to make tone.md shorter — register separation is required.
- Run this skill on an account; it is user-level only.
- Trigger the council gate even in error cases.

## Last Updated

- 2026-04-28: Initial skill.
- 2026-05-06: Embedded extraction methodology inline; replaced profile.md
  dependency with Slack API auto-discovery; removed hard stop on missing
  references file.
