# HANDOVER — analyze-transcript v2

> Date: 2026-03-17 | Location: `~/.claude/skills/analyze-transcript/`

## 1. Session Summary

This session brainstormed, designed, and spec'd a comprehensive v2 upgrade to the `/analyze-transcript` skill. The goal was to transform it from an SE-only call debrief tool into a full account team post-call workflow — adding MEDDPICC scorecards, call type detection, delta reports, Slack summaries, and SE/AE follow-up email drafts. The spec was written, reviewed by a code-reviewer subagent (8 issues found), and all issues were fixed. The spec is approved and ready for implementation. No code has been written yet.

## 2. What Got Done

- **Design spec written and reviewed:** `docs/2026-03-17-analyze-transcript-v2-design.md` — complete spec covering architecture, call type detection, output structure, prompt templates, script changes, and token budget
- **Spec review completed:** Code reviewer found 3 critical, 3 important, 2 suggestion issues. All 8 were fixed in the spec.
- **Databricks roadmap work (earlier in session):** Built a full talk track for Databricks CY26 Q1 roadmap call, added presenter notes to all 87 slides of a PowerPoint, and wrote deep-dive feature reference to Obsidian. This is unrelated to the skill upgrade but consumed most of the session context.

## 3. What Didn't Work / Bugs Encountered

- **WebFetch tool failures:** Throughout the session, `WebFetch` consistently failed with `401 key_model_access_denied` errors (trying to access `claude-haiku-4-5-20251001` which isn't in the allowed model list). Workaround: use `firecrawl scrape` CLI or `litellm_web_search` instead. Subagents need explicit instructions to avoid WebFetch.
- **Firecrawl scraping Okta help docs:** Many Okta help doc URLs return search scaffolding (Coveo search widget) rather than actual content when scraped via Firecrawl. The `/oie/en-us/` URL prefix works better than `/en-us/` for OIE docs. Some pages (ITP, Universal Logout) don't have stable public URLs.

## 4. Key Decisions Made

| Decision | Reasoning |
|----------|-----------|
| **Two-pass architecture** (analysis + follow-ups) | Follow-up emails need a fundamentally different voice (customer-facing) vs. the analytical debrief (internal). Separate API call also means email prompt can be iterated independently. |
| **Auto-detect call type from transcript** | No CLI flag needed. LLM is reliable at classifying from content. Keeps the interface simple. |
| **MEDDPICC over MEDDIC** | Craig's AE team uses the 8-element MEDDPICC framework. |
| **Slack summary at position 2** (after exec summary) | Moved from position 9 per reviewer suggestion. It's a copy-paste artifact — should be immediately accessible. |
| **Prior debrief loaded only within 90 days** | Balances context freshness with availability. Stale context flagged rather than excluded. |
| **Pass 2 skip enforced in Python** | For `internal-prep` calls, skip the API call entirely rather than relying on prompt-level instructions. Saves tokens. |
| **Frontmatter participants as JSON inline list** | `json.dumps()` avoids YAML serialization fragility in f-string construction. |

## 5. Lessons Learned / Gotchas

- **The existing debrief output quality is strong** — the Deel 2026-03-11 debrief (`call-debriefs/deel-2026-03-11.md`) is a good reference for what good output looks like. The v2 prompt should preserve this quality while adding new sections.
- **v1 debriefs won't have MEDDPICC sections** — `load_prior_debrief()` must gracefully handle missing sections when reading v1 format debriefs. The spec now explicitly documents this.
- **Exact regex anchors are critical** — the spec now specifies the exact strings Claude must emit (`**Call Type: discovery**`, `**Overall: 62%**`) with corresponding regex patterns. Without these, metadata extraction silently fails.
- **Craig's LiteLLM proxy is at `llm.atko.ai`** — credentials in `~/.claude-litellm.env`. The script uses `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL`.

## 6. Current State

- **No code changes made** — all existing files are untouched v1
- **Spec is complete and reviewed** at `docs/2026-03-17-analyze-transcript-v2-design.md`
- **No git repo** — the skill directory is not version-controlled
- **Skill is functional** — current v1 works and can be tested at any time

## 7. Clear Next Steps

Implementation order (4 files to change):

1. **Write `references/debrief-prompt.md`** (rewrite) — The expanded Pass 1 system prompt with call type detection, MEDDPICC, delta report, Slack summary, role-tagged action items, and adaptive section instructions. This is the highest-impact change and the most nuanced to get right.

2. **Write `references/followup-prompt.md`** (new) — The Pass 2 system prompt for SE and AE follow-up email generation. Simpler, focused prompt.

3. **Rewrite `scripts/analyze_transcript.py`** — Add: `load_prior_debrief()`, `generate_followups()`, `extract_call_type()`, `extract_meddpicc_score()`, `extract_participants()`, `extract_slack_summary()`. Modify: `analyze_with_claude()` (increase max_tokens to 12000, add prior context), `write_debrief()` (enhanced frontmatter with json.dumps for participants), `main()` (new two-pass flow). Keep unchanged: `parse_vtt()`, `slugify()`, env/package helpers, CLI interface.

4. **Update `SKILL.md`** — New description, updated invocation docs, new "After Running" section mentioning all outputs.

5. **Test** — Run against Deel 2026-03-11 transcript (has prior debrief for delta testing), and the Databricks internal prep transcript (tests internal-prep type detection with MEDDPICC skip).

## 8. Important Files Map

| File | Status | Description |
|------|--------|-------------|
| `docs/2026-03-17-analyze-transcript-v2-design.md` | NEW ✅ | Complete design spec — the implementation blueprint |
| `references/debrief-prompt.md` | TO REWRITE | Current v1 system prompt (3.7KB). Must be rewritten per spec. |
| `references/followup-prompt.md` | TO CREATE | New Pass 2 prompt for SE/AE follow-up emails |
| `scripts/analyze_transcript.py` | TO MODIFY | Current v1 script (10.3KB, 303 lines). Add ~150 lines for new functions + modify existing. |
| `SKILL.md` | TO UPDATE | Current v1 skill definition. Update description + docs. |
| `~/Documents/ObsidianNotes/Claude-Research/call-debriefs/deel-2026-03-11.md` | REFERENCE | Example v1 output — use as quality benchmark |
| `~/Documents/ObsidianNotes/Claude-Research/call-debriefs/deel-2026-03-07.md` | REFERENCE | Earlier Deel debrief — test delta loading against this |
