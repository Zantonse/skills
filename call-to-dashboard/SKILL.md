---
name: call-to-dashboard
description: "Post-call workflow automation — takes a call transcript or debrief notes, extracts key findings (decisions, technical requirements, stakeholders, next steps, competitive signals), updates the account's Vercel dashboard data file with a structured call recap entry, commits, and deploys. Use whenever the user says 'update the dashboard with the call', 'post-call update', 'add transcript findings to the app', 'update [account] with call notes', 'update dashboard data with the call findings', or any request to push call insights into an account's Vercel dashboard. Also trigger when the user pastes a transcript and mentions updating a dashboard or app. Do NOT use for transcript analysis only (use analyze-transcript), or for building a new dashboard from scratch (use account-dashboard-build)."
---

# Call to Dashboard

Post-call workflow that takes a transcript or debrief notes, extracts structured findings, updates the account's Vercel dashboard data file, saves a debrief note to Obsidian, commits, and deploys — all in one pass.

## Step 1: Identify the Inputs

### Transcript or Debrief Content

Determine what the user provided:

- **Pasted transcript text** — raw conversation content in the message. Save to a temp file: `/tmp/{account-slug}-transcript.txt` using the Write tool, then treat as transcript.
- **File path** to a `.vtt` or `.txt` transcript file — use directly.
- **Pre-written debrief or summary** — notes the user already distilled. Use directly as findings, skip extraction.
- If ambiguous, check whether the content looks like raw speaker-turn dialogue (transcript) or structured summary text (debrief).

### Account Name

Infer from:
1. The user's message (e.g., "update the Deel dashboard")
2. The working directory name
3. If not determinable, ask: "Which account is this call for?"

### Dashboard Project Directory

Look for the project in this order:
1. Working directory if it contains a `vercel.json` or `package.json`
2. `~/Documents/Work/Accounts/{account-name}/`
3. `~/Documents/Work/Accounts/{account-name-slug}/`
4. Common variations: lowercase, hyphenated (e.g., `net-app`, `netapp`)
5. If not found, ask the user: "What's the path to the {account} dashboard project?"

---

## Step 2: Extract Findings from Transcript

If **raw transcript** was provided, extract the following. If the user already provided a debrief summary, use it directly and skip this step.

### Extraction Targets

- **Call type** — Detect from content: discovery, demo, architecture review, QBR, renewal, executive briefing, technical deep-dive, internal sync
- **Key decisions made** — Anything agreed upon or resolved during the call
- **Technical requirements discussed** — Stack details, integration needs, environment constraints, scale requirements
- **Stakeholders mentioned** — Name, role/title, what they care about, their position (champion, skeptic, economic buyer, etc.)
- **Action items** — Split by owner:
  - `[SE]` — Craig's technical follow-ups
  - `[AE]` — Account exec follow-ups
  - `[CUSTOMER]` — Things the prospect/customer agreed to do
  - `[TEAM]` — Shared or unassigned
- **Competitive mentions** — Any competitor names, comparisons, or "we're also looking at X" signals
- **Open questions** — Things that came up but weren't resolved
- **Next steps agreed upon** — Specifically what was committed to before the call ended

---

## Step 3: Find and Update the Dashboard Data File

### Locate the Data File

Search the project for the data file using these common patterns (in order):

1. `src/data/accountData.js`
2. `src/data/accountData.ts`
3. `src/data/dashboardData.json`
4. `src/data/dashboardData.js`
5. `src/lib/data.ts`
6. `src/lib/data.js`
7. `data/*.json`
8. `data/*.js`
9. Any `.json` or `.js` file in `src/` or `data/` that contains keys matching the section names (Account Overview, Call Strategy, Demo Flow, Talk Track, Competitive Intel)

Read the file once found to understand its current structure before modifying.

### Add a New Call Entry

Find the call history or timeline section in the data. Common key names: `callHistory`, `callLog`, `timeline`, `calls`, `recentCalls`, `callDebriefs`. If none exists, add one.

Add a new entry with this structure (adapt the field names to match the existing format):

