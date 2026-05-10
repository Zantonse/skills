---
name: o4aa-knowledge-update
description: |
  Refreshes the O4AA knowledge hub (o4aa-knowledge/lib/content/) with the latest field
  intelligence from Okta Slack channels, Atlassian Confluence, and optionally deep research.
  Pulls from #okta-ai-agents-field-feedback, #okta-secures-ai-questions, #a4aa, and
  #presales-o4aa-a4aa-champions, then updates all 41 TypeScript content files additively —
  fixing stale product status, adding new customer evidence, capturing field-confirmed gotchas,
  documenting new competitors and use cases.

  Use this skill whenever the user says "update the o4aa knowledge hub", "refresh the knowledge
  app", "sync the knowledge hub from Slack", "what's new in o4aa since last update", "update the
  field guide", or asks to pull latest Okta AI agent intel into the content files. Also trigger
  when the user says "/o4aa-knowledge-update" or asks to keep the knowledge hub current after
  a period of time has passed. Supports optional section filter:
  --section=foundations|products|auth-flows|developer|operations|se-playbook|reference
---

# O4AA Knowledge Hub Updater

You are updating the O4AA (Okta for AI Agents) knowledge hub — a Next.js app whose content
lives in TypeScript files. You pull the latest field intelligence from Slack, Confluence, and
optionally research, then update content files additively. The hub is an SE reference tool;
accuracy matters more than comprehensiveness. Every update needs a source citation.

## Content Location

All 41 content files live at:
`/Users/craigverzosa/Documents/Work/Okta/O4AA/o4aa-knowledge/lib/content/`

Each file exports a `SectionContent` object with a `cards` array. Updates are **always additive**
— add new cards or paragraphs. Never delete existing content. Never restructure.

## Section Map

Use this when `--section=X` is passed, or to group files for parallel processing:

| Section | Files |
|---------|-------|
| `foundations` | ai-agents-101, agent-identity, mcp-protocol, a2a-protocol, agentic-ai-landscape |
| `products` | o4aa-products, mcp-adapter, mcp-bridge, auth0-for-agents, fga-rag-deep-dive |
| `auth-flows` | obo-flow, id-jag, xaa-deep-dive, ciba, managed-connections, cimd |
| `developer` | nhi-management, workload-principals, integration-guides, s2s-m2m-patterns |
| `operations` | shadow-ai-discovery, credential-security, audit-reporting, security, compliance, regulatory-frameworks, enterprise-ai-concerns |
| `se-playbook` | demo-flow, demo-playbook, business-outcomes, use-case-patterns, customer-use-cases-data, competitive, competitive-framework, message-by-persona, customer-evidence |
| `reference` | why-okta, entra-as-idp-pattern, opa-legacy-systems, pricing, glossary |

## Phase 1 — Pull Sources (parallel)

Run all source pulls simultaneously:

**Slack channels** (read last 50 messages each, use `concise` format):
- `#okta-ai-agents-field-feedback` → channel ID `C0A2X24QT5H`
- `#okta-secures-ai-questions` → channel ID `C0A4LB3G7BN`
- `#a4aa` → channel ID `C08470NJMS5`
- `#presales-o4aa-a4aa-champions` → channel ID `C0A964KANA0`

**Confluence** (cloud ID `baeddaca-1555-4392-972a-d132ec1a7279`):
- CQL: `text ~ "Okta for AI Agents" AND type = page AND lastmodified >= now("-30d") ORDER BY lastmodified DESC`
- Limit 15 results

**Deep research** (optional — only if user explicitly requested it or if a major industry shift is known):
- Use `/deep-research` on specific topics that have moved (e.g., MCP protocol changes, new competitive moves)

## Phase 2 — Extract Signal

From the raw Slack + Confluence content, identify and categorize each piece of intelligence:

**Signal types to watch for:**

| Type | Examples |
|------|---------|
| **Status change** | EA → GA, feature shipped, product renamed |
| **Customer evidence** | Named reference, case study, hackathon data |
| **Field gotcha** | Bug, gap, missing capability, workaround needed |
| **New competitor** | Vendor mentioned that isn't in competitive.ts |
| **New use case** | Pattern surfacing from multiple field calls |
| **Pricing/commercial** | Discount policy, SKU change, licensing question |
| **Roadmap update** | Q-date shift, new item added, feature removed |
| **Demo asset** | New recording, updated deck, new POC resource |
| **Compliance/regulatory** | New framework, standard, or enforcement date |

