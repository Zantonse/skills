---
date: 2026-04-07
tags:
  - research
  - deep-research
  - command-of-message
  - cotm
  - sales-methodology
  - force-management
  - meddpicc
  - presales
  - skill-building
source: claude-code
project: CraigCareer
---

> Related: [[se-team-ai-workshop-agenda]] [[se-workshop-craig-demo-talk-track]] [[se-workshop-manager-talk-track]]

# Command of the Message: Comprehensive Research Synthesis
## For the Purpose of Building a `/cotm` AI Skill

**Report compiled:** 2026-04-07
**Research scope:** 5 specialist domains, 30+ unique sources
**Primary source weighting:** Force Management official content (High trust) > Practitioner synthesis (Medium trust) > Community/forum (Low-Medium trust)

---

## Executive Summary

Command of the Message is a registered B2B sales messaging framework developed by Force Management that operates as a **value articulation layer** — governing what every rep says, not which deals to pursue. The five most consequential findings for building a `/cotm` AI skill are:

1. **All 10 CotM deliverable types derive from seven shared VMF fields.** An AI skill that extracts Before Scenario, Negative Consequences, After Scenario, Positive Business Outcomes (PBOs), Required Capabilities, Differentiators Used, and Proof Points from discovery call notes or transcripts can auto-generate every downstream artifact with minimal additional prompting. This is the core architectural insight.

2. **Input discipline is the primary determinant of output quality.** The documented failure modes of AI-generated sales content — hallucinated proof points, generic messaging, vendor cheerleading — all trace to insufficient or unstructured customer context fed into the LLM. The `/cotm` skill's Phase 0 (input collection and validation) is more important than its generation logic.

3. **CotM is a messaging framework, not a full sales methodology.** It governs conversation quality but not deal qualification, multi-stakeholder navigation, or forecasting. MEDDPICC is the qualification layer that pairs with it. A `/cotm` skill that conflates the two will produce outputs that confuse scoring with message generation.

4. **Force Management has built adjacent AI tools but has not solved deliverable generation.** Ascender AI (October 2025) reinforces methodology learning. XCELERATOR with WINN.AI (December 2025) automates CRM field entry from live calls. Neither generates polished, customer-ready CotM-structured documents. The `/cotm` deliverable generation gap is unoccupied by the methodology owner.

5. **The champion enablement brief is the highest-leverage, lowest-coverage deliverable in the market.** It is the artifact SEs most consistently fail to produce, is the one most directly tied to internal deal losses, and has no current AI tooling addressing it. A `/cotm` skill should treat the champion brief as its flagship output.

**Confidence:** High for findings 1, 2, 4, and 5. Medium for finding 3 (based on comparative analysis, not a single FM primary source making this claim explicitly).

---

## Part A: Complete CotM Framework Reference

*This section is structured as a rubric an AI skill can use to evaluate inputs, generate outputs, and score compliance.*

### A1. Organizational Alignment Layer (Pre-Conversation Foundation)

Before any rep-facing application, CotM requires the organization to answer four foundational questions. These are the source of truth from which all VMF content derives. Per Force Management's official blog (2026), every sales organization must be able to answer:

| Question | What It Governs | Failure State |
|---|---|---|
| What problems do you solve? | Alignment between marketing, sales, and delivery on which customer pains the solution addresses | Vague answers produce vague pitches; reps freelance their own problem framing |
| How specifically do you solve them? | Mechanism-level specificity ("continuous behavioral monitoring that flags anomalies in real time" vs. "we protect data") | Category-level claims collapse to commodity comparisons |
| How do you do it differently than competitors? | Differentiation that is buyer-contextualized, not internally validated | Global presence as a differentiator means nothing to a regional buyer |
| What is your proof? | A systematic proof point capture process — not ad hoc references | Reps fail the "says who?" test in live conversations |

**Confidence: High — direct Force Management primary source.**

---

### A2. The Value Messaging Framework (VMF) — Seven Core Fields

The VMF is the master artifact from which all deliverables derive. It is built through an 8–16 week Force Management engagement involving stakeholder workshops, buyer research, and 10–15 iterative drafts. For `/cotm` skill purposes, these seven fields are the **required inputs** before any output can be generated.

#### Field 1: Before Scenario
**Definition:** A vivid, buyer-language description of the prospect's current undesirable state — written from the buyer's perspective, not the vendor's.

**Quality criteria:**
- Uses the prospect's vocabulary, not vendor jargon
- Names the specific stakeholder experiencing the pain (data engineers, security operations team, provisioning administrators)
- Describes the operational situation, not the absence of the product
- Specific to this prospect, not an industry generalization

**Strong example:** "Your data engineers spend 8–12 hours weekly troubleshooting broken pipelines, often discovering issues only after downstream teams report missing data."

**Weak example:** "Your lack of our product causes pipeline failures." *(Vendor framing — fails the Before Scenario standard.)*

**Confidence: High — Force Management primary source via Oliv.ai synthesis (Dec 2025).**

---

#### Field 2: Negative Consequences (NCI — Negative Consequences of Inaction)
**Definition:** Quantified operational and financial losses that result from the Before Scenario. Creates urgency and justifies budget allocation. Serves the economic buyer specifically — they allocate discretionary budget only when pain has a dollar sign.

**Five NCI categories (per Force Management blog, 2026):**
1. Lost revenue / revenue at risk
2. Operational cost (labor hours, direct cost)
3. Compliance and legal exposure
4. Competitive disadvantage
5. Risk to strategic initiative

**Quality criteria:**
- Quantified: dollar amount, time lost, headcount affected, or regulatory penalty
- Acknowledged by the buyer — not inferred by the rep
- Connected to the economic buyer's domain of responsibility

**Confidence: High — direct Force Management primary source.**

---

#### Field 3: After Scenario
**Definition:** A concrete vision of measurable improvement after the solution is implemented. Not a feature list. A business outcome picture in the buyer's language.

**Quality criteria:**
- Describes the operational future state, not a product capability
- Uses buyer vocabulary
- Specific enough to be measurable ("engineers receive instant alerts with root cause analysis" vs. "improved visibility")
- Introduces best-practice vision the buyer may not have fully considered

**Strong example:** "With automated data quality monitoring, your engineers receive instant alerts when pipelines fail, with root cause analysis and suggested fixes — most issues self-heal automatically."

**Confidence: High — Oliv.ai CotM Guide (Dec 2025); consistent across all sources.**

---

#### Field 4: Positive Business Outcomes (PBOs)
**Definition:** Specific, measurable business performance improvements that result from achieving the After Scenario. PBOs bridge the technical buyer (who cares about capabilities) and the economic buyer (who cares about ROI and strategic impact).

**Five PBO categories:**
1. Revenue growth / protection
2. Cost reduction (hard dollar, not estimate)
3. Risk mitigation (quantified exposure reduction)
4. Productivity gains (FTE hours recovered, cycle time reduced)
5. Competitive advantage (market share, speed to market)

**The quantification standard:** "Reduced onboarding time" fails. "Reduced onboarding time from 3 days to 30 minutes, freeing 125 engineering hours monthly" is a PBO.

**Force Management's exact framing:** "People rarely argue with their own conclusions." The rep's job is to guide buyers to articulate their own PBOs through questioning, not to present them as vendor claims. Per Force Management seller blog (2026): "PBOs are the tangible benefits that result from a buyer implementing your solutions."

