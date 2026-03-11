# Deep Mode Agent Definitions

These 5 agents are dispatched in parallel after the baseline quick-mode brief is generated. Each agent receives the baseline battlecard as input context and is responsible for one investigative dimension. A Synthesis Agent runs after all 4 research agents complete.

---

## Agent 1: Product Deep Dive Agent

**Role:** Feature-level competitive teardown. Maps the competitor's product surface against Okta's and produces a structured comparison matrix.

**Inputs:**
- Baseline battlecard content (passed in prompt)
- Vendor name and known product page URLs

**Research tasks:**
1. Scrape the competitor's main product/features page(s) using Firecrawl
2. Scrape their documentation index or developer docs for feature surface area signals
3. Search for their public changelog, release notes, or "What's New" blog (common URLs: `/changelog`, `/releases`, `/blog/product-updates`, `/docs/whats-new`)
4. Search G2 and Gartner Peer Insights for feature satisfaction scores: query `"[Vendor] reviews site:g2.com"` and `"[Vendor] reviews site:gartner.com/reviews"`
5. Cross-reference against Okta's known feature set on these dimensions:
   - Single Sign-On (SSO) — protocol support, app catalog depth, custom SAML/OIDC
   - Multi-Factor Authentication (MFA) — factors supported, phishing-resistant options, step-up auth
   - Lifecycle Management — joiner/mover/leaver automation, SCIM, HR integrations
   - Identity Governance — access certification, SoD policies, role mining, audit trails
   - API Access Management — OAuth 2.0, fine-grained authorization, API gateway integrations
   - Extensibility — workflow builder, hooks/events, SDK depth, low-code options
   - B2B/B2C Identity — CIAM capabilities, federation, self-service registration
   - Device Trust — endpoint posture, MDM integrations, passwordless

**Output format:**

```
## Feature Comparison Matrix: [Vendor] vs. Okta

| Dimension | [Vendor] | Okta | Advantage |
|-----------|----------|------|-----------|
| SSO | ... | ... | Okta / Competitor / Neutral |
| MFA | ... | ... | ... |
| Lifecycle Mgmt | ... | ... | ... |
| Governance | ... | ... | ... |
| API Access Mgmt | ... | ... | ... |
| Extensibility | ... | ... | ... |
| CIAM | ... | ... | ... |
| Device Trust | ... | ... | ... |

### Recent Feature Releases (last 6–12 months)
- [Feature]: [what it does, why it matters]
- ...

### Product Gaps (where [Vendor] lags Okta)
- ...

### Product Strengths (where [Vendor] leads or matches Okta)
- ...

### G2 / Gartner Feature Satisfaction Highlights
- Top-rated by users: ...
- Lowest-rated by users: ...
```

---

## Agent 2: Customer & Market Agent

**Role:** Maps the competitor's customer base, vertical focus, market position, and commercial model.

**Inputs:**
- Baseline battlecard content (passed in prompt)
- Vendor name

**Research tasks:**
1. Scrape the competitor's customers or case studies page (`/customers`, `/case-studies`, `/success-stories`) using Firecrawl
2. Search for recent press releases announcing customer wins: `"[Vendor] announces" OR "[Vendor] selected by" site:prnewswire.com OR site:businesswire.com`
3. Scrape their pricing page if public (`/pricing`); if paywalled note that pricing is not publicly listed
4. Search for Gartner Magic Quadrant, Forrester Wave, or IDC MarketScape placements: `"[Vendor]" "Magic Quadrant" OR "Forrester Wave" OR "MarketScape" 2024 OR 2025`
5. Search for partner ecosystem: `"[Vendor] partner" OR "[Vendor] integration partner" OR "[Vendor] MSSP"`
6. Search for evidence of customer churn to Okta or from Okta: `"switched from [Vendor] to Okta" OR "replaced [Vendor] with Okta" site:g2.com OR site:reddit.com OR site:community.okta.com`
7. Identify verticals with the highest logo density from case studies (healthcare, finance, tech, government, retail, etc.)

**Output format:**

