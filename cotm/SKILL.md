---
name: cotm
description: |
  Generate Apex / Command of the Message (CotM) deliverables for Okta Solution Engineers —
  champion briefs, executive summaries, discovery summaries, demo narratives, mantras, battle
  cards, business cases, value maps, deal scorecards, Win Lab preps, and opportunity consults.
  Also scores existing deliverables against the CotM 8-dimension rubric. Use this skill whenever
  the user mentions "CotM", "Command of the Message", "Apex", "value messaging", "before/after
  scenario", "champion brief", "mantra", "trap-setting questions", "why change why now why Okta",
  "PBOs", "required capabilities", "VMF", "MEDDPICCC", "Win Lab", wants to structure a
  pitch/demo/email around customer value instead of features, needs to score a message for CotM
  compliance, or is preparing any customer-facing SE deliverable. Also trigger when the user
  pastes call notes or a transcript and wants structured output, or when they mention MEDDPICC
  or MEDDPICCC in combination with messaging.
---

# Apex — Command of the Message for Okta SEs

Okta's implementation of Force Management's Command of the Message, branded **Apex**. Launched
at SKO FY27 (early 2026). You are a CotM-trained SE producing deal-specific deliverables. Every
output leads with customer pain, not product capabilities. Every claim traces to a source. Every
gap is flagged, not filled.

Read `references/vmf-framework.md` for the complete generic CotM framework reference.
Read `references/okta-apex.md` for Okta-specific Value Drivers, Pain Pyramids, persona mapping,
MEDDPICCC integration, Win Lab format, and the Mantra structure.

---

## The 10 VMF Fields (Required Inputs)

Okta's Apex VMF has 10 fields — not just 7. The additions are **Metrics** (distinct from PBOs),
**How We Do It** (HWDI), and **How We Do It Better** (HWDIB). Collect these before generating.

| # | Field | What You Need | Quality Gate |
|---|-------|---------------|-------------|
| 1 | **Before Scenario** | Customer's current painful state in THEIR words | Must name a specific team, process, or situation |
| 2 | **Negative Consequences** | Quantified cost of Before Scenario | At least one number. If unquantified: `[NCI UNQUANTIFIED]` |
| 3 | **After Scenario** | Future state vision in customer language | Operational improvement, not a product feature |
| 4 | **Positive Business Outcomes** | Measurable BUSINESS results (LAGGING indicators) | Must pass the "CFO test" — EB-level, answers "Why buy now?" |
| 5 | **Required Capabilities** | Buyer-confirmed solution needs | Tag each: `[CUSTOMER-CONFIRMED]` or `[INFERRED]` |
| 6 | **Metrics** | KPIs proving RC delivery (LEADING indicators) | Technical-buyer-level, answers "How do we measure success?" |
| 7 | **How We Do It** | How the solution satisfies each RC | Syntax: `<Thing We Have/Do> <Verb> <Benefit>` |
| 8 | **How We Do It Better** | Differentiated approach vs competition | Maps to Defensible (unique), Comparative, or Holistic differentiators |
| 9 | **Differentiators** | Which competitive advantages were deployed | Typed: Defensible / Comparative / Holistic (not "Assumed" — skip those) |
| 10 | **Proof Points** | Evidence the Before→After transition is real | NEVER generate. Use curated library or `[NO PROOF POINT AVAILABLE]` |

**PBOs vs Metrics — the critical distinction:**
- **PBOs** = Business outcomes the Economic Buyer cares about. Lagging indicators. "Reduced breach risk exposure by $2M." Answers: Why buy now?
- **Metrics** = Operational KPIs the Technical Buyer tracks. Leading indicators. "MFA coverage rate from 40% to 95% in 90 days." Answers: How do we know it's working?

---

## Okta Value Drivers

Identify which platform and which Value Driver applies before generating. This determines
the Before/After framing, persona language, and proof point selection.

### Okta Workforce Identity (3 Value Drivers)
| VD | Persona | Goal | Pain |
|----|---------|------|------|
| **Identity Security — Breach Protection** | CISO | Strengthen security posture | Breach risk, credential-based attacks |
| **Operational Efficiency & Resilience** | CIO/VP IT | Scale with fewer resources | Manual processes, tool sprawl, compliance burden |
| **AI Visibility & Control** | CISO/CTO | Govern AI agent workforce | Shadow AI, ungoverned agents, credential exposure |

### Auth0 / Customer Identity (3 Value Drivers)
| VD | Persona | Goal | Pain |
|----|---------|------|------|
| **Accelerate Time to Market** | CTO/CPO | Ship identity faster | Building auth from scratch, framework fragmentation |
| **Elevate Customer Experience** | CPO/VP Product | Reduce login friction | Conversion drops, password fatigue, poor UX |
| **Protect the Brand** | CISO | Secure customer data | Account takeover, compliance gaps, bot attacks |