```js
{
  date: "YYYY-MM-DD",
  callType: "discovery | demo | architecture-review | qbr | renewal | executive-briefing | technical-deep-dive | internal-sync",
  attendees: ["Name (Role)", "Name (Role)"],
  summary: "2-3 sentence plain-language summary of what happened and what was learned.",
  keyFindings: [
    "Finding 1",
    "Finding 2"
  ],
  actionItems: {
    se: ["Action 1", "Action 2"],
    ae: ["Action 1"],
    customer: ["Action 1"],
    team: []
  },
  nextSteps: "What was agreed to happen next, and by when.",
  competitiveSignals: ["Signal 1 if any"],
  openQuestions: ["Question 1 if any"]
}
```

### Update Other Relevant Sections

Beyond the call log, update other sections if the call revealed new information:

- **Competitive Intel** — If a competitor was named or compared, add or update that competitor's entry with the new signal and date
- **Talk Track** — If a new pain point, objection, or angle emerged, add it to the relevant talk track node
- **Demo Flow** — If technical requirements changed (new integration asked about, new environment constraint surfaced), update the demo flow notes
- **Account Overview** — If key facts changed (new stakeholder, updated headcount, budget confirmed/denied), update

Only modify sections where the call produced genuinely new information. Do not pad sections with vague updates.

---

## Step 4: Update Obsidian

Save the structured debrief to Obsidian using the `mcp__obsidian__write_note` tool.

**Path:** `Claude-Research/call-debriefs/{account-slug}-{YYYY-MM-DD}-debrief.md`

**Frontmatter:**

```yaml
---
date: YYYY-MM-DD
tags: [debrief, call-log, {account-slug}]
source: claude-code
project: {account-name}
call-type: {detected-call-type}
attendees: [{name1}, {name2}]
---
```

**Content:** Full structured debrief — call type, attendees and roles, key findings, action items by owner, competitive signals, open questions, next steps, and a link back to the account's main note if one exists (use `[[account-name]]` wiki-link).

If a debrief note already exists at that path (same account, same date), append with a section header `## Update — HH:MM` rather than overwriting.

---

## Step 5: Commit and Deploy

### Git Commit

```bash
git -C {project-dir} add {data-file-path}
git -C {project-dir} commit -m "Update {account} dashboard with {YYYY-MM-DD} call debrief"
git -C {project-dir} push
```

Only stage the data file that was modified — not the entire working tree. This avoids accidentally committing unrelated changes.

### Vercel Deploy

```bash
vercel --prod --cwd {project-dir} --scope okta-solutions-engineering
```

Capture the output to extract the live URL. If the deploy command is not available or fails, report the error and the commit SHA so the user can trigger a deploy manually.

### Deploy Failure Handling

- If `vercel` CLI is not found: report the git commit was successful and ask the user to deploy from the Vercel dashboard
- If deploy fails due to build error: show the error output, do not leave the repo in an inconsistent state
- If push fails (remote ahead): pull first, then push

---

## Step 6: Confirm

Print a concise summary:

```
Call debrief processed for {Account} — {YYYY-MM-DD}

Extracted:
  - Call type: {type}
  - Attendees: {names}
  - Action items: {SE count} SE / {AE count} AE / {customer count} customer
  - Competitive signals: {count or "none"}

Dashboard updated:
  - Call log entry added to {data-file-path}
  - {Other sections updated, if any}

Obsidian note saved:
  - Claude-Research/call-debriefs/{account-slug}-{date}-debrief.md

Deployed:
  - {live Vercel URL}
```

If any step was skipped or failed, call it out explicitly — do not silently omit it from the summary.

---

## Dependencies

- Vercel CLI (`vercel`) — authenticated and scoped to `okta-solutions-engineering`
- Git — project must be a git repo with a configured remote
- Obsidian vault at `~/Documents/ObsidianNotes/` with `Claude-Research/call-debriefs/` subfolder
- `/analyze-transcript` skill — available at `~/.claude/skills/analyze-transcript/` (referenced for extraction logic; not chained directly unless a VTT file is provided)

## Related Skills

- `/analyze-transcript` — Use this instead if you only want the debrief without updating a dashboard
- `/account-dashboard-build` — Use this to build a new dashboard from scratch
- `/obsidian-save-research` — Used internally in Step 4 for vault saves
