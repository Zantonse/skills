---
name: session-analyst
description: Analyze Claude Code session history to surface usage patterns, workflow inefficiencies, skill gaps, and personalized recommendations. Reads session logs including subagent transcripts, tracks token consumption and tool-chain workflows, and generates an actionable report. Use this skill whenever the user asks about their Claude usage, wants to understand their patterns, asks what skills they should create or install, wants a usage report, mentions session analysis, or says things like "how am I using Claude", "what should I automate", "analyze my sessions", or "usage patterns". Also use when the user wants to optimize their Claude Code setup or reduce wasted tokens.
---

# Session Analyst

Analyze Claude Code session history to surface usage patterns, workflow inefficiencies, and actionable skill recommendations.

## What this skill produces

A structured report covering:
- **Usage overview** — sessions, prompts, active days, token consumption
- **Project breakdown** — where time and tokens are going
- **Task taxonomy** — what kinds of work the user does with Claude
- **Tool workflow patterns** — repeated sequences of tool calls that reveal automatable workflows
- **Skill audit** — which installed skills are actually used, which are gathering dust
- **Subagent analysis** — how delegation is being used (or underused)
- **Session health** — compaction frequency, longest/heaviest sessions
- **Skill recommendations** — specific, evidence-backed suggestions for new skills or better use of existing ones

## Steps

### Step 1: Run the collector

Run the Python data collector. Default is 20 days; the user can request a different window.

```bash
python3 ~/.claude/skills/session-analyst/collector.py --days <N>
```

Capture the JSON output (it prints to stdout; progress info goes to stderr). If the script errors, check that `~/.claude/history.jsonl` exists.

The collector output is large (often 50K+ characters). Do NOT try to paste it all into a single prompt. Instead, save it to a temp file:

```bash
python3 ~/.claude/skills/session-analyst/collector.py --days <N> > /tmp/session-analyst-data.json 2>/tmp/session-analyst-progress.txt
```

Read the progress output to confirm it ran successfully, then read the JSON data file.

### Step 2: Analyze the data yourself

Read `/tmp/session-analyst-data.json` and produce the report. Do not dispatch this to a subagent — you have the full context of the user's skill library and conversation history, which a subagent would lack.

Produce a report with these sections. Be specific and data-driven throughout — cite actual numbers, project names, and tool sequences from the data.

---

## Usage Overview
- Total sessions, prompts, and active days in the window
- Prompts per day average and trend (increasing? decreasing? steady?)
- Total token consumption (input + output) and cache hit rate percentage
- Most active time of day and day of week (from `time_patterns`)
- Average session duration, plus call out the longest and heaviest sessions

## Project Landscape
- Top projects by prompt count, grouped by category
- For each top project: prompts, sessions, active date range, and what category of work it represents
- Highlight any projects that consumed disproportionate tokens relative to prompt count (these suggest complex, long-context work)

## Task Taxonomy
Classify the `prompt_samples` into categories based on prompt text. Use categories that fit the actual data — common ones include: account-prep, UI-building, debugging, writing/docs, research, skill-creation, data-analysis, demo-building, personal-coaching, career, health/wellness, financial-research. Show each as a percentage. List 2-3 example prompts per category.

## Tool Workflow Patterns
This section is the heart of the analysis. Use `workflow_patterns.tool_chain_pairs` and `tool_chain_trigrams` to identify:
- **Dominant workflows**: What are the most common 2-step and 3-step tool sequences? What do they represent? (e.g., `Grep -> Read -> Edit` = find-and-fix pattern; `WebSearch -> WebFetch -> Write` = research-to-notes)
- **Manual repetition signals**: Sequences that appear 10+ times suggest the user is manually orchestrating a workflow that could be automated by a skill
- **Unusual patterns**: Tool sequences that seem inefficient (e.g., many `Bash` calls where specialized tools exist, or `Read -> Read -> Read` chains suggesting exploration that could use `Explore` subagents)

## Skill Usage Audit
- **Active skills**: Top skills by invocation count from `skill_usage`, with how often each was used
- **Installed but unused**: Skills in `installed_skills` that appear 0 times in `skill_usage`. For each, briefly note what it does and hypothesize why it might be unused (wrong trigger description? not relevant to current work? user doesn't know about it?)
- **Slash commands without skills**: Commands in `slash_commands` that don't match installed skills — these might be GSD commands, built-in commands, or gaps
- **Skill trigger efficiency**: If skills are rarely used despite relevant prompts appearing in `prompt_samples`, flag this as a triggering problem

## Subagent Delegation Profile
Using `subagent_analysis`:
- How many subagents were spawned in the window? What types (Explore, general-purpose, Bash, etc.)?
- Are subagents being used for the right things? (Explore for codebase search, general-purpose for research, etc.)
- Token cost of subagent work vs. main session work
- Opportunities: Are there repeated manual workflows in main sessions that should be delegated to subagents?

## Session Health
- **Compaction frequency**: Average compactions per session from `session_health`. High compaction rates (>2 per session) suggest sessions are running too long or context is being used inefficiently.
- **Heaviest sessions**: List the top 3-5 by token usage. What projects were they? Why were they heavy?
- **Longest sessions**: Same for duration. Were these productive or spinning?

## Repetition Detection
Scan `prompt_samples` for prompts with similar intent that appear 3+ times without a matching skill. Group into clusters. For each cluster: what is the repeated task, how many times, what project context.

## Skill Recommendations

Based on ALL of the above analysis, recommend 5-10 skills. Split into two groups:

### Skills to Create (new)
For each:
- **Name**: kebab-case
- **Trigger**: phrases that would invoke it
- **Automates**: specific steps it would perform (be concrete — "reads X, calls Y, outputs Z")
- **Evidence**: which patterns, repetitions, or workflow chains surfaced this recommendation
- **Estimated impact**: how many prompts/sessions per week this would improve

### Skills to Use More (existing but underused)
For each installed-but-unused skill that IS relevant to the user's actual work:
- **Name**: the skill name
- **Why it's relevant**: connect it to specific prompt clusters or task categories from the data
- **How to start**: one concrete example of when to invoke it, based on the user's real prompts

Be concrete throughout. "A skill for account prep" is not useful. "A skill that reads the account name, pulls the Obsidian brief from Claude-Research/accounts/{name}/, checks competitive-intel notes, cross-references recent call debriefs, and generates a 5-point call strategy with talk track" is useful.

---

### Step 3: Save to Obsidian

Use the `mcp__obsidian__write_note` tool to save the report:

- **Path**: `Claude-Research/usage/YYYY-MM-DD-session-analysis.md` (use today's date)
- **Frontmatter**:
```yaml
date: YYYY-MM-DD
tags: [usage-analysis, claude, meta]
source: claude-code
project: meta
window: last-N-days
```
- **Content**: the full report

If the Obsidian write fails, save to `~/Desktop/YYYY-MM-DD-session-analysis.md` as fallback and tell the user.

### Step 4: Print to terminal

Print the full report inline. At the end, tell the user where the Obsidian note was saved.

If the report is very long, it's fine to print a condensed executive summary to the terminal (Usage Overview + Skill Recommendations) and direct the user to the Obsidian note for the full breakdown.
