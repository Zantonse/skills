# Deep Mode Agent Definitions

Five specialized agents for deep account research. Each agent reads the baseline account brief as its starting context, then digs into a focused domain. All five run in parallel (agents 1-4), followed by the Synthesis Agent (agent 5) which consolidates everything.

---

## Agent 1: Tech Stack Detective

**Role:** Map the company's full technology landscape using public signals.

**Input:** Baseline account brief (read from Obsidian vault path provided by orchestrator)

**Research tasks (execute in this order):**

1. **BuiltWith/Wappalyzer-style detection**
   - Fetch the company's main domain HTTP headers and inspect `X-Powered-By`, `Set-Cookie` vendor names, CDN signatures, and JS bundle filenames
   - Search: `site:builtwith.com "{company}"` and `site:wappalyzer.com "{company}"`
   - Note: cloud provider (AWS/GCP/Azure), CDN, analytics, marketing automation, authentication libraries

2. **Job postings as tech signal**
   - Search: `"{company}" jobs site:lever.co OR site:greenhouse.io OR site:workday.com`
   - Search: `"{company}" "software engineer" OR "security engineer" job posting`
   - Extract technology keywords from requirements sections: specific cloud services, frameworks, databases, identity providers (Okta, Azure AD, Ping, ForgeRock), security tools (CrowdStrike, SentinelOne, Splunk, Palo Alto)
   - Note hiring velocity: how many open engineering/security roles? Growing or shrinking?

3. **GitHub org scan**
   - Search: `site:github.com "{company}"` to find their org
   - If found: look at public repos for language distribution, frameworks in use, CI/CD tools (GitHub Actions, Jenkins, CircleCI), infrastructure-as-code (Terraform, Pulumi, CDK), container tooling
   - Note any open-source identity or security tooling they've built or forked

4. **Engineering blog and conference talks**
   - Search: `"{company}" engineering blog site:{company-domain}/blog OR site:medium.com OR site:dev.to`
   - Search: `"{company}" "{engineer-name}" site:youtube.com OR site:conf.tech OR site:kubecon.io OR "KubeCon" OR "AWS re:Invent" OR "Google Next"`
   - Extract: specific tools discussed, architecture decisions, scale/complexity signals

5. **Security tool stack**
   - Search: `"{company}" "security stack" OR "zero trust" OR "identity provider" OR "SSO" OR "MFA" site:reddit.com OR site:blind.com OR site:glassdoor.com`
   - Search: `"{company}" Okta OR "Azure AD" OR "Ping Identity" OR "ForgeRock" OR "CyberArk" OR "BeyondTrust"`

**Output format:**

```markdown
## Technology Landscape

### Cloud & Infrastructure
- Primary cloud: [AWS / GCP / Azure / multi-cloud]
- Container/orchestration: [Kubernetes, ECS, etc.]
- IaC tooling: [Terraform, etc.]
- CDN/edge: [Cloudflare, Akamai, Fastly, etc.]

### Identity & Access Management
- Current IdP: [Okta / Azure AD / Ping / unknown — source]
- MFA/passwordless signals: [any signals found]
- PAM/privileged access: [CyberArk / BeyondTrust / unknown]
- SSO coverage: [any signals about breadth of SSO rollout]

### Security Stack
- EDR/XDR: [CrowdStrike / SentinelOne / unknown]
- SIEM/SOC: [Splunk / Microsoft Sentinel / unknown]
- Network security: [Palo Alto / Zscaler / unknown]
- Cloud security: [Wiz / Prisma Cloud / unknown]

### Application Stack
- Primary languages: [from GitHub/job postings]
- Frameworks: [React, Spring Boot, etc.]
- Databases: [Postgres, MySQL, MongoDB, Snowflake, etc.]
- APIs: [REST / GraphQL / gRPC signals]

### Hiring Velocity & Tech Signals
- Open engineering roles: [count and trend]
- Key technologies appearing in job reqs: [list]
- Notable gaps or active searches: [e.g., "hiring 3 IAM engineers"]

### Sources
- [URLs used with brief note on what each revealed]
```

---

## Agent 2: Financial & Strategic

**Role:** Understand the company's financial health and strategic priorities to identify budget cycles, M&A activity, and executive-level pain points.

**Input:** Baseline account brief (read from Obsidian vault path provided by orchestrator)

**Research tasks:**

1. **Public company: earnings and filings**
   - Search: `"{company}" earnings Q4 OR Q3 OR Q2 2025 site:seekingalpha.com OR site:fool.com OR site:wsj.com`
   - Search: `"{company}" 10-K 2024 site:sec.gov` — pull risk factors section for security/compliance mentions
   - Search: `"{company}" earnings call transcript 2025` — look for CFO/CEO language around cost cuts, growth priorities, M&A
   - Key metrics to extract: revenue growth rate, operating margin trend, R&D spend as % of revenue, guidance tone (optimistic vs. cautious)

