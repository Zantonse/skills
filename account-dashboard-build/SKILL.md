---
name: account-dashboard-build
description: "End-to-end account dashboard builder. Auto-chains /account-research, /competitive-intel, and /analyze-transcript, then builds a Next.js account strategy site and deploys to Vercel. Adaptive sections based on available data. Use when the user asks to build an account dashboard, prep an account site, create a strategy site for a customer, or wants the full account prep workflow automated. Triggers on: 'build account dashboard', 'account dashboard for [company]', 'prep account site', 'build dashboard for [company]', 'create account strategy site', 'full account prep', or any request combining a company name with dashboard, site, or account prep intent."
---

# Account Dashboard Build

End-to-end agent that researches a company, ingests raw materials, builds a Next.js account strategy site with adaptive sections, and deploys to Vercel.

## Input Parsing

Extract from the user's request:
1. **Company name** (required)
2. **File paths** (optional — PDFs, VTT transcripts, DOCX, PPTX, XLSX, CSV)
3. **Angle/context** (optional — "focus on PAM displacement", "preparing for RFP")

## Phase 1: Research (Auto-Chain)

Run these automatically. Use parallel subagents where possible.

### Step 1.1: Account Research

Dispatch via Task tool (Bash subagent, model: "sonnet"):
```
python3 /Users/craigverzosa/.claude/skills/account-research/scripts/research_account.py "{COMPANY}" --depth deep [--angle "{ANGLE}"]
```
This produces an Obsidian brief at `~/Documents/ObsidianNotes/Claude-Research/accounts/`.

### Step 1.2: Competitive Intel (if competitors detected)

After account-research completes, check the brief for competitor mentions (look for vendor names in the Identity & Security Posture and Competitive Landscape sections).

For the top 2-3 detected competitors, check if battlecards already exist at `~/Documents/ObsidianNotes/Claude-Research/competitive-intel/{vendor-slug}.md`.

If battlecards are missing for key competitors, dispatch quick mode:
```
python3 /Users/craigverzosa/.claude/skills/competitive-intel/scripts/research_competitive.py --mode quick "{VENDOR}"
```

### Step 1.3: Check for Existing Transcript Debriefs

Check `~/Documents/ObsidianNotes/Claude-Research/call-debriefs/{company-slug}-*.md` for any existing debriefs. If found, read them for call insights.

### Step 1.4: Ingest User-Provided Files

If the user provided file paths:
- **PDFs:** Read with the Read tool
- **VTT transcripts:** Run `/analyze-transcript` skill to produce debriefs first, then use findings
- **DOCX/PPTX:** Read with the Read tool
- **XLSX/CSV:** Read and summarize key data points

### Step 1.5: Synthesize

Combine all gathered intel into a mental model of the account:
- Company snapshot + business goals (from account-research)
- Competitive positioning (from competitive-intel battlecards)
- Relationship dynamics (from transcript debriefs)
- Technical details (from user-provided docs)
- Pain points and opportunities (synthesized from all sources)

## Phase 2: Plan (Propose Sections)

Based on available data, propose which sections to include. Present this as a checklist to the user for approval.

### Always Include
- **Account Overview** — Company snapshot, business goals, strategic priorities, tech landscape
- **Competitive Intel** — Comparison vs detected competitors, feature matrix, positioning

### Include If Data Exists
- **Call Strategy** — Include if: transcript debriefs exist OR pain points are clear. Content: discovery questions, hypotheses to validate, personas to engage.
- **Talk Track** — Include if: pain points AND competitive signals exist. Content: narrative flow from opening to value prop to proof points.
- **Demo Flow** — Include if: user provided build guides or demo materials. Content: step-by-step demo plan with talking points.
- **Relationship Map** — Include if: transcript debriefs exist with speaker identification. Content: champions, blockers, decision makers.
- **Discovery Insights** — Include if: transcript debriefs exist. Content: what was learned, gaps, follow-up needed.
- **Deal Intelligence** — Include if: user provided Salesforce data or deal docs. Content: pipeline, timeline, budget signals.

### Present to User
Show the proposed sections with a brief note on what data source feeds each one. Ask: "These are the sections I'll build based on available data. Want to add, remove, or adjust anything?"

Wait for approval before proceeding to Phase 3.

## Phase 3: Build

### Step 3.1: Scaffold

```bash
npx create-next-app@latest {company}-dashboard --typescript --tailwind --app --no-eslint --no-src-dir
cd {company}-dashboard
npm install recharts
```

### Step 3.2: Configure globals.css (Tailwind v4)