**Confidence: High — direct Force Management primary source.**

---

#### Field 5: Required Capabilities (RCs)
**Definition:** The specific solution features or capabilities the buyer must have to achieve their PBOs. These become the RFP criteria and technical evaluation checklist.

**Force Management's exact language (2026):** "Required capabilities define the specific requirements that are necessary to achieve your prospect's PBOs, meaning if your buyers want to achieve X, they need to make sure Y is in place."

**Strategic importance:** RCs are jointly developed with the buyer through discovery questioning. When an SE helps define RCs, those criteria can be shaped to favor the SE's solution — this is where trap-setting questions operate. RCs presented as a vendor feature list instead of buyer-confirmed criteria are a methodology failure.

**Quality criteria:**
- Confirmed by the buyer, not inferred by the rep
- 3–5 items (a list of 10+ dilutes the trap-setting potential)
- At least one RC should map to your Defensible Differentiator
- Traceable to a stated PBO

**Confidence: High — direct Force Management primary source.**

---

#### Field 6: Differentiators Used
**Definition:** The specific competitive advantages deployed in this deal. CotM defines three differentiator types, and the type determines how to position each one.

**Three differentiator categories:**

| Type | Definition | How to Use |
|---|---|---|
| **Defensible (Unique)** | Capabilities only your solution possesses. Competitors cannot replicate. | Convert to a Required Capability via trap-setting. The highest-value use of conversation time. |
| **Comparative** | Capabilities you execute better than competitors (speed, ease, support quality). | Deploy after baseline RCs are established. These tilt evaluations when multiple vendors clear the threshold. |
| **Assumed** | Table-stakes features every modern solution includes (security, cloud deployment, basic integration). | Acknowledge briefly as checkboxes. Do not spend discovery time here. Do not lead with these as differentiators. |

**The trap-setting mechanism:** Identify your Defensible Differentiator → craft a discovery question that leads the buyer to recognize the business need it solves → the buyer articulates the requirement themselves → it becomes their criterion, not your pitch → competitors cannot dislodge a requirement the buyer defined independently.

**Force Management's exact definition (2026):** "Trap-Setting Questions help you steer a discovery session toward your differentiators. We call them 'trap setting' because they trap your competition."

**Confidence: High — direct Force Management primary source; confirmed across Oliv.ai and Sales Enablement Collective.**

---

#### Field 7: Proof Points
**Definition:** Evidence that the claimed Before → After transition is real and achievable. CotM treats proof as a system, not an ad hoc reference.

**Three tests every proof point must pass:**
- **"Says Who?":** Every value claim needs a named customer or third party. "We reduce onboarding time by 70%" fails without attribution.
- **"So What?":** The metric must connect to a PBO the current prospect cares about.
- **"For Whom?":** Proof ideally matches the prospect by industry, company size, or technical environment.