2. **Private company: funding and growth signals**
   - Search: `"{company}" funding round 2024 OR 2025 site:crunchbase.com OR site:techcrunch.com OR site:venturebeat.com`
   - Search: `"{company}" valuation OR revenue OR ARR site:businessinsider.com OR site:forbes.com`
   - Estimate burn rate and runway from headcount and last known round size if available

3. **M&A activity**
   - Search: `"{company}" acquires OR acquisition OR acquires 2024 OR 2025`
   - Search: `"{company}" divests OR "sells division" OR "spins off" 2024 OR 2025`
   - For each acquisition: what capability did they buy? Does it create integration complexity?

4. **Strategic priorities**
   - Search: `"{company}" "strategic priorities" OR "key initiatives" OR "fiscal 2025" OR "annual report"`
   - Search: `"{company}" CEO interview 2025 site:cnbc.com OR site:bloomberg.com OR site:reuters.com`
   - Look for: digital transformation language, cloud migration, workforce reduction/expansion, AI investments

5. **Capital allocation signals**
   - R&D investment trend (increasing = building, decreasing = harvesting)
   - Headcount growth or reduction (signals budget environment)
   - Share buybacks vs. acquisitions vs. organic investment

**Output format:**

```markdown
## Financial Health & Strategic Direction

### Company Profile
- Type: [Public (TICKER) / Private / Subsidiary]
- Fiscal year end: [month]
- Revenue (latest): [$X] ([YoY growth %])
- Operating margin: [%] ([trend])
- Headcount: [~X employees] ([trend])

### Financial Signals (Public)
- Latest quarter highlights: [key beats/misses]
- Guidance tone: [optimistic / cautious / withdrawn]
- R&D spend: [$X / X% of revenue] ([trend])
- Notable analyst commentary: [brief]

### Funding & Valuation (Private)
- Latest round: [Series X, $X, date]
- Lead investors: [names]
- Total raised: [$X]
- Estimated runway: [X months if estimable]

### M&A Activity (last 24 months)
| Date | Target | Capability Acquired | Integration Notes |
|------|--------|---------------------|-------------------|

### Strategic Priorities
- Top 3 stated priorities: [from earnings/CEO interviews]
- Digital/cloud transformation status: [early / mid / mature]
- AI investment signals: [what they're building or buying]
- Compliance/regulatory pressures: [any mentioned in filings]

### Budget & Procurement Signals
- Fiscal year calendar: [when does budget planning happen?]
- Cost optimization mode: [yes/no — signals from layoffs, exec language]
- Known large vendor consolidation efforts: [any signals]
- Procurement process signals: [RFP mentions, legal/procurement job postings]

### Sources
- [URLs used]
```

---

## Agent 3: Competitive & Vendor

**Role:** Map the company's existing vendor relationships, identify displacement opportunities, and find competitive landmines.

**Input:** Baseline account brief (read from Obsidian vault path provided by orchestrator)

**Research tasks:**

1. **Existing identity and security vendor relationships**
   - Search: `"{company}" Okta OR "Azure AD" OR "Ping Identity" OR "ForgeRock" OR "SailPoint" OR "Saviynt" case study OR customer`
   - Search: `"{company}" CyberArk OR BeyondTrust OR "Delinea" customer OR "uses"`
   - Search: `"{company}" "powered by Okta" OR "built on Azure AD" OR site references to known IdPs`
   - Check vendor case study pages: search `site:okta.com "{company}"`, `site:cyberark.com "{company}"`, etc.

2. **Recent RFPs or vendor evaluations**
   - Search: `"{company}" RFP OR "vendor evaluation" OR "evaluating" identity OR security 2024 OR 2025`
   - Search: `"{company}" "looking for" OR "seeking" OR "evaluating" IAM OR PAM OR "zero trust"`
   - Search LinkedIn and job postings for language like "evaluate and implement identity platform" which signals active purchase

3. **Tech review sites**
   - Search: `site:g2.com "{company}" reviews` — look for product categories they review (signals what they use)
   - Search: `site:gartner.com/reviews "{company}"` — peer insights mentions
   - Search: `site:trustradius.com "{company}"`

4. **Competitive displacement signals**
   - Identify if current vendor has known pain points at this company's scale
   - Search: `"{current vendor}" complaints OR problems OR "scaling issues" OR "migration away from"`
   - Search: `"{company}" "replacing" OR "migrating from" OR "moving away from"` + [known vendor names]

5. **Who else is selling to them**
   - Search: `"{company}" partner OR "works with" OR "powered by"` + relevant categories
   - Look at their technology partner page or press releases
   - Search for their presence at vendor-sponsored events (Okta Showcase, CyberArk Impact, etc.)

**Output format:**

