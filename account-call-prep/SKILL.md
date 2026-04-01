---
name: account-call-prep
description: "Pre-call preparation that aggregates all known context about an account and generates a structured call strategy. Reads Obsidian account notes, recent call debriefs, mem0 stored facts, and the Vercel dashboard data to produce a comprehensive pre-call brief with talk track angles, discovery questions, competitive positioning, and recommended approach. Use whenever the user says 'prep for [account] call', 'brief me on [account]', 'get me up to speed on [account]', 'what do I know about [account]', 'call prep for [account]', 'what should I ask in the [account] call', or any request to prepare for a customer meeting. Also trigger when the user mentions having a call coming up with a specific account. Do NOT use for initial account research (use account-research), building a dashboard (use account-dashboard-build), or post-call updates (use call-to-dashboard)."
---

# Account Call Prep

Aggregate all known context about an account and generate a structured call strategy before a customer call.

## Step 1: Identify the account

Extract from the user's prompt:
- **Account name** (required) — normalize to title case for display, lowercase-hyphenated for file paths (e.g., "Robinhood" → `robinhood`)
- **Call type** (optional) — discovery, demo, architecture review, QBR, renewal, follow-up, executive alignment, etc. Default to "call" if unspecified
- **Specific topics or people** (optional) — any individuals, products, or themes the user explicitly mentions wanting to focus on

## Step 2: Gather context (parallel where possible)

Run all five data-gathering steps concurrently. Treat missing sources as non-fatal — skip gracefully and note what was unavailable.

### 1. Obsidian account folder
Search and read all notes under `Claude-Research/accounts/{account-slug}/`:
- Account briefs and overviews
- People / stakeholder profiles
- Previous call debriefs
- Competitive intel specific to this account
- Any ad-hoc notes

Use the `mcp__obsidian__list_directory` tool on `Claude-Research/accounts/{account-slug}/` first, then read each file found.

### 2. Obsidian call debriefs
Search `Claude-Research/call-debriefs/` for recent files mentioning this account name. Use `mcp__obsidian__search_notes` with the account name as query, limited to that folder path. Read the 2-3 most recent matches.

### 3. mem0 facts
Call `memory_search` with query `"{account} account"` (user_id: craig). Also search `"{account} stakeholders"` and `"{account} technical"` to catch fragmented facts. Collect all returned memories.

### 4. Dashboard data file
If a Vercel dashboard project exists for this account, the data file is typically located at one of:
- `/Users/craigverzosa/Documents/Projects/{account-slug}-dashboard/data/account-data.json`
- `/Users/craigverzosa/Documents/Projects/{account-slug}-dashboard/src/data/accountData.ts`
- `/Users/craigverzosa/Documents/Projects/{account-slug}/data/`

Check these paths. If found, read the file and extract: call history, talk track, competitive intel, open items, and deal status.

### 5. Competitive context
Call `mcp__obsidian__search_notes` for any notes in `Claude-Research/competitive-intel/` that reference competitors mentioned in the account notes. Read any matching files.

## Step 3: Synthesize the call prep brief

Using all gathered context, produce the following structured brief. Omit sections where no data exists rather than leaving them blank. Mark any field as "Unknown — ask on call" if it is a known gap worth surfacing.

```
# {Account} — Call Prep ({YYYY-MM-DD})

## Call Context
- **Type:** {discovery / demo / architecture review / QBR / renewal / etc.}
- **Known attendees:** {names, titles, and roles if known}
- **Last interaction:** {date and summary of most recent debrief or call note}
- **Focus topics for this call:** {from user's prompt, or inferred from open threads}

## Account Status
- **Deal stage / current state:** {e.g., active eval, POC, renewal negotiation, expansion}
- **Products of interest:** {Workforce Identity, Customer Identity, PAM, etc.}
- **Key technical requirements:** {SSO, MFA, SCIM provisioning, SIEM integration, etc.}
- **Open questions from prior calls:** {unanswered questions, pending items}

## Call Strategy

### 1. Opening
How to frame this call based on where the relationship stands. One or two sentences to reestablish context and set the agenda.

### 2. Discovery angles
3–5 targeted questions, each tied to a specific knowledge gap:
- Q1: {question} — *Why ask: {what gap this fills}*
- Q2: {question} — *Why ask: {what gap this fills}*
- Q3: {question} — *Why ask: {what gap this fills}*
(add more if warranted)

### 3. Talk track
Key points to make in this call, with supporting evidence or proof points:
- Point 1: {claim or positioning statement} — *Evidence: {data point, customer story, or benchmark}*
- Point 2: …
- Point 3: …

### 4. Demo moments (if applicable)
What to show, in what order, and why each moment matters:
- Show: {feature/flow} — *Because: {what business problem it addresses for this account}*

### 5. Competitive positioning
What we know about competitor presence at this account, and how to respond:
- Competitor: {name} — *Their angle: {pitch}* — *Our counter: {positioning}*
- Topics to avoid or handle carefully: {if any}

## Stakeholder Map
| Name | Title | Cares about | Last contact | Notes |
|------|-------|-------------|--------------|-------|
| {name} | {title} | {priorities} | {date} | {anything notable} |

People we still need to meet:
- {role or name} — *Why important: {reason}* — *Path to get there: {champion, org chart, etc.}*

## Risk & Objection Prep
- **Objection:** {likely objection} — **Response:** {prepared answer}
- **Objection:** {likely objection} — **Response:** {prepared answer}
- **Deal risks:** {timeline slippage, champion turnover, budget freeze, etc.}

## Action Items Going In
What was committed to last time, and whether it was delivered:
- [ ] {commitment} — Status: {done / pending / overdue}

What we are bringing to this call:
- {e.g., POC findings, custom demo, pricing proposal, reference intro}
```

## Step 4: Print and save

1. Print the full brief to the terminal.
2. Save to Obsidian automatically at `Claude-Research/accounts/{account-slug}/call-prep-{YYYY-MM-DD}.md`.
   Include YAML frontmatter:
   ```yaml
   ---
   date: {YYYY-MM-DD}
   tags: [call-prep, account/{account-slug}]
   source: claude-code
   project: {account-slug}
   call_type: {type}
   ---
   ```
3. Report the saved path to the user.

## Behavior notes

- When context is thin (new account, sparse notes), say so explicitly and weight the brief toward discovery questions rather than assertions.
- When context is rich, prioritize recency — debrief from last week beats account brief from six months ago.
- Do not hallucinate contacts, deal stages, or technical requirements. Every fact in the brief must trace back to a source (Obsidian note, mem0, dashboard file). Flag gaps as gaps.
- If the account slug does not match any Obsidian folder, check for close matches (e.g., "databricks" vs "Databricks-Inc") before giving up.
- Call type heavily influences which sections to emphasize: discovery calls → discovery angles; demos → demo moments; renewals/QBRs → deal risks and action items.