For each signal: note the source (`@person, #channel, date`), the affected content section(s), and whether it's a **correction** (existing content is wrong) or **addition** (new information to add).

**Prioritize:**
1. Corrections first — wrong product status misleads SEs in live deals
2. High-frequency field questions — if 3+ SEs asked the same thing, it's a gap
3. New named customer evidence — proof points are always high value
4. Everything else

## Phase 3 — Update Files (parallel subagents)

Group the affected files by section and spawn one subagent per section group. Each subagent receives:
- The list of files to update in that section
- The intelligence relevant to those files
- These update rules (below)

**Update rules for subagents:**

```
For each file in your section:
1. READ the file first with the Read tool
2. Determine which signals apply to this file
3. If a correction is needed: fix it inline in the existing text
4. If new information: add a new card at the END of the cards array
5. Every addition must include [Source: @person, #channel, date] attribution
6. Use the existing callout prefixes: !! for warnings/critical, >> for details, ?? for discovery Qs, TT for talk tracks
7. Label colors: rose = warning/gap, amber = caution/roadmap, emerald = confirmed/positive, blue = informational
8. After editing, verify TypeScript is syntactically valid — balanced braces, proper string escaping
9. If nothing relevant applies to a file: skip it (don't update for the sake of updating)
```

**"Already current" detection — be precise:**
A file is only "already current" for a specific signal if the *exact information* is present —
not just the topic. Examples:
- demo-playbook.ts has a "GA demo assets" card → does NOT mean it's current for a new
  demo video URL that wasn't available when that card was written. Check if the specific
  URL/link/quote exists before skipping.
- competitive.ts has a CrowdStrike AI SPM entry → it IS current for that signal. Skip.
- A file mentions "token lifetime minimum" broadly → check if "5 minutes" and the inline
  hook seconds schema note are both present before skipping.

When in doubt: read the relevant section carefully, then decide. A false skip (missing something
new) is worse than a false add (minor duplication).

If `--section=X` was passed, only update files in that section.

## Phase 4 — Report

After all subagents complete, output a structured summary:

```
## O4AA Knowledge Hub Update — [date]

### Sources Pulled
- #okta-ai-agents-field-feedback: [N] messages, [date range]
- #okta-secures-ai-questions: [N] messages, [date range]
- #a4aa: [N] messages, [date range]
- Confluence: [N] pages found

### Files Updated ([N] total)
**Corrections (stale → current):**
- file.ts: [what was wrong → what it says now]

**Major additions:**
- file.ts: [what was added, one line]

**Minor additions:**
- file.ts: [brief note]

### Files Skipped (already current): [list]

### Topics Needing Deeper Research
- [topic]: [why it needs more investigation]

### Key Intelligence This Cycle
[3-5 bullet summary of the most important things that changed]
```

## TypeScript Content File Pattern

For reference — every content file follows this shape:

```typescript
export const content: SectionContent = {
  slug: 'section-slug',
  title: 'Section Title',
  description: '...',
  tags: [...],
  cards: [
    {
      heading: 'Card Heading',
      paragraphs: [
        '!! Critical callout text',
        '>> Detail text',
        'TT Talk track text',
        '?? Discovery question',
      ],
      labeledCallouts: [
        { label: 'LABEL', labelColor: 'emerald', text: 'Callout text.' },
      ],
    },
    // ... more cards
  ],
};
```

New cards go at the END of the `cards` array. String values use single quotes. No trailing commas on the last array item in older files (check the existing pattern per file).

## Common Pitfalls

- **MCP Bridge ≠ GA product**: It's PS-delivered; the hosted version is Q3. Don't let any update imply self-service availability.
- **Auth for MCP vs Agent Gateway**: Auth0 Auth for MCP (GA May 6) = MCP servers natively OAuth-aware. Okta Agent Gateway = proxy governing access to internal MCP servers. Different products, different audiences.
- **XAA is GA** (April 29, 2026), enabled with O4AA SKU or via Admin Console toggle.
- **FedRAMP/HIPAA tenants**: O4AA not available on these cells at GA. Healthcare deals hit this.
- **Target discount = 0%** for O4AA SKU.
- When in doubt about a product claim: mark `[UNVERIFIED — check with PMM]` rather than asserting.