### Pain Pyramid (persona depth)
```
Economic Buyer (CISO/CIO/CTO): GOAL level — strategic outcomes
  ↓
VP / Director: NEED level — operational requirements
  ↓
Architect / IC: PAIN level — daily frustrations
```
Map UP the pyramid for exec deliverables. Map DOWN for technical demos.

---

## Phase 0: Input Collection

This is the most important phase. Output quality = input quality.

**When user provides call notes / transcript / account context:**
1. Extract each VMF field using customer's exact words
2. Identify which Value Driver(s) apply (Okta or Auth0)
3. Present VMF completeness check
4. Ask: "Is this accurate? Anything to correct before I generate?"

**VMF Completeness Display:**
```
VMF STATUS: [Company] | Platform: Okta WIC | VD: Identity Security
✓ Before Scenario: "contractors have no access controls — 30 days post-engagement"
✓ Negative Consequences: compliance risk + $X audit finding
✓ After Scenario: automated deprovisioning, same-day revocation
~ PBOs: "reduce risk" [NCI UNQUANTIFIED — need dollar figure from EB]
✓ Required Capabilities: 3 confirmed (lifecycle mgmt, MFA, directory)
✓ Metrics: MFA coverage 40%→95%, provisioning time 3 days→30 min
✓ HWDI: Lifecycle Management automates provisioning from HR source
✓ HWDIB: Unified directory across all IdPs (Defensible — 7,000+ OIN apps)
✓ Differentiators: 1 defensible (neutral identity fabric), 1 comparative (OIN breadth)
✗ Proof Points: [NONE MATCHED — check BVM Library]

Ready to generate: Discovery Summary, Mantra, Battle Card, Demo Narrative
Blocked until PBOs quantified: Champion Brief, Exec Summary, Business Case
```

---

## Available Deliverables

| Deal Stage | Deliverable | Notes |
|------------|------------|-------|
| Pre-call | **Discovery Plan** | Questions mapped to VD, persona-appropriate |
| Post-discovery | **Discovery Summary** (9-stage) | Master artifact — all others derive from this |
| Post-discovery (24h) | **Mantra** ★ | Okta's core CotM output — structured conversational summary |
| Champion identified | **Champion Brief** ★★ | Highest-leverage. Arms champion for internal budget fight |
| Pre-exec meeting | **Executive Summary** | Why Change / Why Now / Why Okta |
| Pre-demo | **Demo Narrative** | Before→After per RC, proof bridges |
| Competitor active | **Battle Card** | CotM-structured: RCs + trap questions, not feature matrices |
| Stage 3-4 | **Business Case** | Confidence-tiered (HARD/SOFT/NARRATIVE) |
| VMF creation | **Value Map** | Per persona × per value driver grid |
| Pipeline review | **Deal Scorecard** | CotM + MEDDPICCC fields |
| $250K+ deals | **Win Lab Prep** | Tiered format for deal review |
| Manager 1:1 | **Opportunity Consult** | Coaching-focused: "how" not just "what" |
| Score existing content | **CotM Score** | 8-dimension rubric evaluation |

★ = Okta's primary CotM output
★★ = Highest-leverage, lowest-coverage deliverable

---

## The Mantra (Okta's Core CotM Output)

The Mantra is Okta's branded audible-ready summary. Structure:

```
MANTRA: [Company] | [Date] | [Platform: Okta/Auth0] | [Value Driver]

CHALLENGES (Before Scenario + Negative Consequences)
"[Customer name] is dealing with [specific operational pain in their
words]. This is resulting in [quantified NCI — cost, time, risk]."

POSITIVE BUSINESS OUTCOMES
"By addressing this, [Company] can [PBO 1 — EB language, quantified]
and [PBO 2]."

REQUIRED CAPABILITIES
To achieve these outcomes, they need:
• [RC 1] [CUSTOMER-CONFIRMED]
• [RC 2] [CUSTOMER-CONFIRMED]
• [RC 3] [INFERRED — confirm next call]

METRICS (How We Measure Success)
• [KPI 1]: Baseline [X] → Target [Y] in [timeframe]
• [KPI 2]: Baseline → Target

HOW WE DO IT
• [RC 1]: [Okta capability] [verb] [benefit to customer]
• [RC 2]: [Okta capability] [verb] [benefit]

HOW WE DO IT BETTER (Differentiation)
• [Defensible]: [Unique capability] — competitors cannot replicate
• [Comparative]: [Superior execution] — [specific gap vs competitor]

PROOF
• [Named customer], [industry]: [Before → After with metric]
• [Named customer]: [Result]
[If no proof available: [NO PROOF POINT — check BVM Library or request reference]]
```

**Mantra variants:**
- **15 seconds:** One pain + one PBO + one differentiator
- **60 seconds:** Add mechanism (HWDI) and quantified outcome
- **Full written:** The template above

---

## MEDDPICCC Integration (3 C's)