```
## Market Position & Customer Base: [Vendor]

### Customer Profile
- Known logos: [list notable names by vertical]
- Strongest verticals: ...
- Apparent sweet spot (company size/type): ...

### Recent Customer Wins
- [Customer] — [context, source]
- ...

### Pricing & Packaging
- Model: [per-user / per-app / platform tier / custom enterprise]
- Known tiers: ...
- Price anchors (if found): ...
- Notes: ...

### Analyst Positioning
- Gartner MQ: [leader/challenger/visionary/niche, year]
- Forrester Wave: [strong performer/leader/etc., year]
- IDC: ...

### Partner Ecosystem
- Key SI/reseller partners: ...
- Technology alliances: ...
- MSSP/channel presence: ...

### Win/Loss Signals
- Evidence of wins vs. Okta: ...
- Evidence of losses to Okta: ...
```

---

## Agent 3: Strategy & Roadmap Agent

**Role:** Surfaces the competitor's strategic direction from public signals — what they're building toward, where they're investing, and what their leadership is saying.

**Inputs:**
- Baseline battlecard content (passed in prompt)
- Vendor name

**Research tasks:**
1. Search for recent conference presentations or keynotes (Gartner Identity Summit, RSA, Identiverse, etc.): `"[Vendor]" site:youtube.com OR "keynote" OR "session" "Identiverse" OR "RSA" 2024 OR 2025`
2. Scrape their engineering or company blog for posts about future direction, architecture, or platform vision (`/blog`, `/engineering`)
3. Search for M&A activity: `"[Vendor] acquires" OR "[Vendor] acquisition" 2023 OR 2024 OR 2025`
4. Search LinkedIn for recent VP/C-suite hires to infer strategic priorities: `"[Vendor]" "joins as" OR "appointed" "VP" OR "Chief" site:linkedin.com OR site:businesswire.com`
5. Search for analyst commentary on their strategy: `"[Vendor]" strategy OR "roadmap" OR "vision" site:gartner.com OR site:forrester.com OR site:kuppingercole.com`
6. If the vendor is public, search for recent earnings call highlights or investor relations disclosures: `"[Vendor]" "earnings" OR "investor day" OR "10-K" 2024 OR 2025`
7. Search for job postings that reveal investment areas: `"[Vendor]" jobs OR careers "machine learning" OR "AI" OR "identity security" OR "IGA" OR "PAM"`

**Output format:**

```
## Strategic Direction & Roadmap: [Vendor]

### Stated Strategic Priorities
- ...

### Recent Announcements & Pivots (last 12 months)
- [Date] [Announcement]: [significance]
- ...

### M&A Activity
- [Acquisition] ([date]): [what they bought, why it matters for their roadmap]
- ...

### Executive Hires (signals)
- [Role filled] — signals investment in [area]
- ...

### Financial Performance (if public)
- Revenue/growth: ...
- Profitability/burn: ...
- Key investor day themes: ...

### Where They're Heading (synthesis)
- [2–4 sentence narrative of strategic trajectory]

### Implications for Okta
- ...
```

---

## Agent 4: Win/Loss & Objection Handling Agent

**Role:** Uncovers how the competitor sells against Okta, what they attack, what customers say, and how to counter it in a deal.

**Inputs:**
- Baseline battlecard content (passed in prompt)
- Vendor name

**Research tasks:**
1. Search G2 for head-to-head comparison reviews: `"[Vendor] vs Okta" site:g2.com` and scrape the top comparison page
2. Search TrustRadius for the same: `"[Vendor] vs Okta" site:trustradius.com`
3. Search Reddit for candid competitive discussions: `"[Vendor] vs Okta" OR "[Vendor] or Okta" site:reddit.com`
4. Search for sales/marketing content where the competitor explicitly positions against Okta: `"[Vendor]" "vs Okta" OR "compared to Okta" OR "alternative to Okta" OR "replace Okta"`
5. Scan Okta's community forum or partner community for threads about this competitor: `"[Vendor]" site:community.okta.com`
6. Search for known deal landmines or procurement friction: `"[Vendor]" "contract" OR "pricing" OR "renewal" OR "lock-in" site:g2.com OR site:reddit.com OR site:trustradius.com`
7. Look for the competitor's own comparison pages or analyst-style content they publish: `site:[vendor-domain] "vs Okta" OR "compared to Okta" OR "Okta alternative"`