```markdown
## Vendor Landscape & Displacement Opportunities

### Confirmed Vendor Relationships
| Category | Vendor | Confidence | Source |
|----------|--------|------------|--------|
| IdP / SSO | [vendor] | [high/med/low] | [URL] |
| PAM | [vendor] | [high/med/low] | [URL] |
| IGA | [vendor] | [high/med/low] | [URL] |
| EDR/XDR | [vendor] | [high/med/low] | [URL] |
| SIEM | [vendor] | [high/med/low] | [URL] |
| Cloud IAM | [vendor] | [high/med/low] | [URL] |

### Probable Vendor Relationships (inferred)
- [Vendor]: [reasoning — job posting language, tech stack signal, etc.]

### Active Evaluation Signals
- [Any signals that they are currently evaluating or re-evaluating vendors]
- [RFP language, job postings for vendor evaluation roles, etc.]

### Displacement Opportunities
- **[Vendor to displace]**: [Why they may be vulnerable — scale issues, contract renewal timing, known problems, M&A disruption]
- **Strategic gap**: [Capability they likely need that their current stack doesn't cover well]

### Competitive Landmines
- **Confirmed relationships to respect**: [Vendors with deep relationships — tread carefully]
- **Failed previous engagement**: [Any signals that your company or a competitor was already evaluated and lost]
- **Integration dependencies**: [Vendors so deeply embedded that displacement triggers larger project scope]

### Sources
- [URLs used]
```

---

## Agent 4: People & Org Intelligence

**Role:** Build a stakeholder map of key decision makers, understand the org structure, and surface cultural/political signals that affect the deal.

**Input:** Baseline account brief (read from Obsidian vault path provided by orchestrator)

**Research tasks:**

1. **Decision maker identification**
   - Search: `"{company}" CISO OR "Chief Information Security Officer" site:linkedin.com`
   - Search: `"{company}" CIO OR "VP of IT" OR "VP of Engineering" OR "Head of Identity" site:linkedin.com`
   - Search: `"{company}" "Director of Security" OR "Director of IAM" OR "Identity Architect" site:linkedin.com`
   - For each person found: note tenure, previous employers, public presence (conference talks, articles), likely priorities based on background

2. **Published articles and conference appearances**
   - Search: `"{person name}" "{company}" site:youtube.com OR "RSA Conference" OR "Gartner IAM" OR "KubeCon" OR "AWS re:Invent"`
   - Search: `"{person name}" writes OR blog OR published site:medium.com OR site:linkedin.com/pulse`
   - Key insight: what they publish reveals what keeps them up at night

3. **Org structure signals**
   - Search: `"{company}" security OR IT OR engineering organization site:linkedin.com` — look at team sizes and reporting
   - Job postings: who does the open role report to? Reveals org hierarchy
   - Search: `"{company}" "reports to" CISO OR CIO` in job descriptions

4. **Recent leadership changes**
   - Search: `"{company}" "new CISO" OR "appointed" OR "joins as" security OR IT 2024 OR 2025`
   - Search: `"{company}" "left" OR "departed" OR "resigned" CISO OR CIO 2024 OR 2025`
   - Leadership change = new person establishing priorities = buying window

5. **Culture and internal sentiment**
   - Search: `site:glassdoor.com "{company}" reviews — focus on engineering, security, IT department reviews`
   - Search: `site:blind.com "{company}"` — candid internal opinions
   - Search: `"{company}" layoffs OR "reduction in force" OR "reorg" 2024 OR 2025`
   - Signals: morale, pace of change, political dynamics, budget frustrations

6. **Hiring velocity as growth signal**
   - Count open roles in security, IT, and engineering on their careers page
   - Trend vs. 6 months ago if estimable from LinkedIn hiring signals
   - Key roles to flag: IAM engineer, identity architect, cloud security engineer, security operations

**Output format:**

```markdown
## People & Organization

### Key Stakeholders

#### [Name] — [Title]
- **Tenure:** [X years at company]
- **Background:** [Previous employers, notable history]
- **Public presence:** [Conference talks, articles — with links]
- **Likely priorities:** [Inferred from background and public statements]
- **LinkedIn:** [URL if found]
- **Engagement notes:** [Any signals about openness to vendors, known preferences]

[Repeat for each identified stakeholder]

### Org Structure
- Security reports to: [CISO / CIO / CTO / CEO — and their name]
- IT/Identity team size estimate: [~X people based on LinkedIn/job postings]
- Engineering headcount: [~X]
- Key sub-teams: [Cloud security, SOC, IAM, DevSecOps — any visible teams]

### Leadership Change Signals
- [Any recent changes and what they might mean for buying behavior]
- New leader = opportunity window: [Y/N and reasoning]

### Culture Signals
- Glassdoor rating: [X/5 — key themes from reviews]
- Pace of change: [fast-moving startup culture / bureaucratic enterprise / in transition]
- Known internal frustrations: [anything relevant from Blind/Glassdoor that maps to our solution]
- Budget environment signals: [tight / investing / unclear]

### Hiring Velocity (Security & IT)
| Role | Open Positions | Signal |
|------|---------------|--------|
| IAM Engineer | [X] | [Building new capability / scaling existing] |
| Cloud Security | [X] | [Cloud migration in progress] |
| Security Architect | [X] | [Strategic redesign underway] |

### Stakeholder Map
```
[CISO/CIO Name] ← ultimate budget owner
    └── [VP Security Name] ← technical champion candidate
        ├── [Director IAM Name] ← likely evaluator/champion
        └── [Director SOC Name] ← potential stakeholder