**CRITICAL:** Tailwind v4 uses CSS Cascade Layers. Unlayered CSS silently overrides ALL Tailwind utilities. The `globals.css` MUST follow this exact structure:

```css
@import "tailwindcss";

@theme {
  --color-bg: #F7F7F5;
  --color-surface: #FFFFFF;
  --color-border: #E8E6E1;
  --color-text: #1A1A1A;
  --color-text-secondary: #6B6B6B;
  --color-text-muted: #8A8A8A;
  /* ... other tokens ... */
  --font-sans: "DM Sans", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;
}

/* Resets MUST be inside @layer base — bare * {} kills all spacing utilities */
@layer base {
  html { height: 100%; -webkit-font-smoothing: antialiased; }
  body { height: 100%; font-family: var(--font-sans); font-size: 14px; color: #1A1A1A; background: #F7F7F5; }
  ul, ol { list-style: none; }
  a { color: inherit; text-decoration: none; }
  table { border-collapse: collapse; }
}

/* Component classes MUST be in @layer components so TW utilities can override */
@layer components {
  .card { background: #FFFFFF; border: 1px solid #E8E6E1; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
  .section-label { font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #7A7A7A; margin-bottom: 16px; }
  .badge { display: inline-flex; align-items: center; font-size: 11px; font-weight: 500; padding: 2px 8px; border-radius: 4px; }
}
```

**Sidebar layout:** Use `style={{ marginLeft: 240 }}` on `<main>`, NOT `ml-[240px]` (arbitrary TW classes can fail silently).

**Font loading:** Use `<link>` tag in layout.tsx `<head>`, NOT `@import url()` in CSS (causes build warning about @import ordering).

### Step 3.3: Build Pages

For each approved section, create a page or tab component. Follow these principles:
- **Light mode default** with dark mode toggle (per CLAUDE.md)
- **Recharts** for any data visualization (comparison charts, timelines, metrics)
- **Responsive** — desktop and tablet layouts
- **Navigation** — dark sidebar with grouped nav items, light content area
- Each section should be a separate page under `/app/{section-slug}/page.tsx`
- Use `card` CSS class for all content containers, `section-label` for headers, `badge` for status indicators

### Step 3.4: Content Population

For each section, use the synthesized research to populate real content — not placeholder text. The value of this dashboard is that it contains actual account intelligence, not templates.

### Step 3.5: UI Polish

Apply `/frontend-design` skill principles:
- Clean typography, proper spacing
- Data-dense where appropriate (tables, metrics cards)
- Professional aesthetic suitable for internal SE use
- Optional: use `/nano-banana-art` for custom header graphics if the user requests visual flair

### Step 3.6: Local Verification

```bash
npm run dev
```
Verify the site runs locally before deploying. Check each section renders correctly.

## Phase 4: Deploy

### Step 4.1: Git + GitHub

```bash
git init
git add -A
git commit -m "feat: {company} account dashboard"
gh repo create Zantonse/{company}-dashboard --private --source=. --push
```

### Step 4.2: Vercel Deploy

```bash
vercel --prod --scope okta-solutions-engineering
```

URL will be: `{company}-dashboard.vercel.app`

### Step 4.3: Report

Tell the user:
1. The live URL
2. Summary of what sections were built
3. What data sources fed each section
4. Any data gaps (sections that were thin due to missing sources)
5. Suggestions for enriching the dashboard (e.g., "run /analyze-transcript on your next call to add Relationship Map data")

## After the Initial Build

The dashboard is a living document. On subsequent invocations:
- "Update the NetApp dashboard" → re-run research skills, compare new data to existing site, update changed sections
- "Add a transcript to the NetApp dashboard" → run /analyze-transcript, then add Call Strategy/Relationship sections if missing
- "Add demo flow to NetApp dashboard" → user provides build guide PDF, skill builds the new section and redeploys

## Error Handling

- If `/account-research` fails: continue with user-provided files only, note the gap
- If `/competitive-intel` fails for a vendor: skip that competitor's battlecard, note it
- If no data sources produce useful content for a section: drop that section with a note to the user
- If Vercel deploy fails: save the project locally, report the error, suggest manual deploy

## Dependencies

This skill chains other skills. All must be installed:
- `/account-research` at `~/.claude/skills/account-research/`
- `/competitive-intel` at `~/.claude/skills/competitive-intel/`
- `/analyze-transcript` at `~/.claude/skills/analyze-transcript/`
- `/frontend-design` plugin (for UI polish)
- Vercel CLI (`vercel`) installed and authenticated
- Node.js for Next.js project creation
