---
name: session-analyst
description: Analyze Claude session history to surface usage patterns, skill gaps, and recommendations for new skills to build. Reads last 90 days of sessions and generates a full report via extended thinking synthesis. Saved to Obsidian.
triggers:
  - /session-analyst
  - analyze my claude usage
  - session analysis
  - usage patterns
  - what skills should I create
---

# Session Analyst

Analyze Claude session history, surface usage patterns, and recommend new skills to build.

## Steps

### Step 1: Run the collector script

Run the Python data collector:

```bash
python3 ~/.claude/skills/session-analyst/collector.py
```

Capture the JSON output. If the script errors, check that `~/.claude/history.jsonl` exists.

### Step 2: Dispatch synthesis subagent

Use the Task tool to dispatch a general-purpose subagent with `model: "sonnet"` and the following prompt (replace `[COLLECTOR_JSON]` with the full JSON output from Step 1).

---

You are a Claude usage analyst. Analyze the following session data collected from a real user's Claude Code history and produce a structured insight report.

**Session Data:**
```json
[COLLECTOR_JSON]
```

**Note on data precision:** `prompt_samples` is capped at 500 entries (most recent). Day-of-week and time-of-day distributions are sample-based approximations, not full-population counts. Caveat your analysis accordingly.

Produce a report with these exact sections:

## Usage Overview
- Total sessions, prompts, active days in the window
- Prompts per day average
- Sessions per week trend (derived from session timestamps — note this is approximate)
- Top 5 projects by prompt count (with category)
- Most active day of week and time of day (derived from prompt timestamps — sample-based)

## Task Taxonomy
Classify the prompt_samples into categories. Use the prompt text to infer intent. Suggested categories: account-prep, UI-building, debugging, writing-docs, research, skill-creation, data-analysis, demo-building, personal. Show each category as a percentage of total classified prompts. List 2-3 example prompts per category.

## Skill Usage Audit
- Top 5 skills by invocation count (from skill_usage)
- Skills in installed_skills that appear 0 times in skill_usage — list them as "Installed but unused"
- Slash commands used frequently that don't match any installed skill — flag as potential skill gaps

## Repetition Detection
Scan prompt_samples for prompts with similar intent that appear 3+ times without a matching skill. Group into clusters. For each cluster: what is the repeated task, how many times, what project context.

## Skill Recommendations
Based on the above analysis, recommend 3–7 skills to create. For each:
- **Name**: kebab-case skill name
- **Trigger**: the phrase(s) that would invoke it
- **Automates**: what it would do
- **Evidence**: which prompt clusters or patterns surfaced this
- **Complexity**: simple | medium | complex

Be specific. "A skill that preps for account calls" is not useful. "A skill that reads an account name, pulls the Obsidian account brief, checks for recent competitive intel, and outputs a 5-point call strategy" is useful.

---

### Step 3: Save to Obsidian

Use the mcp__obsidian__write_note tool to save the report:

- **Path**: `Claude-Research/usage/YYYY-MM-DD-session-analysis.md` (use today's date)
- **Frontmatter**:
```yaml
date: YYYY-MM-DD
tags: [usage-analysis, claude, meta]
source: claude-code
project: meta
window: last-90-days
```
- **Content**: the full report from Step 2

If the Obsidian write fails (MCP tool unavailable or vault not found), save the report to `~/Desktop/YYYY-MM-DD-session-analysis.md` as a fallback and tell the user which path was used.

### Step 4: Print to terminal

Print the full report inline so the user can read it immediately.

Tell the user: "Report saved to `Claude-Research/usage/YYYY-MM-DD-session-analysis.md` in Obsidian."