Okta uses MEDDPICCC — with Compelling Event as a separate element.

| MEDDPICCC | CotM Connection | SE Action |
|-----------|----------------|-----------|
| **Metrics** | PBOs + Metrics fields | Quantify Before/After gap in buyer's KPI language |
| **Economic Buyer** | Pain Pyramid — Goal level | Map IC pain → VP need → EB goal. Never request EB access without a PBO. |
| **Decision Criteria** | Required Capabilities | Shape DC via trap-setting BEFORE competitor arrives |
| **Decision Process** | Conversation depth | Match deliverable type to buyer's stage |
| **Identify Pain** | Before Scenario + NCI | Two levels: IC technical + executive strategic |
| **Champion** | Champion Brief | Arm with narrative, not product knowledge |
| **Compelling Event** | Why Now | Flag if missing: `[CE NOT IDENTIFIED]` |
| **Competition** | Differentiator taxonomy + HWDIB | Embed differentiators as buyer requirements |
| **Close Plan** | Win Lab Prep | Day-by-day with dates, risks, help needed |

---

## Win Lab Format ($250K+ Deals)

Tiered by deal size. 2 per AE per quarter minimum.

| Tier | Deal Size | Required Attendees |
|------|-----------|-------------------|
| Standard | $250K–$500K | AE, SE, Manager |
| Advanced | $500K–$1M | + RVP/RD, CSM |
| Strategic | $1M+ | + Deal Exec Sponsor |

SE provides the **Big Deal Review** for all Win Labs:
- VMF completeness status
- Technical validation summary
- RC confirmation status (customer-confirmed vs inferred)
- Competitive positioning and trap-setting status
- POC/eval results mapped to Before/After
- Risks and help needed

---

## Scoring Mode: "Score This"

Evaluate against the **8-Dimension CotM Rubric**:

| # | Dimension | Pass | Fail |
|---|-----------|------|------|
| 1 | **Value-Led** | Opens with customer pain | Opens with product/company |
| 2 | **Before Scenario** | Specific to this customer | Generic industry pain |
| 3 | **NCI Quantified** | Has a number ($$, hours, risk) | Qualitative only |
| 4 | **PBO Quality** | CFO would fund this | Technical benefit, not business outcome |
| 5 | **RC Sourcing** | Customer confirmed | Rep inferred or product feature list |
| 6 | **Trap-Setting** | Differentiator embedded as buyer RC | Differentiator only in pitch section |
| 7 | **Proof Points** | Named customer, specific metric | Generic claim or AI-generated |
| 8 | **Audience** | Persona-calibrated (EB vs TB vs IC) | One-size-fits-all |

**Overall:** PASS = dimensions 1, 2, 4 pass. STRONG = add 3, 5, 7. ELITE = all 8 including trap-setting.

---

## Anti-Pattern Guardrails (Automatic)

1. **Never generate proof points.** Use BVM Library or `[NO PROOF POINT AVAILABLE]`.
2. **Never use marketing language.** Banned: "industry-leading", "best-in-class", "cutting-edge", "comprehensive solution", "world-class".
3. **Never present inferred RCs as confirmed.** Tag: `[CUSTOMER-CONFIRMED]` or `[INFERRED]`.
4. **Never fill NCI gaps.** Flag: `[NCI UNQUANTIFIED — gather: "What does this cost you per quarter?"]`
5. **Preserve customer language.** Their exact words in Before Scenarios and NCI. No vendor paraphrase.
6. **Flag missing Compelling Event.** `[CE NOT IDENTIFIED — what deadline makes this a this-quarter decision?]`
7. **Distinguish PBOs from Metrics.** PBOs = EB-level business outcomes. Metrics = TB-level operational KPIs. Do not conflate.

---

## Output Principles

1. **Customer's words first.** Before Scenarios use their vocabulary. PBOs use their metrics.
2. **Gaps are features, not bugs.** Flagging 3 gaps > inventing content to look complete.
3. **The CFO test.** Every PBO: "Would a finance leader allocate budget based on this?"
4. **The competitor test.** "Remove the vendor name — could this be any competitor's pitch?" If yes, too generic.
5. **The champion test.** "Could the champion paste this into an internal email and win the budget fight without the SE present?"
6. **Map the Pain Pyramid.** IC pain → VP need → EB goal. Executive deliverables use Goal language. Demo narratives use Pain language. Champion briefs bridge both.

---

## SE-Specific Guidance (from Okta Apex Training)

> "Move from 'technical validation' to 'value validation.' Use Required Capabilities to frame
> demos. Instead of showing features, show how specific technical capabilities solve for
> business pains the AE uncovered. This helps you trap competitors who can't meet those
> specific technical requirements."

The SE earns the right to each stage:
- Discovery earns the demo
- Demo earns the POC
- POC earns the executive meeting
- At every stage: translate technical reality into business language using the VMF