**Proof point structure (FM-recommended):**
1. Before Scenario (the customer's starting state)
2. Required Capabilities implemented
3. After Scenario / PBOs achieved (quantified metrics)
4. Named customer or third-party source

**Proof point categories ranked by persuasive weight:**
1. Customer testimonial video (hardest to dismiss)
2. Named customer case study with specific metrics
3. Third-party analyst validation (Gartner, Forrester)
4. Internal ROI analysis with documented methodology

**Confidence: High — direct Force Management primary source.**

---

### A3. The "Why Change / Why Now / Why Us" Narrative Arc

Operates across the full deal cycle, particularly relevant for economic buyer engagement.

| Question | CotM Connection | SE/AE Action |
|---|---|---|
| **Why Change?** | Before Scenario + Negative Consequences | Quantify the cost of inaction. The status quo must be more expensive than change. |
| **Why Now?** | Compelling Event (intersects with MEDDPICC) | Identify the time-bound trigger: regulatory deadline, competitive threat, board initiative, contract renewal. Without a "Why Now," deals slip indefinitely. |
| **Why Us?** | Defensible Differentiators + Required Capabilities (trap-set) | Present differentiators as buyer-confirmed decision criteria. This is where trap-setting work pays off — the buyer chose the criteria that favor your solution. |

**Confidence: Medium** — practitioner validation from Reddit r/sales (2025); structural alignment confirmed against FM primary sources. FM does not use this exact three-question framing explicitly in primary sources; it is a widely adopted practitioner synthesis.

---

### A4. The Five-Step Value-Based Conversation Model

Per Force Management's published guidance (seller blog, 2026):

1. **Execute discovery to uncover business pain and PBOs.** Ask: What are the Before/After scenarios? What are the company-wide impacts? What are the negative consequences of not acting?

2. **Create justification for an urgent premium solution.** Build urgency and economic buyer engagement. The buyer must conclude: (a) they need a solution urgently, and (b) they cannot provide it internally.

3. **Help define Required Capabilities that favor your solution.** Use trap-setting questions to embed your Defensible Differentiators as evaluation criteria. Get the buyer to "stack requirements in your favor."

4. **Pull value and differentiation into negotiations.** "Our solution delivers $2M in cost reduction through these Required Capabilities. A 20% discount reduces that value by $400K — which capabilities should we remove?"

5. **Provide proof.** Match proof points to the prospect's stated PBOs, Before/After Scenarios, and Required Capabilities. Stories over logos. If proof gaps exist, acknowledge and bridge to reference calls.

**Confidence: High — direct Force Management primary source.**

---

### A5. Audible-Ready Standards

**Three required fluency formats per FM:**

| Format | Context | Structure |
|---|---|---|
| **15-second version** | Cold outreach, elevator | One pain, one outcome, one differentiator |
| **60-second version** | Discovery call opening | Add mechanism and quantified outcome: "We eliminate 40 hours monthly by automating data quality monitoring. For teams your size, that's typically $500K in recovered engineering capacity." |
| **Audience-specific pivots** | Any buyer persona | CFO hears cost/ROI; VP Engineering hears team productivity; IC hears reduced on-call burden. Same solution. Different PBO framing. |

**The test for audible-readiness:** "If I removed your company name and logo from this pitch, could it be any competitor's pitch?" If yes, it fails the CotM standard.

**Confidence: High — Oliv.ai CotM Guide (Dec 2025); consistent with FM primary sources.**

---

## Part B: Ten Deliverable Templates

*Each template is structured for direct use as a `/cotm` skill output schema. Fields in brackets are populated from the seven VMF inputs.*

---

### Template 1: Discovery Call Summary (9-Stage)

**Trigger:** After every discovery call, within 24 hours. This is the master artifact from which all other deliverables derive.

```
DISCOVERY CALL SUMMARY
Account: [Company] | Date: [Date] | Stage: [Deal Stage]
Attendees: [Names + Titles]

STAGE 1 — CURRENT STATE (Before Scenario)
"[Customer's exact words about their current situation — 
verbatim where possible]"

Operational scope: [How many teams/systems/people affected]
Recurrence: [Ongoing / triggered by specific event]

STAGE 2 — NEGATIVE CONSEQUENCES
Quantified impact:
• Dollar/time/risk: [Customer-confirmed figure or [UNCONFIRMED — 
  gather on next call]]
• Which stakeholders are affected: [Names/roles]
• What does inaction cost per month/quarter: [Estimate or [UNCONFIRMED]]

STAGE 3 — FUTURE STATE (After Scenario)
"[What ideal state looks like in their language]"

STAGE 4 — POSITIVE BUSINESS OUTCOMES
• [PBO 1 — linked to economic buyer's domain]: [Target metric]
• [PBO 2]: [Target metric]
• Executive-level strategic connection: [Company priority this supports]

STAGE 5 — REQUIRED CAPABILITIES
☐ [Capability 1] — Confirmed by: [Name/Title] — Source: [Their words]
☐ [Capability 2] — Confirmed by: [Name/Title]
☐ [Capability 3] — Confirmed by: [Name/Title]
[UNCONFIRMED RCs — gather on next call: ________]

STAGE 6 — SUCCESS METRICS / KPIs
"Success looks like [metric] improving from [baseline] to [target] 
by [timeframe]."

STAGE 7 — SOLUTION POSITION
[What was shared, and how it connected to their stated RCs]

STAGE 8 — DIFFERENTIATION / TRAP-SETTING
Trap questions asked:
• "[Question asked]" — Response: "[Buyer's response]"
Differentiators surfaced as RCs: [List]
Differentiators NOT yet surfaced: [Gaps to address]

STAGE 9 — PROOF POINTS SHARED
• [Proof point used] — Reception: [Positive/Skeptical/Indifferent]
• [Proof gaps — what proof they'd need that we didn't have]

VMF COMPLETENESS SCORECARD
Economic Buyer identified: ☐ Yes ☐ No — Name: [___]
PBOs quantified: ☐ Yes ☐ No — Amount: $[___]
NCI quantified: ☐ Yes ☐ No
Required Capabilities confirmed: ☐ Complete ☐ Partial (___/5)
Champion identified: ☐ Yes ☐ No
Trap questions deployed: ☐ Yes ☐ No
Proof point matched to their pain: ☐ Yes ☐ No

OPEN QUESTIONS / GAPS:
[List with owner and target date]

NEXT STEPS:
1. [Action] — [Owner] — [Date]
2. [Action] — [Owner] — [Date]
```

---

### Template 2: Mantra / Audible-Ready Summary Email

**Trigger:** Post-discovery call, within 24 hours. Confirms the SE's understanding in customer language. Sets context for next steps.

```
Subject: Summary — [Company] + [Your Company], [Date]

[Champion Name],

Following our conversation, I wanted to confirm what I heard:

CURRENT STATE
You described [specific operational situation in customer's exact 
words — not paraphrase].

BUSINESS IMPACT
You shared that this results in [quantified impact — cost, time, 
risk as stated by the customer].
[If unquantified: "You mentioned this affects [scope] — we'll want 
to size this more precisely."]

YOUR GOAL
You're working toward [After Scenario in their language]. Success 
would look like [PBO — their metric, their target].

WHAT YOU'D NEED
You indicated any solution would need to:
• [RC 1 — their words]
• [RC 2 — their words]
• [RC 3 — their words]

OUR APPROACH
[Your solution] addresses this by [differentiated mechanism — 
one sentence connecting your approach to their specific pain].
[Named proof point: Customer X, similar environment, specific result.]

OPEN QUESTIONS
[List unresolved items from the call that need answers before 
the next step]

NEXT STEPS
• [Action] — [Owner] — [Date]
• [Action] — [Owner] — [Date]

Please correct anything I misunderstood — getting this right matters 
more than looking like I took good notes.

[Name]
```

---

### Template 3: Champion / Internal Selling Brief

**Trigger:** After champion is identified. Enables the champion to advocate internally for budget and priority without the SE present.

```
[COMPANY NAME] — INTERNAL BUSINESS CASE BRIEF
Prepared for: [Champion Name, Title]
Date: [Date] | Deal Stage: [Stage]
[DRAFT — pending Champion review] / [FINAL — approved by Champion]

THE PROBLEM
"Today, [Company] faces [specific challenge in champion's language].
This is costing us [quantified impact — dollars, hours, risk exposure].
If unresolved, [escalating consequence over 6–12 months]."

[This section should use language the champion can paste directly 
into an internal email. No vendor jargon.]

THE OPPORTUNITY
"By addressing this, we can [specific improvement in executive language].
This directly supports [company-level priority — growth target, 
cost reduction initiative, compliance deadline].
The expected business impact is [quantified PBO]."

WHY NOW
"The triggering event is [Compelling Event — specific and dated].
Delay past [date] means [specific cost or missed opportunity]."

WHY [YOUR SOLUTION]
Three reasons grounded in what [Company] said they need:

1. [RC 1 they confirmed] → [How you deliver it] → [Proof: 
   Customer X, similar environment, specific outcome]
2. [RC 2 they confirmed] → [How you deliver it] → [Proof]
3. [RC 3 / Defensible Differentiator] → [Why this matters 
   specifically to their situation] → [Proof]

LIKELY INTERNAL OBJECTIONS — RESPONSE GUIDE
"We don't have budget." 
→ [NCI framing: cost of inaction vs. cost of solution]
"We're too busy to implement this right now." 
→ [Timeline/phasing response grounded in their After Scenario]
"[Competitor] is cheaper." 
→ [RC framing: which required capabilities would be removed?]

NEXT STEPS FOR [CHAMPION NAME]
1. [Specific action — internal meeting to schedule, stakeholder 
   to brief, document to share] — by [Date]
2. [Action] — by [Date]

SUPPORTING MATERIALS
• [Customer story: link or attachment]
• [Third-party validation: Gartner/Forrester reference]
• [ROI analysis: link]
```

---

### Template 4: Executive Summary / CxO One-Pager

**Trigger:** Before Economic Buyer or executive sponsor meeting. Synthesizes findings from prior discovery into a 1-page narrative structured around Why Change / Why Now / Why Us.

```
[COMPANY NAME] INITIATIVE — EXECUTIVE SUMMARY
Date: [Date] | Prepared for: [Executive Name, Title]

WHY CHANGE
Current state: [Specific operational problem at executive level — 
no technical specifications]
Business impact: [Dollar amount, risk exposure, or strategic 
inhibitor — confirmed in prior conversations]
Industry context: [1 sentence connecting their situation to a 
broader pattern or trend in their market — validates the urgency]

WHY NOW
[Regulatory deadline / growth initiative / competitive threat / 
contract renewal] creates a time-sensitive window.
Cost of delay: [Specific consequence per quarter — if known] 
or [Estimated at $X based on stated impact — confirm with 
[Champion Name]]

WHY [YOUR SOLUTION]
Three capabilities, each tied to their stated requirements:

• [Capability 1]: [How you uniquely deliver it] 
  → Outcome: [Customer: specific result]
• [Capability 2]: [Differentiated mechanism]
  → Outcome: [Customer: specific result]  
• [Capability 3]: [Risk reduction or strategic alignment]
  → Outcome: [Customer: specific result]

BUSINESS CASE (3-Year Value Model)
Conservative: $[X] | Likely: $[Y] | Optimistic: $[Z]
Comparable customer ROI range: [range] | Payback: [months]
[Flag: HARD values = customer-confirmed. SOFT = inferred from 
comparable customers. Validate before presenting.]

RECOMMENDED NEXT STEPS
1. [Specific action requiring executive authorization]
2. [Specific next milestone — POC, reference call, business 
   case review]
```

---

### Template 5: Demo Narrative Script

**Trigger:** Before every discovery-validated demo. Never used without a completed discovery call summary.

```
DEMO NARRATIVE
Account: [Company] | Date: [Date] | Audience: [Personas present]
Discovery Summary Reference: [Link/date of call summary]
Required Capabilities to demonstrate: [RC 1, RC 2, RC 3]

PRE-DEMO CONTEXT BRIDGE (2 minutes)
"[Customer], in our last conversation you told me [Before Scenario 
in their exact words]. That's causing [Negative Consequences — 
their quantified impact]. What you're working toward is 
[After Scenario / PBOs]. Today I'm going to show you exactly 
how we address [RC 1] and [RC 2] — and I want to leave time 
to show you something on [Defensible Differentiator] that 
[Champion] thought was worth your team seeing.
Is that still the right agenda?"

CHAPTER 1: [RC 1 — Highest Priority]
Intro: "You said you need [RC 1] to achieve [PBO 1]. Here's 
exactly how we address that..."
[Demo sequence — show feature in context of their situation]
Value checkpoint: "Does this address what you described as 
[their exact words about the problem]?"
Proof bridge: "[Customer X, same industry] was in a similar 
situation. After implementing this, they [specific outcome 
with metric]. Would it be useful to connect you with them 
directly?"

CHAPTER 2: [RC 2]
[Same structure]

CHAPTER 3: [Defensible Differentiator / Trap Validation]
Intro: "Earlier you mentioned that [trap-set RC — the capability 
they named in response to your trap question]. This is where our 
approach differs from how most teams handle this today. Watch what 
happens here..."
[Demo sequence highlighting the unique capability]
Value checkpoint: "Earlier you said [their words confirming this 
as a requirement]. Does this validate that capability for you?"
Proof bridge: "[Customer who switched from alternative approach] 
— here's what changed: [specific before/after metric]."

DEMO CLOSE (5 minutes)
Before/After Summary:
"Before [your solution]: [Before Scenario — their words].
After: [After Scenario — their words].
That maps to [PBO — quantified, their metric].
[2–3 named customers] achieved this in [timeframe].
Does this confirm we address what you described as 
your core challenge?"

NEXT STEP ASK
"Based on what you've seen, what would need to be true 
for [next stage — POC, stakeholder meeting, business case] 
to make sense by [specific date tied to Compelling Event]?"

FEATURES NOT SHOWN (for reference)
[List anything available but deliberately excluded — to prevent 
scope creep and stay focused on RCs]
```

---

### Template 6: Competitive Battle Card (CotM-Structured)

**Trigger:** When a specific competitor is active in the deal. Produced by enablement, used by SEs in preparation.

**Critical design principle:** CotM-structured battle cards are organized around Required Capabilities and trap-setting questions, not feature comparison matrices. Overclaiming here destroys SE credibility in a POC.

```
BATTLE CARD: [Your Solution] vs. [Competitor]
Last updated: [Date] — Review by: [Date + 90 days]
Approved by: [Technical owner who validated accuracy]

WHEN THIS COMPETITOR APPEARS
Deal signals: [Job postings, tech stack, existing relationships, 
mention in discovery]
Their typical ICP: [Who they target — helps contextualize 
when they're a real threat vs. paper threat]

THEIR GENUINE STRENGTHS (be honest — reps must be credible)
• [Strength 1]: Matters most when [specific scenario]
• [Strength 2]: Matters most when [specific scenario]

YOUR DEFENSIBLE DIFFERENTIATORS (capabilities they cannot replicate)
• [Differentiator 1]: [Specific capability gap — what they lack 
  or do materially worse]
• [Differentiator 2]: [Same]

TRAP-SETTING QUESTIONS (deploy during discovery, before they present)
• "[Question that surfaces Required Capability tied to your 
  Defensible Differentiator]"
  Expected response: "[What a buyer who cares will say]"
  If they say this, the differentiator is now their requirement.
• "[Question that exposes their limitation as a buyer need]"

ASSUMED CAPABILITIES (do not use as differentiators)
[List features both you and competitor have — rep should 
acknowledge and move on]

HOW TO POSITION (value-based framing, not competitor bashing)
"When a customer needs [RC tied to your differentiator], the 
question becomes [specific capability requirement]. [Competitor] 
addresses this by [honest description — do not fabricate]. The 
challenge with that approach is [specific, verifiable limitation]. 
Our approach enables [outcome]. [Named customer]: [result]."

PROOF POINTS (this competitive scenario specifically)
• [Customer who chose you over this competitor] — What they said: 
  "[Quote if available]" — Outcome: [Metric]
• [Customer who was in competitive eval] — Result: [Metric]

COMMON OBJECTIONS + VALUE-BASED RESPONSES
"[Competitor] is cheaper."
→ "[Connect to RCs: which Required Capabilities would be 
   removed at that price point? What's the cost of those gaps?]"
"We already have [Competitor] for [adjacent product]."
→ "[Integration/consolidation angle tied to their stated PBOs]"

DO NOT SAY:
[Any claim that is not directly verifiable — list specific 
claims that have caused credibility issues in past deals]
```

---

### Template 7: Business Case / ROI Framework

**Trigger:** After 2+ discovery calls confirming PBOs. Status badge is mandatory — do not produce before discovery.

```
BUSINESS CASE: [Company Name] + [Your Solution]
Status: [SKELETON / DRAFT-VALIDATION NEEDED / CUSTOMER-READY]
Prepared by: [SE Name] | Date: [Date]
Based on conversations with: [Names, titles, dates]

EXECUTIVE OVERVIEW
Current state cost of inaction: $[X] per year
[If unquantified: FLAG — gather on next call]
Expected value with [solution]: $[range] over 3 years
Payback period: [months]
Comparable customer ROI: [range from proof point bank]

VALUE DRIVER 1: [Category — e.g., "Engineering Productivity Recovery"]
Before (current state): [Customer-confirmed description + baseline metric]
After (target state): [Customer-confirmed target or comparable customer benchmark]
Value calculation:
• Volume: [Number of incidents/cycles/hours — source: customer-confirmed 
  or [COMPARABLE CUSTOMER ESTIMATE]]
• Unit cost: [Cost per incident/hour — source: [customer-confirmed / 
  industry benchmark / internal estimate]]
• Reduction: [% improvement — source: [customer target / comparable 
  customer result]]
• Annual value: $[X]

Confidence tier: 
☐ HARD — customer-confirmed baseline and target
☐ SOFT — inferred from comparable customers; methodology documented
☐ NARRATIVE — directional, no dollar conversion appropriate

Value Driver 2 / 3: [Same structure]

TOTAL QUANTIFIED VALUE
HARD values only: $[X] – $[Y] per year
HARD + SOFT: $[X] – $[Y] per year
Three-year cumulative: $[X] – $[Y]

NARRATIVE VALUE (outcome metrics, no dollar conversion)
• [e.g., "Mean time to detect: from 292 days industry average to <24 hours"]
• [e.g., "Provisioning cycle time: from [their baseline] to [target]"]

KEY ASSUMPTIONS (each sourced)
• [Assumption 1]: Source — [customer-confirmed / industry data / FM 
  comparable customer benchmark]
• [Assumption 2]: Source

HOW TO IMPROVE THIS ESTIMATE
To upgrade SOFT drivers to HARD, gather:
• [Specific data point] — Ask: "[Exact question for next call]"
• [Specific data point] — Ask: "[Exact question]"
[This section makes the business case a discovery agenda, 
not a static document]

COMPARABLE CUSTOMER REFERENCES
• [Customer] ([industry, size]): [Specific before/after with 
  time to value]
• [Customer]: [Result]
```

---

### Template 8: Value Map / Messaging Grid

**Trigger:** Produced during VMF creation for each target persona/value driver. The master reference document from which all per-deal content is customized.

```
VALUE MAP: [Solution/Product Area] × [Persona]
Value Driver: [Top-level business problem — e.g., "Identity Sprawl Risk"]
Target Persona: [Role — Economic Buyer / Technical Buyer / End User]
Last Updated: [Date] | Owner: [Name]

PERSONA CONTEXT
What they care about most: [Their primary metric / responsibility]
What a bad day looks like: [When things go wrong in their domain]
How they evaluate solutions: [Their decision criteria at this level]

BEFORE SCENARIO
"[Operational description in customer language — use actual 
language from customer interviews or calls]"
Confirmed by: [Named customers who have used this language]

NEGATIVE CONSEQUENCES
• [Quantified consequence 1]: $[X] or [metric]
• [Quantified consequence 2]
• [Strategic/risk consequence]
Source: [Customer-confirmed / industry benchmark / analyst data + date]

AFTER SCENARIO
"[Future state vision in customer language]"

POSITIVE BUSINESS OUTCOMES
• [PBO 1]: [Metric improvement — quantified]
• [PBO 2]: [Metric improvement]
• [PBO 3]: [Strategic / risk reduction]

REQUIRED CAPABILITIES
1. [RC 1]: [Why it's required — traces to which PBO]
2. [RC 2]
3. [RC 3]
4. [RC 4 — Defensible Differentiator embedded as RC]

TRAP-SETTING QUESTIONS FOR THIS PERSONA
• "[Question 1 — surfaces RC 4, the defensible differentiator]"
• "[Question 2 — quantifies NCI to create urgency]"
• "[Question 3 — surfaces After Scenario the prospect defines themselves]"

DIFFERENTIATORS
Type | Differentiator | Trap Question | Competitive Gap
Defensible | [Only you] | [Question] | [What competitor lacks]
Comparative | [You do better] | [Question] | [Measurable gap]
Assumed | [Table stakes] | [Skip — acknowledge as checkbox] | —

PROOF POINTS (for this persona × value driver)
• [Named customer, same industry/size]: "[Quantified before/after]"
• [Named customer]: "[Result]"
• [Third-party source]: "[Analyst validation + date]"
```

---

### Template 9: Deal Qualification Scorecard (VMF/Command Plan)

**Trigger:** Required for all deals Stage 2+. Stage gates enforced: cannot advance to Proposal without Economic Buyer and quantified PBOs. Per GitLab public handbook documentation and Force Management Opportunity Manager structure.

```
COMMAND PLAN / VMF SCORECARD
Account: [Name] | AE: [Name] | SE: [Name]
Stage: [Stage] | ARR: $[amount] | Close Date: [date]
Forecast Category: [Commit / Upside / Pipeline]

SECTION 1: CotM COMMAND FIELDS
(Required for all Stage 2+ deals)

WHY NOW
Compelling Event: [Specific event with date]
Cost of delay per quarter: $[X] or [consequence]
Buyer-confirmed: ☐ Yes ☐ No ☐ Inferred

PRIMARY VALUE DRIVER
Business problem Economic Buyer is funding: [Specific statement]
Connected to company initiative: [Name of initiative]

WHY [YOUR SOLUTION]
Key differentiators from the buyer's perspective:
• [Differentiator 1 — as the buyer stated it, not vendor language]
• [Differentiator 2]

WHY DO ANYTHING AT ALL
NCI (cost of status quo): $[X] or [operational impact]
Buyer-articulated: ☐ Yes ☐ No

SECTION 2: MEDDPPICC
Metrics
Quantified outcome target: [Metric + target + timeframe]
Buyer-confirmed: ☐ Yes ☐ No

Economic Buyer
Name/Title: [___] | Direct access: ☐ Yes ☐ No
Budget authority confirmed: ☐ Yes ☐ No
PBOs presented to EB: ☐ Yes ☐ No | Response: [Summary]

Decision Criteria
RCs confirmed by buyer: ☐ Complete ☐ Partial
Trap-setting completed: ☐ Yes ☐ No | Differentiators embedded: [List]
Evaluation criteria documented: ☐ Yes ☐ No

Decision Process
Steps mapped: ☐ Yes ☐ Partial | Steps: [List with dates]
All decision-makers identified: ☐ Yes ☐ No

Paper Process
Legal/security review required: ☐ Yes ☐ No
Procurement timeline: [X weeks] | Started: ☐ Yes ☐ No

Identify Pain
Root cause confirmed: ☐ Yes ☐ Symptom-level only
Pain acknowledged by EB: ☐ Yes ☐ Champion only

Champion
Name/Title: [___]
Personal motivation: [What they gain if this gets bought]
Organizational influence: [Evidence they can access EB]
Champion tested: ☐ Yes ☐ No | Test result: [Summary]

Competition
Competitors in deal: [List]
Trap questions deployed against each: ☐ Yes ☐ No
Decision criteria favor us: ☐ Yes ☐ Neutral ☐ Unfavorable

SECTION 3: CLOSE PLAN
Remaining steps to close: [Ordered list with dates and owners]
Key risks: [List]
Help needed (cross-functional): [Specific requests]

MANAGER REVIEW
Date: [Date] | Reviewed by: [Manager name]
Top 3 gaps: [Specific gaps — not generic "need more info"]
Priority actions:
1. [What rep will do] — by [Date]
2. [What rep will do] — by [Date]
Next review: [Date]
```

---

### Template 10: Opportunity Consult / QBR Review Template

**Trigger:** Monthly for all $250K+ Enterprise deals in Stage 3+. Per GitLab Handbook (public) and Force Management Opportunity Consult framework.

```
OPPORTUNITY CONSULT
Rep: [Name] | Account: [Name] | Date: [Date]
Stage: [Stage] | ARR: $[X] | Close: [Date]

COMMAND PLAN INSPECTION (10 minutes)

Why Now? 
Is the Compelling Event specific, dated, and acknowledged by buyer?
☐ Strong ☐ Weak ☐ Missing
Manager note: [What's real vs. assumed]

Value Driver / Why Change?
Is the NCI quantified in the Economic Buyer's language?
☐ Strong ☐ Weak ☐ Missing

Why Us?
Are differentiators tied to buyer-stated RCs?
☐ Traps set ☐ Mentioned as features ☐ Not addressed

MEDDPPICC GAPS (15 minutes)
For each flagged gap, the coaching question and the "how":

[Gap 1 — e.g., "No Economic Buyer access"]
Coaching question: "What's the specific obstacle to getting 
  in front of [EB]? What has [Champion] offered to do?"
The how: "Here's how I'd approach the ask to [Champion]: 
  [specific language for the rep to use]"

[Gap 2]
[Same structure — question + how]

CVO VERIFICATION (5 minutes)
Customer Verifiable Outcomes completed:
☐ [CVO 1 for current stage] — Evidence: [Buyer action taken]
☐ [CVO 2] — Evidence
CVOs for next stage needed:
☐ [Required buyer action to advance]
☐ [Required buyer action]

STRATEGIC RISK ASSESSMENT
Top 3 risks to close:
1. [Risk] — Probability: [H/M/L] — Mitigation: [Specific action]
2. [Risk] — Probability — Mitigation
3. [Risk] — Probability — Mitigation

COACHING OUTPUT
Rep leaves with:
1. [Specific action with exact language/approach] — by [Date]
2. [Specific action] — by [Date]
3. [Specific action] — by [Date]

[This section distinguishes a coaching session from a 
status update. The manager provides "how," not just "what."]

MANAGER NOTES: [YYYY-MM-DD]
[Cap: 5,000 characters — per GitLab public handbook standard]
```

---

## Part C: Eight-Dimension Scoring Rubric

*For evaluating whether any `/cotm` output — or any rep-produced deliverable — follows CotM methodology. Each dimension is independently assessed.*

**Overall scoring:** A deliverable **passes** CotM compliance if it scores Pass on dimensions 1, 2, and 4. **Strong** if it adds dimensions 3, 5, and 7. **Elite** if all eight dimensions pass — particularly dimension 6 (trap-setting presence).

---

### Dimension 1: Opening Orientation (Value-Led vs. Feature-Led)

| Score | Criteria |
|---|---|
| **Pass** | Opens with the customer's problem statement, business impact, or Before Scenario. Product capabilities appear only after the customer's pain is established and acknowledged. |
| **Borderline** | Mentions customer pain briefly but leads with a solution overview, company positioning, or product capabilities. Pain is acknowledged but subordinated. |
| **Fail** | Leads with product features, integration specs, company background, or market leadership claims. No customer pain stated before the product is introduced. |

**AI skill check:** Does the first 20% of the output contain a recognizable Before Scenario or NCI statement? If not, flag and regenerate with the instruction: "Begin with the customer's problem before mentioning any product capability."

---

### Dimension 2: Before Scenario Specificity

| Score | Criteria |
|---|---|
| **Pass** | Describes the customer's current undesirable state with: a named stakeholder or team, the specific affected process or system, operational scope (how many teams, what downstream impact), and language traceable to what the buyer actually said. |
| **Borderline** | Pain statement is recognizable but generic ("many companies struggle with X") without customer-specific evidence, named processes, or confirmed scope. Reads like a marketing persona, not a specific account. |
| **Fail** | No Before Scenario is present, or the stated "pain" is actually the absence of the vendor's product ("they don't have automated monitoring") rather than an operational problem the customer experiences. |

**AI skill check:** Does the Before Scenario contain at least one specific operational detail (team name, process, frequency, downstream impact)? If not, flag with: "Before Scenario too generic — gather specific operational details from customer."

---

### Dimension 3: Negative Consequences Quantification

| Score | Criteria |
|---|---|
| **Pass** | Consequences are quantified with at least one specific metric: dollar amount (cost or revenue at risk), time lost (hours per week, days per cycle), headcount affected, compliance penalty named, or strategic initiative at risk named. Source is the buyer or a named comparable customer. |
| **Borderline** | Qualitative consequences are stated ("this slows down the team," "it creates compliance risk") without quantification. The pain category is correct; the magnitude is unconfirmed. |
| **Fail** | No negative consequences articulated, or consequences are framed from the vendor's perspective ("they're missing out on our features") rather than the buyer's operational experience. |

**AI skill check:** Is there at least one number in the NCI section? If all NCI statements are qualitative, append: "[NCI UNQUANTIFIED — gather cost estimate or comparable customer benchmark on next call]"

---

### Dimension 4: After Scenario / PBO Quality

| Score | Criteria |
|---|---|
| **Pass** | Specific, measurable outcome is stated in the economic buyer's language. Tied to a metric the customer named (or a comparable customer metric explicitly labeled as a benchmark). Represents a business result, not a product satisfaction statement. |
| **Borderline** | Outcome is directional and real ("faster provisioning," "reduced incident response time") but not quantified or tied to an economic buyer priority. Reads like a technical improvement, not a business outcome. |
| **Fail** | Outcome is product-feature satisfaction ("they'll have better visibility into their environment," "they'll be able to see all users in one place") rather than a business result with a metric. No economic buyer connection. |

**AI skill check:** Can this PBO statement be presented to a CFO as a reason to approve budget? If the answer is no — because it's a technical capability description — it fails dimension 4.

---

### Dimension 5: Required Capabilities Sourcing and Integrity

| Score | Criteria |
|---|---|
| **Pass** | RCs were stated or confirmed by the customer in their own words. Each RC traces to a specific PBO. At least one RC maps to a Defensible Differentiator. The list is finite (3–5 items). |
| **Borderline** | RCs are listed but the source is ambiguous — unclear whether the customer confirmed them or the rep inferred them from the conversation. Some RCs are product features reframed as requirements. |
| **Fail** | RCs are a product feature list. Customer never confirmed them. The list is exhaustive (8+) rather than prioritized. No RC maps to a differentiator. No PBO connection is traceable. |

**AI skill check:** Tag each RC with its source: [CUSTOMER-CONFIRMED] or [REP-INFERRED]. Flag all [REP-INFERRED] RCs for explicit buyer confirmation on the next call.

---

### Dimension 6: Trap-Setting Presence (Differentiator Methodology)

| Score | Criteria |
|---|---|
| **Pass** | At least one discovery question or framing positioned a Defensible Differentiator as a Required Capability before competitors had the opportunity to frame the evaluation differently. The RC list reflects this — a criterion the buyer named that maps to a capability only the seller uniquely provides. |
| **Borderline** | A Defensible Differentiator is mentioned but as a vendor feature rather than embedded in the buyer's decision criteria. The buyer has not confirmed it as a requirement. Competitors can still easily propose alternatives. |
| **Fail** | No trap-setting has occurred. Differentiators are presented in the pitch section only. All RCs could apply equally to any competitor. The evaluation criteria are not favorable to the seller's differentiated position. |

**This is the elite execution dimension.** Most deliverables that pass dimensions 1–5 fail dimension 6. An AI skill should flag missing trap-setting explicitly: "[NO TRAP-SETTING DETECTED — suggest discovery questions for [Defensible Differentiator] before next competitive engagement]"

---

### Dimension 7: Proof Point Quality and Specificity

| Score | Criteria |
|---|---|
| **Pass** | Proof point is specific: a named customer (or attributed to a named third party), in a comparable industry and company size, with a quantified before/after result (metric + timeframe), relevant to the current prospect's stated pain. Passes "Says Who?", "So What?", and "For Whom?" tests. |
| **Borderline** | Proof point is real but generic ("enterprise customers have achieved significant results"), anonymized without explanation, or not connected to the current prospect's specific pain. Passes "Says Who?" but fails "So What?" or "For Whom?" |
| **Fail** | No proof point present, proof point is a marketing claim ("industry-leading platform"), metric is not attributed to a source, or the proof point is AI-generated (no verifiable customer behind it). |

**AI skill check:** Never generate proof point content without a curated library source. If no applicable proof point exists, output: "[NO PROOF POINT AVAILABLE FOR THIS PAIN/PERSONA COMBINATION — flag for enablement team to develop or source a reference call]"

---

### Dimension 8: Audience Calibration

| Score | Criteria |
|---|---|
| **Pass** | Messaging is explicitly calibrated to the buyer persona receiving it. Economic Buyer receives PBO and NCI framing with financial metrics. Technical Buyer receives RC and After Scenario framing with operational metrics. End User receives Before/After scenario framing in their day-to-day language. |
| **Borderline** | A single messaging layer mixes PBOs and RCs without persona-specific framing. The document could be read by any stakeholder but is optimally matched to none. |
| **Fail** | No persona calibration. The same technical content is sent to the CISO, the engineering team, and the CFO. Architecture diagrams appear in the Economic Buyer section. Financial metrics are absent from the executive summary. |

**AI skill check:** Before generating any output, require persona identification. Default to Economic Buyer framing if unspecified and append: "[PERSONA NOT SPECIFIED — this output uses Economic Buyer framing by default. Confirm intended audience.]"

---

## Part D: CotM + MEDDPICC Integration Map

*Concept-by-concept mapping of the two frameworks. CotM is the messaging layer; MEDDPICC is the qualification layer. Both are required for elite enterprise execution.*

**Foundational clarity:** CotM governs **how you articulate value in every conversation**. MEDDPICC governs **whether this particular deal is real, winnable, and accurately forecasted**. Neither makes the other redundant. Force Management sells both as separate offerings and explicitly pairs them in enterprise deployments. Per the Intercom case study (cited on forcemanagement.com): "We implemented Force Management's Command of the Message and MEDDPICC. Since then, average revenue per account increased almost 4x." — Judson Griffin, Head of North America & APAC Sales, Intercom.

| MEDDPICC Element | CotM Connection | How They Integrate | SE Action |
|---|---|---|---|
| **Metrics (M)** | Positive Business Outcomes | PBOs define the value story; Metrics quantifies it in the customer's confirmed language. A PBO without a metric is a hope, not a deal. | Translate Before/After Scenarios into quantified metrics the EB owns. Gather the number or flag it for the next call. |
| **Economic Buyer (E)** | Goals layer of pain flow | The "After Scenario" and PBOs are the story you take to the Economic Buyer. MEDDPICC asks whether you've gotten access; CotM provides the narrative to justify that access. | Map IC-level technical pain → manager-level operational need → EB-level strategic goal. Never request EB access without a PBO to justify it. |
| **Decision Criteria (D)** | Required Capabilities | Required Capabilities ARE the Decision Criteria — or should be. The SE's job is to shape DC through trap-setting before competitors arrive. CotM provides the mechanism; MEDDPICC tracks whether it's been accomplished. | Set trap questions before DC is formalized. If DC is already set by a competitor, assess whether your RCs are represented. If not, use champion to reopen. |
| **Decision Process (D)** | Conversation depth calibration | CotM adjusts message depth based on stage: early-stage conversations lead with Before Scenarios; late-stage conversations shift to proof and champion enablement. MEDDPICC maps the actual process steps and timeline. | Match demo depth and deliverable type to the buyer's stage in their decision process. Don't provide an ROI model before the buyer has confirmed they're evaluating. |
| **Paper Process (P)** | Post-technical-win execution | CotM doesn't address Paper Process. MEDDPICC ensures the SE has mapped security review, legal, and procurement timelines before they become deal killers. | Proactively prepare security questionnaire responses, compliance documentation, and procurement intake before the buyer's procurement team asks. |
| **Identify Pain (I)** | Before Scenario + Negative Consequences | "Identify Pain" in MEDDPICC is a qualification test: is the pain real, acknowledged, and connected to a budget decision? CotM's Before Scenario and NCI provide the content that qualifies the pain. Two levels required: IC technical pain and executive strategic pain. | Do not accept technical pain (experienced by an individual engineer) as sufficient qualification. Trace technical pain to organizational strategic impact. |
| **Champion (C)** | Champion Enablement Template | MEDDPICC defines what a champion is (someone with power and motivation who advocates internally). CotM provides the tools to make a champion effective: Before/After narrative, NCI quantification, RC list, proof points, objection handling. A champion with product knowledge but no CotM narrative will lose the internal budget fight. | Deliver a champion brief (Template 3) that gives the champion everything they need to sell in meetings the SE will never attend. Test the champion: ask them to present the value narrative back to you. |
| **Compelling Event (C)** | Why Now | The Compelling Event is the MEDDPICC term for the trigger that makes "Why Now" answerable. Without a Compelling Event, deals slip indefinitely. CotM's NCI framing creates urgency; MEDDPICC's CE identifies the specific external or internal trigger. | Use the CE to frame the demo close and the champion brief. "Given [CE], what's the cost of this evaluation extending another quarter?" |
| **Competition (C)** | Differentiator Taxonomy + Trap-Setting | MEDDPICC tracks which competitors are in the deal and how DC aligns. CotM provides the mechanism for influencing DC before the competitive evaluation crystallizes. | Map competitor presence to the DC assessment. If a competitor has shaped DC in their favor, identify which RCs were set and whether any can be reopened through the champion. |

**The integration cadence in practice:**
- **Pre-deal:** CotM framework is built org-wide (VMF creation)
- **Stage 1 discovery:** CotM Essential Questions drive conversation; MEDDPICC fields begin populating
- **Stage 2 qualification:** MEDDPICC gates advancement; CotM quality determines whether you have real PBOs and a real champion
- **Stage 3 technical evaluation:** CotM Required Capabilities become POC success criteria; MEDDPICC tracks Decision Criteria alignment
- **Stage 4 commercial:** CotM value narrative becomes negotiation anchor; MEDDPICC Paper Process prevents late surprises
- **Post-close:** CotM proof points are captured for the next VMF iteration

---

## Part E: Anti-Patterns and Skill Guardrails

*The failure modes that a `/cotm` skill must actively guard against. Ordered by severity.*

---

### Anti-Pattern 1: Hallucinated Proof Points
**Severity: Critical**

**What it looks like:** The LLM fills a proof point field with a plausible-sounding but fabricated customer story — "Company X reduced provisioning time by 60%" — when this was never said by any customer and does not exist in any case study.

**Why it happens:** LLMs fill gaps with statistically plausible content. If the prompt requests a proof point without constraining the source, the model generates one from its training data.

**Downstream damage:** An SE presents the fabricated proof point to a prospect, the prospect asks for a reference call, the SE cannot produce one, and the deal's credibility is permanently damaged. This is the most common AI-generated sales content failure per MagicBlocks AI (February 2026) and multiple practitioner sources.

**Guardrails for `/cotm`:**
- Maintain a curated proof point library (tagged by value driver, industry, company size, persona)
- Prompt constraint: "Use ONLY proof points from the following verified list: [library]. If none apply, output: [NO PROOF POINT AVAILABLE FOR THIS COMBINATION — escalate to enablement team]"
- Never allow the skill to generate a named customer outcome that isn't in the proof point library
- Confidence tier tagging: HARD (named customer, documented result), SOFT (comparable customer benchmark), NARRATIVE (directional, no attribution)

---

### Anti-Pattern 2: Generic Messaging (Category Drift)
**Severity: High**

**What it looks like:** The Before Scenario reads like a market research report rather than a specific customer's situation. "Organizations face challenges managing identity across complex hybrid environments" instead of "Your contractors have no access controls — your security team doesn't know who still has access to your production systems 30 days after an engagement ends."

**Why it happens:** Insufficient customer-specific context fed into the prompt. The LLM fills missing specifics with industry-generic language drawn from its training data on the product category.

**Downstream damage:** The deliverable fails the CotM test ("if you removed the vendor name, would this apply to any competitor?"). It produces no differentiation and no urgency.

**Guardrails for `/cotm`:**
- Require explicit customer context before generating: company name, industry, specific stakeholder role, their exact words from a call or notes
- Add a negative constraint: "Do not use industry-generic pain descriptions. Every Before Scenario statement must trace to something this specific customer said or confirmed."
- Post-generation check: If the Before Scenario could apply to 50 other prospects without modification, flag it as too generic and prompt for more specific input
- Use a chain-of-thought Phase 1: "List every specific pain statement this customer made, in their words" → Phase 2: "Write the Before Scenario using only those statements"

---

### Anti-Pattern 3: Vendor Cheerleading
**Severity: High**

**What it looks like:** The output uses uncritical superlatives ("industry-leading platform," "best-in-class security," "unmatched performance") or presents competitive positioning without acknowledging any limitations.

**Why it happens:** LLMs trained on marketing content default to positive-framing patterns. Without explicit constraints, they produce content that sounds like the company's homepage.

**Downstream damage:** Sophisticated buyers immediately discount the SE's credibility when they hear marketing language. A single superlative in an executive summary can undermine the entire CotM narrative. Per Ada Sales training (cited in research): "Differentiators must be defensible — they will stand up to scrutiny."

**Guardrails for `/cotm`:**
- Negative constraints in every system prompt: "Do not use the following words or phrases: industry-leading, best-in-class, market-leading, unmatched, cutting-edge, world-class"
- Require that every competitive claim be tied to a specific, verifiable capability gap ("They do not offer [specific capability]" not "We are superior")
- For battle cards specifically: require a "Genuine Competitor Strengths" section as a forcing function for honest positioning
- Flag any comparative claim without a source as [UNVERIFIED — confirm with product/competitive intelligence team]

---

### Anti-Pattern 4: RC Fabrication (Rep-Inferred vs. Buyer-Confirmed)
**Severity: High**

**What it looks like:** The Required Capabilities section lists product features reframed as customer requirements — presented as if the buyer confirmed them when they were never explicitly stated by the prospect.

**Why it happens:** The LLM infers logical RCs from the Before Scenario and After Scenario, which is analytically reasonable but methodology-incorrect. CotM requires RCs to be buyer-confirmed, not rep-inferred.

**Downstream damage:** RCs that the buyer never confirmed cannot be used as trap-set criteria. If challenged ("we never said that was a requirement"), the SE's credibility is damaged and the evaluation criteria revert to the competitor's framing.

**Guardrails for `/cotm`:**
- Tag all RCs with provenance: [CUSTOMER-CONFIRMED: "their exact words"] vs. [REP-INFERRED — confirm explicitly on next call]
- In the discovery summary, require the SE to attribute each RC to a named stakeholder who confirmed it
- Prompt constraint: "Only include Required Capabilities that were explicitly stated or confirmed by the customer. If you infer a logical RC that was not explicitly confirmed, label it [INFERRED — not yet confirmed] and generate a question to confirm it on the next call"

---

### Anti-Pattern 5: PBO Downgrade (Business Outcomes Replaced by Technical Benefits)
**Severity: Medium-High**

**What it looks like:** The PBO section lists technical improvements ("improved API response time," "better visibility into user sessions," "unified console view") rather than business outcomes that an economic buyer would use to justify a budget allocation.

**Why it happens:** SE-generated content naturally defaults to technical framing. The LLM mirrors the SE's vocabulary, which skews technical.

**Downstream damage:** The executive summary or champion brief fails the economic buyer test. A CFO reading about "improved API response time" cannot make a budget decision. The deal stalls at technical validation and never advances to economic buyer approval.

**Guardrails for `/cotm`:**
- Add a test in the prompt: "For each PBO, ask: would a CFO or VP of Finance use this statement to justify a budget allocation? If not, reframe as a business outcome (revenue, cost, risk, or strategic priority)."
- Require a connection statement for every technical benefit: "This results in $[X] in [business impact]" or flag it as technical benefit, not a PBO
- Dimension 4 of the scoring rubric should be applied as a generation constraint, not just a post-generation check

---

### Anti-Pattern 6: CRM Drift — Specific Language Becomes Generic Over Time
**Severity: Medium**

**What it looks like:** The customer said "our contractors have no access controls" in call 1. By the time the champion brief is generated in week 6, that has become "the organization has identity security gaps" — the specific, memorable, traceable pain language has been generalized away.

**Why it happens:** Each summarization step in a multi-call deal cycle introduces generalization. LLMs aggregate and smooth language across inputs.

**Downstream damage:** Loss of the customer's own words is a CotM failure. The champion brief needs the customer's specific language to be credible internally ("this is what our team actually said, not the vendor's framing"). Loss of specificity also makes proof point matching harder.

**Guardrails for `/cotm`:**
- Always trace Before Scenario and NCI statements to a specific call date and speaker
- Require verbatim customer quotes in brackets, clearly distinguished from SE paraphrase
- When generating from multiple call inputs, explicitly instruct: "Preserve the customer's exact words in the Before Scenario section. Do not paraphrase or generalize. Use the earliest specific language and flag where it was updated."

---

### Anti-Pattern 7: Missing "Why Now" (Urgency Vacuum)
**Severity: Medium**

**What it looks like:** The deliverable presents a strong Before Scenario and compelling PBOs but contains no Compelling Event. The buyer sees the value but has no reason to act before next quarter.

**Why it happens:** SEs often complete the what (the value story) before confirming the when (the triggering event). The LLM generates content from available inputs — if no CE is provided, it either invents one or omits the section.

**Downstream damage:** Without a "Why Now," every deal can slip. The forecast is unreliable. Deals that appear at Stage 4 in one quarter reappear at Stage 3 in the next.

**Guardrails for `/cotm`:**
- Flag the CE field as required for any deliverable beyond the discovery summary
- If CE is absent, output: "[COMPELLING EVENT NOT IDENTIFIED — this deliverable lacks urgency framing. Gather: What external or internal deadline makes this a Q[X] decision?]"
- In the deal scorecard, gate the champion brief and executive summary templates behind a confirmed CE field

---

### Anti-Pattern 8: Over-Qualification Through Keyword Pattern Matching
**Severity: Medium**

**What it looks like:** An AI deal-scoring tool marks "Economic Buyer identified" as confirmed because the rep said "I mentioned the CFO would need to be involved" — when the buyer never confirmed access or engagement.

**Why it happens:** AI scoring tools trained on MEDDPICC patterns may mark fields as confirmed when a concept is mentioned, not when the buyer has taken a verifiable action.

**Downstream damage:** False-positive deal health scores lead to forecast errors. CROs commit revenue to deals that have not cleared the MEDDPICC gates they appear to have cleared.

**Guardrails for `/cotm`:**
- Distinguish rep-stated vs. buyer-confirmed for every field
- Scoring rubric: require a Customer Verifiable Outcome (CVO) — a specific buyer action — to confirm each MEDDPICC element. "Rep mentioned EB" ≠ confirmed. "EB attended the business case review" = confirmed.
- Flag any field marked confirmed without a traceable buyer action

---

## Part F: Prompt Engineering Patterns

*Validated patterns for generating CotM-compliant output from LLMs. Based on practitioner synthesis from MagicBlocks AI (February 2026), Intuition Labs, Sparrow Genie, and SE community practitioner content.*

---

### Pattern 1: Role + Framework + Context + Constraints (Core Pattern)

The foundational structure for