---
name: obsidian-save-research
description: Save the current conversation's research, analysis, or output to the correct Obsidian vault location with proper frontmatter, tags, and wiki-links. Automatically determines the right folder path based on project context and content type — no manual path specification needed. Use this skill whenever the user says "save to obsidian", "save this to my notes", "write to obsidian", "add to my vault", "save this research", "save this for [account/topic]", "make sure this is in obsidian", or any request to persist the current work as an Obsidian note. Also trigger when the user finishes a research task and mentions wanting to keep the output. Do NOT use for vault organization/cleanup (use organize-vault), reading existing notes, or bulk vault operations.
---

## What this skill does

Determines the correct Obsidian vault path, generates proper frontmatter, formats the content, and saves — eliminating the manual "where should I put this?" step that causes 363+ note-move operations per month.

## Steps

### Step 1: Determine what to save

Look at the current conversation and identify the saveable output. This could be:
- A research brief or deep-research result
- An analysis or synthesis (competitive intel, market trends, etc.)
- A call debrief or meeting notes
- A strategy document or talk track
- Personal coaching output (LinkedIn review, career advice)
- Financial/stock research
- Any other structured output the user wants to keep

If it's not clear what to save, ask the user: "What from this session should I save? The [X] or the [Y]?"

### Step 2: Determine the path

Use this routing logic based on project context and content type:

| Context Signal | Target Path |
|---|---|
| Working in an account project (Accounts/*) | `Claude-Research/accounts/{account-name}/{topic}.md` |
| Call debrief or transcript analysis | `Claude-Research/call-debriefs/{account}-{date}-debrief.md` |
| Competitive intel or battlecard | `Claude-Research/competitive-intel/{vendor}.md` |
| Stock or investment research | `Claude-Research/stocks/{ticker}-{date}.md` or `Claude-Research/investments/{topic}.md` |
| Crypto research | `Claude-Research/crypto/{coin}-{date}.md` |
| Career or coaching content | `Claude-Research/career/{topic}.md` |
| Personal wellness/health | `Claude-Research/wellness/{topic}.md` |
| Person research | `Claude-Research/accounts/{company}/people/{name}.md` or `Claude-Research/coaching/{name}-brief.md` |
| SE/Gong analysis | `Claude-Research/SE-Gong/{topic}.md` |
| Market trends | `Claude-Research/market-trends/{topic}.md` |
| Design research | `Claude-Research/Design/{topic}.md` |
| Identity/security protocols | `Claude-Research/identity-protocols/{topic}.md` |
| General/unclear | Ask: "I'm not sure where to file this — is this for an account, a project, or personal topic?" Then route based on the answer. |

**Path resolution rules:**
- Always use kebab-case for file names
- Use today's date prefix (YYYY-MM-DD) when the content is time-sensitive (debriefs, market updates, daily research)
- Skip date prefix for evergreen content (battlecards, person profiles, protocol docs)
- If the user explicitly specifies a path, use it — don't override
- Check if a note already exists at the target path using `mcp__obsidian__search_notes`

### Step 3: Format the content

**Generate frontmatter:**
```yaml
---
date: YYYY-MM-DD
tags: [auto-generated-based-on-content-type]
source: claude-code
project: {inferred-from-working-directory-or-context}
---
```

Tag generation rules:
- Always include the content type: `research`, `debrief`, `competitive-intel`, `person-research`, `investment`, etc.
- Include the account name if applicable
- Include topic tags (2-3 max, relevant to content)

**Add wiki-links:**
- Scan for mentions of other notes that likely exist (account names, person names, competitor names)
- Add `[[wiki-links]]` for cross-references where appropriate
- Link to the parent account note if this is an account sub-document

**Content formatting:**
- Ensure proper markdown headings (H1 for title, H2 for sections)
- If saving a conversation excerpt, clean up conversational artifacts
- Keep the content substantive — don't save "here's what I found" wrapper text

### Step 4: Save to Obsidian

**If the note is new:** Use `mcp__obsidian__write_note` with mode `overwrite`.

**If a note already exists at that path:** Use `mcp__obsidian__write_note` with mode `append`, adding a dated section header:
```
---
## Update — YYYY-MM-DD
[new content]
```

### Step 5: Confirm to user

Print:
- The path where the note was saved
- The tags applied
- Any wiki-links created
- If appended to existing, note that it was appended (not overwritten)