**Output format:**

```
## Objection Handling & Counter-FUD: [Vendor] vs. Okta

### What [Vendor] Says About Okta in Sales Cycles
- "[Claim they make]" → Counter: ...
- "[Claim they make]" → Counter: ...
- ...

### Top Themes from Customer Reviews (G2 / TrustRadius / Reddit)
Reasons customers chose [Vendor] over Okta:
- ...

Reasons customers chose Okta over [Vendor]:
- ...

Common complaints about [Vendor] from reviews:
- ...

### Known Deal Landmines
- [Landmine]: [what to watch for, how to defuse]
- ...

### "If They Say X, We Say Y" Response Framework
| Their claim | Our counter |
|-------------|-------------|
| "[X]" | "[Y]" |
| ... | ... |

### Discovery Questions to Ask When [Vendor] Is In the Deal
1. ...
2. ...
3. ...
4. ...
5. ...

### Pricing / Commercial Landmines
- ...
```

---

## Agent 5: Synthesis Agent

**Role:** Integrates the baseline battlecard with all 4 research agent outputs into a single, enhanced battlecard file. This is the final write step.

**Inputs:**
- Baseline battlecard content
- Agent 1 output (Feature Comparison Matrix)
- Agent 2 output (Market Position & Customer Base)
- Agent 3 output (Strategic Direction & Roadmap)
- Agent 4 output (Objection Handling & Counter-FUD)

**Synthesis tasks:**
1. Produce an at-a-glance comparison table at the top of the document
2. Distill the top 3 reasons Okta wins against this competitor (evidence-backed)
3. Distill the top 3 risks or deal landmines when this competitor is present
4. Write 5 specific discovery questions tailored to uncovering this competitor's weaknesses
5. Write 3–4 recommended positioning statements (first-person, sales-ready)
6. Assemble the full "If they say X, we say Y" response table from Agent 4, augmented with product evidence from Agent 1
7. Integrate all agent sections under clean headers
8. Overwrite the existing battlecard file at: `~/Documents/ObsidianNotes/Claude-Research/competitive-intel/{vendor-slug}.md`

**Output format (full enhanced battlecard):**

```markdown
---
vendor: [Vendor Name]
last_updated: [YYYY-MM-DD]
mode: deep
---

# [Vendor Name] — Enhanced Competitive Battlecard

## At-a-Glance

| Dimension | [Vendor] | Okta | Edge |
|-----------|----------|------|------|
| Market position | ... | ... | ... |
| Core strength | ... | ... | ... |
| Core weakness | ... | ... | ... |
| Pricing model | ... | ... | ... |
| Typical buyer | ... | ... | ... |
| Key differentiator | ... | ... | ... |

## Top 3 Reasons We Win

1. **[Reason]:** [1–2 sentence explanation with supporting evidence]
2. **[Reason]:** [...]
3. **[Reason]:** [...]

## Top 3 Risks / Landmines

1. **[Risk]:** [what to watch for, how to handle]
2. **[Risk]:** [...]
3. **[Risk]:** [...]

## Discovery Questions

Ask these when [Vendor] is in the deal:
1. ...
2. ...
3. ...
4. ...
5. ...

## Recommended Positioning Statements

- "Unlike [Vendor], Okta..."
- "Where [Vendor] [does X], Okta..."
- ...

## If They Say X, We Say Y

| Their claim | Our response |
|-------------|--------------|
| ... | ... |

---

[Feature Comparison Matrix — from Agent 1]

---

[Market Position & Customer Base — from Agent 2]

---

[Strategic Direction & Roadmap — from Agent 3]

---

[Objection Handling & Counter-FUD — from Agent 4]
```

---

## Orchestration Notes

- Agents 1–4 run in parallel after the baseline brief is confirmed written to disk.
- Agent 5 runs only after all 4 research agents have returned results.
- All agents use `model: "sonnet"`.
- Pass the baseline battlecard file content into each agent's prompt as a `<baseline>` block so agents have shared context without re-running the scraper.
- Agent 5 writes the final file; no other agent writes to disk.
- If any single research agent fails or returns sparse data, Agent 5 should note the gap rather than hallucinate — include a `### Data Gap` callout in the relevant section.
