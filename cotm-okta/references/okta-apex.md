# Okta Apex — CotM Implementation Reference

Source: Okta internal training materials (Apex Field Training Deck, CotM Cheat Sheet,
Formula to Win, Opportunity Coaching Guide, APEX Gem documentation, Sales Methodology FAQs).
Classification: Internal reference for SE skill use only.

## Apex Overview

**Apex** = Okta's branded implementation of Force Management's Command of the Message.
Launched at SKO FY27 (early 2026). Replaces the previous "Three Whys" framework in SFDC/Clari.

Rollout phases:
1. SKO (foundational training)
2. Live Skills Practice (4-hour roleplay sessions, March 2026)
3. Weekly Pitstops (ongoing reinforcement)
4. Manager Opportunity Coaching in 1:1s
5. Evolved Win Labs (deal reviews using CotM/MEDDPICCC)

---

## Okta Value Drivers — Full Detail

### Okta Workforce Identity Cloud (WIC)

**VD1: Identity Security — Breach Protection**
- Persona: CISO, VP Security, Security Architect
- Goal: Strengthen security posture, stop identity-based attacks
- Pain: Credential-based breaches (292-day avg detection), phishing, MFA gaps
- Before: "We can't see who has access to what. When someone leaves, it takes days to revoke."
- After: "Every identity verified continuously. Access revoked in seconds. Threats detected in real time."
- Proof points: Colgate-Palmolive (94.5K threats auto-detected), ProAssurance (~85% ticket reduction)

**VD2: Operational Efficiency & Resilience**
- Persona: CIO, VP IT, IT Operations
- Goal: Scale identity operations without proportional headcount
- Pain: Manual provisioning, tool sprawl, compliance audit burden, fragmented IdPs
- Before: "Onboarding takes 3 days. We manage 6 different identity tools. Audit prep takes weeks."
- After: "Day-1 access. Single control plane. Audit evidence generated automatically."
- Proof points: Vinted (1 day → 30 min onboarding), Experian ($1M/yr savings from 6 IdP consolidation)

**VD3: AI Visibility & Control** (NEW — GA April 2026)
- Persona: CISO, CTO, VP Engineering
- Goal: Discover, govern, and secure AI agents at scale
- Pain: Shadow AI, ungoverned agents, credential exposure, no audit trail
- Before: "We don't know how many AI agents are running or what they can access."
- After: "Every agent registered with a human owner. Least-privilege enforced. Instant revocation."
- Proof points: [NONE YET — EA product. Update when GA customers emerge.]

### Auth0 / Customer Identity Cloud (CIC)

**VD1: Accelerate Time to Market**
- Persona: CTO, CPO, VP Engineering
- Goal: Ship identity features faster, reduce auth build time
- Pain: Building custom OAuth flows, framework fragmentation, slow SDK integration
- Before: "Developers spend weeks building auth for each new app or AI agent."
- After: "Auth0 SDKs provide framework-native auth. Ship in days, not months."

**VD2: Elevate Customer Experience**
- Persona: CPO, VP Product, Growth Lead
- Goal: Reduce login friction, improve conversion
- Pain: Password fatigue, drop-off at login, inconsistent experience across apps
- Before: "20% of users abandon at our login page. Social login isn't configured."
- After: "Passwordless + social login. Conversion up. Friction eliminated."

**VD3: Protect the Brand**
- Persona: CISO, VP Security
- Goal: Secure customer-facing identity, prevent account takeover
- Pain: Bot attacks, credential stuffing, compliance gaps, data breach liability
- Before: "We had 3 account takeover incidents last quarter. No bot detection."
- After: "Attack Protection blocks credential stuffing. Breached password detection active."

---

## Pain Pyramid — Persona Mapping

