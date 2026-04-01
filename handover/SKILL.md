---
name: handover
description: Generate a HANDOVER.md shift-change report documenting everything done in this session so the next Claude picks up exactly where we left off. Use whenever the user says "write a handover note", "create a session summary", "document what we did", "end of session wrap-up", "save session state", "what did we accomplish today", or any request to capture the current session's work for the next session to pick up. Pair with /session-starter to load the handover at the start of the next session.
allowed-tools: Read, Glob, Grep, Write, Bash
---

# Handover — Session Shift-Change Report

Generate a `HANDOVER.md` file in the current project root. This is a shift-change report that tells the next Claude (or human) exactly where things stand so nothing gets lost between sessions.

## Process

1. **Review the full conversation history** — look at every message, tool call, and result from this session
2. **Explore the current project state** — check git status, recent commits, modified files, and any failing tests
3. **Write HANDOVER.md** in the project root with the sections below

## Required Sections

### 1. Session Summary
- One paragraph: what was the goal of this session and what was accomplished
- Date and branch name

### 2. What Got Done
- Bulleted list of completed work items with file paths
- For each item: what changed and why

### 3. What Didn't Work / Bugs Encountered
- Problems hit during the session and how they were resolved
- Any workarounds applied that may need revisiting

### 4. Key Decisions Made
- Architecture or design choices and the reasoning behind them
- Trade-offs that were considered

### 5. Lessons Learned / Gotchas
- Surprising behaviors, undocumented quirks, or non-obvious constraints discovered
- Things the next person should know to avoid wasting time

### 6. Current State
- Does it build? Do tests pass?
- Any uncommitted changes?
- Current git branch and latest commit

### 7. Clear Next Steps
- Ordered list of what to work on next
- Include unfinished items from this session
- Note any blockers

### 8. Important Files Map
- Table of key files touched or relevant, with one-line descriptions
- Focus on files that were changed or are central to understanding the work

## Style Guidelines

- Write for a developer who has never seen this project
- Be specific — include file paths, function names, error messages
- Keep it scannable — use headers, bullets, and tables
- No filler or pleasantries — just facts
- If something is uncertain, say so explicitly