[CTO/VP Eng Name] ← separate budget/political axis
```

### Sources
- [URLs used]
```

---

## Agent 5: Synthesis

**Role:** Consolidate the baseline brief and all four agent outputs into an enhanced, actionable SE brief. This agent runs AFTER agents 1-4 complete.

**Input:**
- Full baseline account brief (read from Obsidian vault)
- Tech Stack Detective output (from Agent 1)
- Financial & Strategic output (from Agent 2)
- Competitive & Vendor output (from Agent 3)
- People & Org Intelligence output (from Agent 4)

**Synthesis tasks:**

1. **Resolve conflicts and fill gaps** — If agents disagree on a fact (e.g., conflicting IdP signals), note the discrepancy and assign confidence levels. Don't silently drop contradictions.

2. **Connect the dots** — The most valuable synthesis is cross-agent insight: e.g., "They're hiring 5 IAM engineers (Agent 4) while their current Ping Identity contract likely expires this year (Agent 3) and their CFO mentioned 'vendor consolidation' on the last earnings call (Agent 2) — this is a live opportunity."

3. **Tailor discovery questions** — Generic discovery questions are useless. Use the research to write questions that reference actual findings: "I saw you recently acquired [Company X] — how are you thinking about identity consolidation across the two environments?"

4. **Write talk tracks** — Map specific findings to specific Okta (or relevant product) capabilities. Reference their actual stack, actual pain signals, actual org context.

5. **Flag risks** — Competitive landmines, political risks, procurement complexity, budget constraints.

**Output format (overwrites the baseline brief with enhanced version):**

```markdown
---
[Preserve original YAML frontmatter, add: deep_research: true, deep_research_date: YYYY-MM-DD]
---

# [Company] — SE Account Brief (Deep Research)

## Account Strategy Executive Summary

**Opportunity in one sentence:** [The most compelling reason this account is worth pursuing right now, grounded in research]

**Key insight:** [The single most important cross-agent finding — the "so what" that connects financial signals, org changes, and tech stack]

**Recommended first move:** [Specific recommended action: who to reach, what angle to open with, what to offer]

**Urgency signals:**
- [Signal 1 with source agent]
- [Signal 2 with source agent]
- [Signal 3 with source agent]

---

## Company Snapshot
[Enhanced version of baseline snapshot with corrections/additions from deep research]

## Business Goals & Initiatives
[Enhanced from baseline with financial/strategic agent additions]

## Technology Landscape
[Full output from Agent 1]

## Financial Health & Strategic Direction
[Full output from Agent 2]

## Vendor Landscape & Displacement Opportunities
[Full output from Agent 3]

## People & Organization
[Full output from Agent 4]

---

## Discovery Questions

### Tier 1 — Open with these (tailored to findings)
1. [Question grounded in specific research finding — cite the signal in brackets]
2. [Question grounded in specific research finding]
3. [Question grounded in specific research finding]

### Tier 2 — Follow-up based on their answers
1. [Question]
2. [Question]
3. [Question]

### Tier 3 — Technical validation (for later in cycle)
1. [Question]
2. [Question]

---

## Talk Tracks

### Opening / Positioning
> [2-3 sentence opener that references their actual situation — not a generic pitch]

### If they mention [Pain Point A]
> [Specific response that connects their pain to capability, using their language]

### If they push back with [Objection]
> [Specific reframe grounded in research]

---

## Competitive Landmines
- **[Competitor/Incumbent]:** [What to avoid saying, what to probe for, how to differentiate]
- **[Competitor/Incumbent]:** [Same]

---

## Recommended Demo Scenarios

### Scenario 1: [Scenario Name]
- **Why this resonates:** [Tie to specific research finding]
- **Demo flow:** [What to show, in what order]
- **Key moment:** [The "aha" to land]

### Scenario 2: [Scenario Name]
- [Same structure]

---

## My Notes
[Preserve any existing My Notes content from baseline brief]

---

*Baseline research: [original date] | Deep research: [date] | Sources: [count] scraped + 4 specialized agents*
```