### Okta WIC Pain Pyramid
```
CISO (Economic Buyer)
  GOAL: Strengthen identity security posture
  PAIN: Breach risk, regulatory exposure, board pressure
  LANGUAGE: "risk reduction", "compliance", "breach cost avoidance"
    ↓
VP Security / VP IT (Manager)
  NEED: Centralize identity, reduce tool sprawl
  PAIN: Integration difficulty, manual processes, staffing constraints
  LANGUAGE: "consolidation", "automation", "operational efficiency"
    ↓
Security Architect / IT Admin (IC)
  PAIN: Too many consoles, manual provisioning, alert fatigue
  LANGUAGE: "reduce manual work", "single pane of glass", "faster response"
```

### Auth0 CIC Pain Pyramid
```
CTO / CPO (Economic Buyer)
  GOAL: Accelerate time to market for identity features
  PAIN: Slow innovation, competitive pressure, developer bottleneck
  LANGUAGE: "time to market", "developer velocity", "competitive advantage"
    ↓
Dir/VP Engineering / Product (Manager)
  NEED: Centralize identity, reduce fragmentation
  PAIN: Multiple auth systems, inconsistent UX, maintenance burden
  LANGUAGE: "consolidation", "developer experience", "technical debt"
    ↓
Developer (IC)
  PAIN: Building and maintaining auth code, debugging OAuth flows
  LANGUAGE: "SDK quality", "documentation", "time spent on auth vs features"
```

---

## MEDDPICCC (3 C's) — Okta Implementation

Okta uses MEDDPICCC with Compelling Event as a distinct element:

| Element | Definition | CotM Connection | SFDC Field |
|---------|-----------|----------------|------------|
| **M** Metrics | Quantifiable success criteria | PBOs + Metrics fields | Metrics (text) |
| **E** Economic Buyer | Budget authority | Pain Pyramid — Goal level | Economic Buyer (lookup) |
| **D** Decision Criteria | How they'll evaluate | Required Capabilities | Decision Criteria (text) |
| **D** Decision Process | Steps/timeline to close | Match deliverable to stage | Decision Process (text) |
| **P** Paper Process | Legal/procurement/security | Pre-stage documentation | Paper Process (text) |
| **I** Identify Pain | Confirmed business pain | Before Scenario + NCI | Identify Pain (text) |
| **C** Champion | Internal advocate with power | Champion Brief template | Champion (lookup) |
| **C** Compelling Event | Time-bound trigger | Why Now | Compelling Event (text/date) |
| **C** Competition | Competitors in deal | HWDIB + Trap-Setting | Competition (text) |

**CotM fields being added to SFDC (Q1-Q2 FY27):**
- Value Driver (picklist)
- Before Scenario (text)
- Negative Consequences (text)
- PBOs (text)
- Required Capabilities (text)
- How We Do It Better (text)

---

## The Mantra — Detailed Structure

The Mantra is Okta's primary CotM output artifact. It follows this exact flow:

```
CHALLENGES → PBOs → REQUIRED CAPABILITIES → METRICS →
HOW WE DO IT → HOW WE DO IT BETTER → PROOF
```

### HWDI Syntax
`<Thing We Have/Do> <Verb> <Benefit You Get>`

Examples:
- "Lifecycle Management **automates** provisioning from HR source, **eliminating** manual account creation"
- "Identity Threat Protection **detects** compromised sessions in real time, **reducing** MTTD from days to minutes"
- "Universal Directory **consolidates** all identity sources into a single control plane, **enabling** consistent policy enforcement"

### HWDIB Syntax
Same as HWDI but explicitly names the competitive gap:
- "Unlike [approach/competitor], our unified identity fabric **governs** all identity types — human, non-human, AI — from a single platform"
- "Where point solutions require separate admin consoles per identity type, Okta **provides** a single control plane **reducing** operational overhead by [X]%"

---

## Win Lab Format

**Cadence:** 2 per AE per quarter minimum
**Scheduling:** AE owns scheduling; Pre-Sales (SE) provides Big Deal Review for $250K+

