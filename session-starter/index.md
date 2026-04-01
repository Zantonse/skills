---
name: session-starter
description: Auto-load context at session start to eliminate cold-start overhead. Checks for handover notes, reads project plan files, queries mem0 for relevant stored facts, and scans Obsidian for recent research — then provides a concise context summary so the session starts warm instead of cold. Use this skill at the beginning of any session where the user says "continue where we left off", "pick up from last session", "what were we working on", "continue from handover", "resume work", or any indication they're continuing previous work. Also trigger when the user starts a session in a project directory that has a HANDOVER.md file. Proactively suggest using this skill when a session begins with multiple Read calls or clarifying questions that suggest cold-start context gathering. Do NOT use for generating a handover note (use handover), or for researching a new topic from scratch.
---

### Step 1: Scan for context sources
Check these locations in order (parallel where possible):

1. **HANDOVER.md**: Look in the current working directory and one level up for HANDOVER.md. This is the primary context source — it contains what was done last session, what's pending, and current state. If multiple HANDOVER.md files exist in parent directories, prefer the one in the current working directory. If none is in cwd, walk up one level only — do not recurse further.

2. **Project plan**: Check for plan.md, PLAN.md, or .planning/ directory. Read the current phase/task status.

3. **Project CLAUDE.md**: Check for a project-level CLAUDE.md with project-specific instructions (not the global ~/.claude/CLAUDE.md which is already loaded).

4. **mem0 context**: Query mem0 with the project name or account name to retrieve stored decisions, preferences, and facts relevant to this project.

5. **Recent Obsidian notes**: If this is an account project, search Obsidian for the most recent 2-3 notes in `Claude-Research/accounts/{name}/` to see what research exists.

### Step 2: Synthesize context summary
Produce a concise briefing (aim for under 500 words — the goal is to warm context, not overwhelm it):

```
## Session Context — {Project Name}

### Last Session
- What was done (from HANDOVER.md)
- What was left pending
- Any blockers or notes

### Current State
- Active plan phase/task (from plan files)
- Key decisions already made (from mem0)
- Recent research available (from Obsidian)

### Ready to Go
- Suggested next action based on what was pending
- Key files/paths you'll likely need
```

### Step 3: Present and proceed
- Print the context summary
- Suggest the most logical next action based on what was pending
- Do NOT ask "what would you like to work on?" — instead propose the next step and let the user redirect if needed

### Important design principles:
- Speed over completeness — this runs at every session start, so keep it fast
- Don't read entire large files — just headers and summaries
- If no HANDOVER.md exists, say so briefly and suggest using /handover at session end. Pair with: /handover to generate the handover note at session end.
- If no context sources are found, just say "Fresh session — no prior context found" and move on
- This skill should feel like a 5-second briefing, not a 2-minute research report