### Tiering
| Tier | Deal Size | Required Attendees | Format |
|------|-----------|-------------------|--------|
| Standard | $250K–$500K | AE, SE, First-line Manager | 30 min |
| Advanced | $500K–$1M | + RVP/RD, CSM/TAM | 45 min |
| Strategic | $1M+ | + Deal Exec Sponsor, Overlay | 60 min |

### SE Big Deal Review Structure
```
1. ACCOUNT CONTEXT: Company, industry, size, identity stack
2. VMF STATUS: Which fields confirmed, which gaps remain
3. TECHNICAL VALIDATION: POC results mapped to Before/After RCs
4. COMPETITIVE POSITION: Trap-setting status, DC alignment
5. RISKS: Technical blockers, integration concerns, timeline risks
6. HELP NEEDED: Resources, reference calls, exec sponsor engagement
```

### SFDC Win Lab Fields
- Deal Exec Sponsor (lookup)
- Win Lab Gong Recording (URL)
- Win Lab Date (date)
- Win Lab Template (attachment)

---

## APEX Gems (Internal AI Tools)

Okta has built Google Gemini-based tools on the APEX platform:

### APEX Discovery Gem
- Input: Account name, deal context, Value Framework selection (Okta/Auth0)
- Output: Pre-call discovery plan with persona-specific questions mapped to VDs
- Sources: Okta/Auth0 Value Frameworks + BVM (Business Value Metric) Library
- Limitation: Generic — not grounded in actual call data for this specific account

### APEX Mantra Generator Gem
- Input: Account name, deal context, discovery notes
- Output: CotM-structured Mantra with Challenges, PBOs, RCs, HWDI, HWDIB, Proof
- Sources: Okta/Auth0 Value Frameworks + BVM Library
- Limitation: Proof points may not match the specific deal context. Manual review required.

**How /cotm differs from APEX Gems:**
- /cotm requires customer's exact words as input (not just account name)
- /cotm flags gaps instead of filling them with generic content
- /cotm scores existing deliverables against the 8-dimension rubric
- /cotm generates champion briefs, business cases, and Win Lab preps (not just mantras)
- /cotm preserves customer language and tags RC provenance

---

## Discovery Questions — Three-Tier Structure

### Tier 1: Opening Questions (Establish Credibility)
"Based on what we've seen with similar companies in [industry], [industry insight that demonstrates
you've done your homework]. Is that consistent with what you're seeing?"

### Tier 2: General Questions (Identify Value Driver)
"What's driving the identity conversation right now? Is this more about security posture,
operational efficiency, or preparing for AI governance?"

### Tier 3: Value Driver-Specific Questions
**VD1 Identity Security:**
- "How confident are you that a departing employee loses ALL access within 24 hours?"
- "What's your current MFA coverage rate across all apps — not just SSO-integrated ones?"
- "When was the last time you discovered an orphaned account with active privileges?"

**VD2 Operational Efficiency:**
- "How many identity tools does your team manage today? What does that cost in admin time?"
- "What does your onboarding process look like from Day 0 to full productivity?"
- "If you could eliminate one manual identity process, which would have the biggest impact?"

**VD3 AI Visibility & Control:**
- "How many AI agents are operating in your environment today? Who authorized them?"
- "Can you produce an audit trail of what your AI agents accessed last quarter?"
- "How do you revoke an AI agent's access when it's no longer needed?"

---

## CSM Handoff Note

PBOs defined during the sales cycle become the delivery success metrics for CSMs post-sale.
When generating a Business Case or Champion Brief, explicitly note: "These PBOs will be tracked
by your Customer Success Manager to validate the investment." This connects the sales promise
to the renewal conversation.

---

## Last Updated
- Date: 2026-04-07
- Sources: Apex Field Training Deck, CotM Cheat Sheet (Force Management), Formula to Win
  for ASDs, APEX Gem Documentation, Sales Methodology FAQs (Highspot), Opportunity Coaching
  Guide (CoM and MEDDPICCC), Okta for AI Agents Apex Product Sales Guide
