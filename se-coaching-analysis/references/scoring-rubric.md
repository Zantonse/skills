---
date: 2026-04-08
tags:
  - research
  - deep-research
  - se-coaching
  - call-analysis
  - sales-engineering
  - presales
  - skill-building
source: claude-code
project: CraigCareer
---

> Related: [[cotm-deep-research-2026-04]] [[se-team-ai-workshop-agenda]]

# SE Call Coaching Analysis Skill: Research Synthesis & Build Specification

**Research compiled:** 2026-04-08
**Primary sources:** Gong Labs (326K+ calls, updated March 2025); Vivun "Definitive Guide to PreSales KPIs"; Revenue.io Scorecard Methodology (Feb 2026); Mindtickle Discovery Call Analysis (2024); Tech Sales Mastery Six Habits Workshop (2026); presales.rocks ENGAGED Demo Framework (2025–2026); John Care, *Mastering Technical Sales* T3-B3-N3 Model; Force Management CotM Debrief Framework; Gong Help Center (updated March 2026); Kalvium Labs AI Compliance Build Case Study (2026); muchbetter.ai practitioner rubric (2026); salesengineer.direct Career Ladder (May 2025)

---

## Executive Summary

Sales engineers are the most analytically under-coached role in enterprise GTM: managers observe an estimated 4–6% of their SEs' calls (based on Gong-cited data: a team of 8 reps taking 20–30 calls per week generates 160–240 calls; a manager reviews roughly 10), leaving the majority of performance data untouched. This research synthesizes five bodies of evidence — SE performance metrics, platform scoring architectures, conversation intelligence methods, SE-specific coaching models, and post-call feedback formats — into a build specification for a transcript-reading coaching skill. Five findings anchor the entire design:

**Finding 1: Discovery quality is the single highest-leverage coaching target.** Per Vivun's research, SEs who performed thorough discovery, ran a technical assessment, and customized their demo to stated needs were more than twice as likely to close. No other single behavior class had as large a measured effect on win rate. The 100-point scoring model weights discovery at 25 points accordingly.

**Finding 2: The skill's hardest problem is not the AI — it is rubric precision.** Kalvium Labs' 2026 build case study found that keyword-matching scored compliance at 58% accuracy; LLM analysis against a well-structured rubric reached 94% agreement with human reviewers. The gap was not model quality — it was rubric quality. Every scoring criterion in this specification is written to be answerable Yes/No from the transcript, observable by two independent reviewers arriving at the same answer, and directly linked to win-rate evidence.

**Finding 3: SEs require call-type-differentiated scoring.** Gong's research explicitly flags that the 43% talk-time benchmark applies to discovery calls; demo calls will naturally skew higher. A single universal scorecard applied across call types produces systematically miscalibrated scores. This specification provides four distinct call-type rubric overlays.

**Finding 4: Scores are coaching indexes, not grades.** No commercially deployed platform (Gong, Revenue.io, Chorus) produces a single universal aggregate score. The 100-point model here is a coaching tool — it generates trend data and surfaces priority gaps, not pass/fail evaluations. The coaching output (strengths, development areas, learning points, next-time actions) carries more operational value than the number.

**Finding 5: There is a hard floor on transcript-only analysis.** Tone of voice, demo visual quality, screen share execution, and post-call prospect engagement are not capturable from text. This skill should explicitly disclose these gaps in every output to preserve credibility on the dimensions it can score.

---

## Part A: Top 5 Research Findings in Detail

### Finding 1 — Discovery Behavior Is the Highest-Leverage Coaching Target

Vivun's research (cited in the Definitive Guide to PreSales KPIs) found deals where SEs performed thorough discovery followed by a needs-matched demo were more than twice as likely to close versus deals where SEs skipped or compressed discovery. Revenue.io's February 2026 scorecard framework independently identifies "quantifying pain before presenting a solution" as one of four behaviors most predictive of deal advancement.

The mechanism is structural: an SE who has not established business pain before demoing has no basis for connecting features to outcomes. The demo becomes a feature tour, not a value validation. Every subsequent objection is harder to handle because the SE has not established what problem is being solved, for whom, and at what cost.

Coaching implication: discovery is a learnable, transcript-measurable skill. Whether the SE asked about business pain before mentioning the product, whether they attempted to quantify the impact of the customer's stated problem, whether they probed the current solution — all are detectable from transcript as present/absent.

**Confidence: MEDIUM** (Vivun, single study; Revenue.io, practitioner framework not a controlled trial. The directional finding is consistent across multiple independent sources, which raises practical confidence even where experimental rigor is limited.)

---

### Finding 2 — Conversation Dynamics Are Measurable and Predictive, But Calibration Requires Call-Type Context

Gong's March 2025 analysis of 326,000+ calls established the following benchmarks:

- **Closed-won calls:** SE talk time averages 57%
- **Closed-lost calls:** SE talk time averages 62%
- **Risk threshold:** SE talk time above 65% consistently correlates with lower win rates
- **Discovery call target:** 43% SE talk / 57% customer talk (Gong's "golden ratio," originally published 2016, still cited as best-practice target for discovery specifically)
- **Top-performer consistency signal:** High performers' talk ratio varies by ~5 percentage points between won and lost deals. Low performers' talk ratio swings by ~10 percentage points (54% in won vs. 64% in lost). Inconsistency itself is a coaching signal — it indicates reactive rather than process-driven behavior.

Question count finding is counter-intuitive: sellers who won deals asked 15–16 questions per call. Sellers who lost deals asked approximately 20 questions per call. More questions correlate with worse outcomes because struggling SEs conduct interrogations rather than conversations. Mindtickle's 2024 analysis of discovery calls found the average customer asks approximately 12 questions back — a proxy for engagement level.

**Confidence: HIGH** (Gong, 326K+ calls, March 2025 update; Mindtickle 2024 methodology is less documented but consistent directionally.)

---

### Finding 3 — LLM-Based Rubric Scoring Substantially Outperforms Keyword Matching for Coaching Tasks

Kalvium Labs built a sales compliance AI in 2026 and published comparative accuracy data:

- Keyword matching accuracy: **58%** on compliance scoring task
- LLM analysis against structured rubric: **94% agreement** with human reviewers

The accuracy gap was attributable not to model quality but to scoring method. Keywords cannot detect whether a behavior occurred in context (a rep who says "I hear your concern about price" has not handled the pricing objection; they've acknowledged it — keyword matching conflates the two). LLMs scoring against a rubric that specifies exactly what constitutes a "yes" can make contextual judgments.

Kalvium also found that Claude 3.5 Sonnet produced noticeably better natural-language explanations of why something scored as a failure, compared to GPT-4o. GPT-4o outperformed on cost and latency. For a coaching application, explanation quality matters more than for a compliance-flagging application — the SE needs to understand WHY a behavior scored as it did.

Cost benchmark: approximately $0.04 per analyzed call at a 15-minute average call length. Transcript generation is the larger cost component; the LLM analysis itself costs under $0.02.

**Confidence: HIGH** (Kalvium Labs, published build case study with methodology described; cost figures are point-in-time and subject to model pricing changes.)

---

### Finding 4 — SE Coaching Addresses a Distinct Problem Set That AE Coaching Frameworks Miss

Three SE-specific failure modes do not appear in AE coaching rubrics:

**Feature dumping:** The SE shows everything the product can do, rather than showing only what solves the buyer's stated problem. Detectable: ratio of features demonstrated vs. features that were linked to a stated customer requirement in the same call.

**POC scope sprawl:** The SE over-engineers the proof of concept to demonstrate technical depth rather than constraining it to prove the specific success criteria that advance the deal. Partially detectable: whether the SE defined specific POC success criteria on the call.

**AE-SE role boundary failure:** The SE either defers entirely to the AE (abdication) or takes over the commercial conversation (territory violation). Detectable: whether the SE attempted to close a commercial commitment, and whether the SE passed technical questions to the AE they should have handled themselves.

Force Management's Command of the Message framework articulates the core SE coaching target as **value validation** (confirming that the product's capabilities solve the customer's business problem at a premium-justifying level) vs. **technical validation** (confirming the product can do what was asked). SEs stuck in technical validation mode are demo-support; SEs executing value validation are deal-drivers. This distinction is detectable from transcript.

**Confidence: HIGH** (multiple independent frameworks converge: Force Management, Tech Sales Mastery, salesengineer.direct, presales.rocks all describe this distinction without having coordinated)

---

### Finding 5 — Scoring Architecture Design Choices Have Large Effects on Coaching Quality

Five design principles emerge from analysis across all platforms (Gong, Chorus, Revenue.io) and practitioner frameworks:

1. **Binary questions score more consistently than 1–5 scales when AI is scoring.** Revenue.io, Gong, and Chorus documentation all recommend Yes/No framing where possible.
2. **Maximum 10 questions per scorecard.** Chorus explicitly caps at 10 questions and recommends under 5 per coaching initiative. Revenue.io: "a focused scorecard outperforms a comprehensive one."
3. **No compound questions.** "Did the SE identify pain AND quantify impact?" must be two separate questions.
4. **Eliminate adjectives from scoring criteria.** "Effectively handled objections" is unscoreable — two reviewers will disagree. "SE restated the customer's objection before responding" is binary and reviewable.
5. **Build rubrics from winning calls, not from theory.** Revenue.io's published framework (Feb 2026) recommends identifying 3–5 high-performing calls, extracting repeatable behaviors, and translating them to binary questions as the first step. Theoretical rubric construction produces academically complete scorecards that do not predict real performance.

**Confidence: HIGH** (consistent across platform documentation, practitioner frameworks, and the Kalvium build case study)

---

## Part B: The 100-Point Scoring Model

### Design Rationale

The model covers seven dimensions, each weighted by evidence of correlation with SE win rates. Weights are not equal-distributed — they are calibrated to the evidence:

- Discovery quality carries the highest weight (25 points) because of the Vivun 2x close rate finding and Revenue.io's identification of it as the #1 scorecard driver.
- Conversation dynamics carries 20 points based on Gong's 326K-call dataset showing direct measurable correlation.
- Next-step discipline carries 15 points based on Gong's finding that top-performing SEs spend 53% more time discussing next steps in first meetings.
- Value alignment carries 15 points based on Vivun's finding that customized demo-to-requirements linkage predicts close rate.
- Technical credibility carries 10 points — a uniquely SE dimension with no AE equivalent, scored qualitatively.
- Engagement quality carries 10 points as a secondary signal (Mindtickle's 12-customer-question baseline; customer sentiment shifts as deal health proxy).
- Stakeholder and competitive intelligence carries 5 points — deal hygiene, low weight because absence is not always failure.

**Total: 100 points.**

---

### Dimension 1: Discovery Quality (25 points)

**What this measures:** Whether the SE established business pain, quantified impact, understood the current solution, and identified stakeholders before or instead of presenting product capabilities.

**Sub-criteria and point allocation:**

| Sub-criterion | Points | Scoring Question |
|---|---|---|
| Pain before product | 7 | Did the SE ask about business pain or current-state challenges **before** mentioning product capabilities or requesting a demo scenario? |
| Business impact quantification | 6 | Did the SE attempt to get the customer to attach numbers, time, or frequency to their pain? (Evidence: dollar amounts, time estimates, volume counts in customer responses.) |
| Current solution probing | 4 | Did the SE ask what the customer currently uses and what they like/dislike about it? |
| Decision process and stakeholder mapping | 5 | Did the SE ask who else is involved in the decision? Was an economic buyer named or a path to the EB defined? |
| Champion identification | 3 | Did the SE ask about the customer's personal stake in the outcome, or identify who has internal motivation to make this happen? |

**Pass (21–25):** All five sub-criteria present. Business impact is specific (numbers named). Stakeholder mapping produced a name and role.

**Borderline (13–20):** Three to four sub-criteria present. Pain was established but not quantified. Stakeholder mapping was surface-level ("I'll need to involve my team") without names.

**Fail (0–12):** Fewer than three sub-criteria present. SE moved to product/demo before establishing any business pain. No stakeholder mapping attempted.

**Gong data anchor:** Deals with no decision-maker involvement are 80% less likely to close; enterprise deals above $100K with no DM involvement are 233% less likely to close (Gong, 2025).

---

### Dimension 2: Conversation Dynamics (20 points)

**What this measures:** Talk-to-listen ratio, monologue management, question quality, and conversational interactivity.

| Sub-criterion | Points | Scoring Question |
|---|---|---|
| Talk ratio (discovery calls: SE <50%; demo calls: SE <65%) | 6 | Is the SE's estimated talk share within the call-type-appropriate target range? |
| Longest monologue | 4 | Did the SE speak continuously for more than 3–4 minutes without a customer response or question? (Flag if yes.) |
| Question quality over quantity | 5 | Were at least 60% of the SE's questions open-ended? Did the SE ask follow-up probing questions (vs. pivoting to a new topic) after significant customer responses? |
| Interactivity and patience | 5 | Does the conversation have frequent speaker turns (dialogue rhythm vs. monologue pattern)? Did the SE appear to pause and allow the customer to finish before responding? |

**Pass (17–20):** Talk ratio within target range. No monologues flagged. Open questions predominate. Probing follow-ups present. Conversation has dialogue rhythm.

**Borderline (10–16):** Talk ratio slightly outside range (e.g., 55% on a discovery call) or a single long monologue present. Questions mostly open-ended but some missed follow-up opportunities.

**Fail (0–9):** SE talk time above 65% on any call type, OR multiple monologues over 3 minutes, OR predominantly closed/leading questions, OR flat Q&A structure with no dialogue rhythm.

**Gong data anchors:** Talk ratio benchmark for discovery: 43% SE / 57% customer (Gong, 2016, still cited). Risk threshold: >65% SE talk time. Top performers' talk ratio varies ≤5 points between won and lost deals; inconsistency of 10+ points is a coaching signal (Gong, March 2025).

---

### Dimension 3: Value Alignment — Demo and Solution Relevance (15 points)

**What this measures:** Whether the SE linked capabilities to customer-stated requirements, used relevant proof points, and demonstrated the solution in terms of the customer's situation rather than generic product functionality.

| Sub-criterion | Points | Scoring Question |
|---|---|---|
| Demo-to-requirements linkage | 6 | Did the SE explicitly connect at least two product capabilities to requirements the **customer stated on this call** (not generic use cases)? ("You mentioned X — here's how this addresses that.") |
| Proof point relevance | 5 | Did the SE use customer examples? Were they matched to this customer's industry, use case, or stated pain — or were they generic? |
| Value framing over feature framing | 4 | Were capabilities introduced in terms of the customer's outcome ("this means you can…") rather than product function ("this feature lets you…")? |

**Pass (12–15):** At minimum two explicit linkages between demo content and stated customer requirements. Proof points are industry- or problem-relevant. At least 50% of capability explanations are framed in customer outcome terms.

**Borderline (7–11):** Some linkage present but inconsistent. Proof points used but not tailored. Occasional outcome framing.

**Fail (0–6):** Demo is a generic feature walkthrough with no connection to stated requirements. Proof points absent or mismatched. Feature framing throughout.

**Evidence anchor:** Vivun research: deals where SEs customized presentation to stated needs were more than 2x as likely to close (Vivun, Definitive Guide to PreSales KPIs).

---

### Dimension 4: Next-Step Discipline (15 points)

**What this measures:** Whether the SE closed the call with a specific, owned, time-bounded next step — and whether the call ended with forward deal momentum.

| Sub-criterion | Points | Scoring Question |
|---|---|---|
| Specificity of next step | 6 | Does the next step include: (1) a specific action, (2) a named owner, (3) a date or timeframe? All three required for full credit. |
| Technical next-step ownership | 4 | Did the SE take ownership of a technical deliverable (architecture document, POC scope, demo environment, technical Q&A follow-up) rather than leaving all next steps to the AE? |
| Technical requirements confirmation | 5 | Did the SE summarize or confirm the technical requirements discussed on the call ("So to confirm — you need X, Y, and Z. Is that the complete list?")? |

**Pass (12–15):** Specific next step with all three components. SE owns at least one technical deliverable. Requirements confirmed or summarized.

**Borderline (7–11):** Next step defined but missing a date or owner specificity. SE mentioned follow-up without confirming technical requirements.

**Fail (0–6):** Vague close ("we'll follow up" or "I'll send you some information"). No technical next step owned. No requirements confirmation.

**Gong data anchor:** In the fastest-closing deals, SEs spent 53% more time discussing next steps during the first meeting than in slow-closing deals (Gong, 2025).

---

### Dimension 5: Technical Credibility (10 points)

*This is the most SE-specific dimension. It has no AE equivalent. It is qualitatively assessed because technical accuracy requires domain knowledge the model cannot independently verify.*

**What this measures:** Whether the SE demonstrated accurate, confident technical knowledge; recovered from knowledge gaps professionally; and avoided over-committing on capability.

| Sub-criterion | Points | Scoring Question |
|---|---|---|
| Accuracy and confidence | 4 | Did the SE answer technical questions without hedging excessively, contradicting themselves, or making claims that seem implausibly broad? |
| Gap handling | 3 | When the SE appeared to not know an answer, did they acknowledge it professionally ("I want to confirm that before I commit to it") rather than bluffing or deflecting? |
| Over-commitment avoidance | 3 | Did the SE avoid committing to roadmap items, custom development, or SLAs that would require separate approval? |

**Pass (8–10):** Confident, accurate responses with no apparent bluffing. One or more knowledge gaps handled with professional acknowledgment. No over-commits detected.

**Borderline (4–7):** Mostly credible but one or two moments of hesitancy or vague hedging that may have reduced buyer confidence.

**Fail (0–3):** Apparent inaccuracies, contradictions, or defensive deflection to avoid technical questions. Or: over-committed on roadmap/custom items.

**Important caveat:** The skill cannot independently verify technical accuracy. This dimension scores *the pattern of confidence, recovery, and honesty* — not the technical facts themselves. Flag this limitation in every output.

---

### Dimension 6: Engagement Quality (10 points)

**What this measures:** The quality of customer engagement signals — questions the customer asked, objection handling quality, and indicators of whether the SE created genuine dialogue.

| Sub-criterion | Points | Scoring Question |
|---|---|---|
| Customer question frequency | 3 | Did the customer ask 6 or more questions during the call? (Mindtickle 2024 baseline: ~12 questions per quality discovery call; 5 or fewer is a low-engagement signal.) |
| Objection handling quality | 4 | When an objection was raised, did the SE: (a) acknowledge it explicitly, (b) probe for the root concern with a question, (c) address it with evidence? Deflection, over-explanation, or feature pivoting scores low. |
| Customer affirmation and vocabulary adoption | 3 | Did the customer use language introduced by the SE, offer unsolicited additional information, or provide explicit affirmations ("that's exactly what we need")? These are positive engagement signals. |

**Pass (8–10):** Visible customer engagement through questions and affirmations. Objections handled with curiosity and evidence. Customer adopted SE framing.

**Borderline (4–7):** Moderate customer engagement. Objections partially handled. Some affirmations present.

**Fail (0–3):** Customer asked few questions, gave brief responses. Objections deflected or over-explained. No engagement affirmations.

**Mindtickle data anchor:** Average discovery call, customers ask ~12 questions back (Mindtickle, 2024). Below 5–6 suggests low engagement or a buyer who has already decided.

---

### Dimension 7: Stakeholder and Competitive Intelligence (5 points)

**What this measures:** Whether the call surfaced new buying group information and competitive landscape data that advances deal strategy.

| Sub-criterion | Points | Scoring Question |
|---|---|---|
| New stakeholders identified | 2 | Did the call surface names, titles, or departments of stakeholders not previously known? |
| Competitive landscape captured | 3 | Were competitors mentioned? Were specific competitor capabilities or preferences named by the customer? Did the SE handle the competitive mention by pivoting to differentiated value vs. feature comparison? |

**Pass (4–5):** New stakeholder surfaced with name/role. Competitor identified, customer preference noted, SE response was value-differentiation not feature-parity comparison.

**Borderline (2–3):** One element captured but not both. Competitive mention handled adequately.

**Fail (0–1):** No stakeholder mapping or competitive positioning attempted, despite opportunity.

**Gong data anchor:** Close rates increase when competition is mentioned early and addressed; they drop when competition surfaces late without SE influence (Gong, 2025).

---

### 100-Point Score Summary Table

| Dimension | Max Points | Pass Threshold | Borderline | Fail |
|---|---|---|---|---|
| Discovery Quality | 25 | 21–25 | 13–20 | 0–12 |
| Conversation Dynamics | 20 | 17–20 | 10–16 | 0–9 |
| Value Alignment | 15 | 12–15 | 7–11 | 0–6 |
| Next-Step Discipline | 15 | 12–15 | 7–11 | 0–6 |
| Technical Credibility | 10 | 8–10 | 4–7 | 0–3 |
| Engagement Quality | 10 | 8–10 | 4–7 | 0–3 |
| Stakeholder & Competitive Intel | 5 | 4–5 | 2–3 | 0–1 |
| **TOTAL** | **100** | **82–100** | **55–81** | **0–54** |

**Aggregate score interpretation:**
- **82–100:** Strong call. One to two targeted coaching opportunities expected.
- **55–81:** Developing call. Two to three clear gaps. Prioritize the dimension furthest below pass threshold.
- **0–54:** Needs intervention. Discovery or conversation dynamics likely driving overall low score. Review full call with manager.

---

## Part C: Call-Type-Specific Rubric Adjustments

### Why Call-Type Calibration Is Mandatory

Gong's research explicitly states the 43/57 talk ratio is most applicable to discovery and qualification calls. A demo call where the SE talks 60% of the time is not a red flag; the same ratio on a discovery call is. Applying one rubric across call types systematically miscalibrates scores and produces invalid coaching signal. Revenue.io's February 2026 scorecard framework specifies different dimension sets for cold calls, discovery calls, demo calls, and late-stage calls.

---

### Call Type 1: Discovery / Qualification Call

**Primary coaching objective:** Was business pain established, quantified, and mapped to stakeholders before any product conversation began?

**Rubric adjustments:**

| Dimension | Adjustment |
|---|---|
| Discovery Quality | Weight effectively increases to 30 points for this call type. All five sub-criteria are mandatory — this is the call type where discovery should occur. |
| Conversation Dynamics | Talk ratio target: SE ≤45%. Flag if SE talk time exceeds 55%. Longest monologue threshold: 2 minutes (tighter than default). Question quality weighted heavily — open-ended questions should predominate by 70%+ ratio. |
| Value Alignment | Reduce weight: product should barely appear. If SE is demonstrating or pitching features extensively on a discovery call, that is itself a red flag — flag as "premature product introduction." |
| Next-Step Discipline | Full weight. Discovery calls must end with a confirmed next meeting (demo, POC scoping, technical deep-dive) with specific date/attendees. |
| Technical Credibility | Reduce weight — technical depth is not the primary objective of a discovery call. Score this dimension only if explicit technical questions arose. |
| Engagement Quality | Customer question count is especially meaningful here — Mindtickle's baseline of ~12 customer questions is most applicable to this call type. |

**Discovery-specific pass/fail signal:** If the SE moved to product demonstration or feature explanation before establishing any business pain, score Discovery Quality at 0/25 regardless of other behaviors. This is the "premature product" flag.

---

### Call Type 2: Technical Demo / Solution Presentation

**Primary coaching objective:** Was the demo scenario built from stated customer requirements, and were capabilities connected to business outcomes rather than presented as a feature tour?

**Rubric adjustments:**

| Dimension | Adjustment |
|---|---|
| Discovery Quality | Reduce weight to 15 points. A demo call may open with a brief discovery recap, but extensive discovery at demo stage is a pipeline health concern, not a coaching win. Score whether SE opened with a requirements check-in ("Before I start, let me confirm what you told us you needed — is that still accurate?"). |
| Conversation Dynamics | Talk ratio target: SE ≤60%. SE will naturally talk more during demo. However, question rate during demo should remain high — the SE should ask at least one engagement question per 10 minutes of demo content. Monologue threshold relaxed to 5 minutes for product explanation segments, but tightened for Q&A segments. |
| Value Alignment | Increase weight to 20 points. This is the primary success criterion for a demo call. Every capability shown should map to a stated requirement. Score this rigorously. |
| Next-Step Discipline | Full weight. Demo calls should end with a POC scope, architectural review, or stakeholder expansion meeting — not just "I'll send you the recording." |
| Technical Credibility | Full weight. This is the call type where technical questions concentrate. Score gap handling carefully — a demo call where the SE bluffed through a technical question is a high-risk indicator. |
| Engagement Quality | Score specifically for demo-phase engagement: Did the SE ask engagement questions that tested whether the customer was connecting features to their situation? ("Does that address the scenario you described?" not "Does that make sense?") |

**Demo-specific anti-patterns to flag:** Generic demo (no linkage to stated requirements), feature-completeness tour (showing everything the product does), and ending the demo without confirming POC success criteria or next milestone.

---

### Call Type 3: Executive / Business Case Presentation

**Primary coaching objective:** Did the SE translate technical capability into business language, and did the presentation address executive-level concerns (risk, cost, strategic fit) rather than technical function?

**Rubric adjustments:**

| Dimension | Adjustment |
|---|---|
| Discovery Quality | Reduce weight to 10 points. Discovery at executive stage is confirmatory, not exploratory. Score: Did the SE open with a reflection of the business situation back to the executive ("My understanding is that you're trying to solve X because of Y — is that accurate?")?  |
| Conversation Dynamics | Talk ratio target: SE ≤50%. Executive meetings should be more conversational. An SE who lectures an executive is a deal-risk indicator. |
| Value Alignment | Increase weight to 25 points. This is the primary dimension. Business outcomes, ROI framing, and risk/consequence framing are the scoring criteria. Technical feature explanations presented without business translation score 0 on this dimension. |
| Next-Step Discipline | Full weight. Executive calls with no agreed next step represent the highest-probability deal stall scenario. Score next-step specificity rigorously. |
| Technical Credibility | Reduce weight to 5 points. Executives generally do not probe technical depth. Score only if technical questions arose and how they were handled. |
| Stakeholder & Competitive Intel | Increase weight to 10 points. Executive meetings frequently surface buying committee composition and competitive strategy that is not available at lower levels. |

**Executive-specific flag:** If the SE used technical jargon, product acronyms, or feature-level language without business translation more than three times in the call, flag as "audience calibration failure." This is a separate signal from value alignment and should appear in the coaching output explicitly.

---

### Call Type 4: POC / Technical Evaluation Review

**Primary coaching objective:** Were POC success criteria defined and confirmed, was the evaluation bounded and manageable, and did the SE maintain commercial alignment throughout?

**Rubric adjustments:**

| Dimension | Adjustment |
|---|---|
| Discovery Quality | Reduce weight to 10 points. POC calls are in a late-stage qualification context. Score: Did the SE ask whether the POC results map to the original success criteria defined at deal outset? |
| Conversation Dynamics | Full weight. Technical evaluation reviews are collaborative — SE should be in listening and problem-solving mode, not pitching. |
| Value Alignment | Full weight but context-adjusted. "Value alignment" in a POC review means: did the SE connect POC outcomes back to the business case ("The fact that we passed your SSO test means your 40,000 users can be onboarded without the manual provisioning cost you described")? |
| Next-Step Discipline | Full weight. POC reviews must end with either: a confirmed decision meeting with economic buyer, a defined extension scope, or a documented pass/fail decision. Vague outcomes at POC stage indicate deal risk. |
| Technical Credibility | Full weight, highest scrutiny. POC calls are where technical objections concentrate. Score gap handling and over-commitment avoidance especially carefully. |
| Stakeholder & Competitive Intel | Full weight. POC review meetings frequently reveal whether competitive evaluations are running in parallel. Score whether the SE surfaced this. |

**POC-specific sub-criteria to add:**
- Did the SE define or confirm specific, measurable POC success criteria on this call?
- Did the SE avoid scope creep (adding evaluation scenarios beyond the agreed POC)?
- Did the SE confirm next step with economic buyer involvement (not just technical team)?

---

## Part D: The Coaching Report Template

*This is the complete output template for every call the skill analyzes. Sections are ordered by evidence-backed coaching effectiveness principles: strengths first (SBI-grounded, builds credibility), then development areas (with alternative approaches, reduces defensiveness), then transferable learning points (builds mental model, not just prescription), then one prioritized next-time action (prevents diffuse attention), then self-reflection prompt (activates ownership before manager debrief).*

---

```
═══════════════════════════════════════════════════════════════
SE CALL COACHING REPORT
Generated by /se-coaching-analysis
═══════════════════════════════════════════════════════════════

CALL METADATA
──────────────────────────────────────────────────────────────
Call date:          [YYYY-MM-DD]
Duration:           [X minutes]
Call type:          [Discovery / Demo / Executive / POC Review / Other]
  ↳ Identification: [One sentence explaining how call type was determined
                     from transcript content]
Participants:       SE: [Name or "SE" if not identified]
                    AE: [Name or "not identified"]
                    Customer: [Names/roles if named in transcript]
                    [Note: Additional participants may not be identifiable
                     from transcript alone]
Deal stage:         [If mentioned; "not stated" if absent]

SCORE SUMMARY
──────────────────────────────────────────────────────────────
Overall Score:  [X] / 100  →  [STRONG / DEVELOPING / NEEDS INTERVENTION]

  Discovery Quality             [X] / 25
  Conversation Dynamics         [X] / 20
  Value Alignment               [X] / 15
  Next-Step Discipline          [X] / 15
  Technical Credibility         [X] / 10
  Engagement Quality            [X] / 10
  Stakeholder & Competitive     [X] /  5

Score note: This score is a coaching index, not a performance evaluation.
It reflects transcript-observable behaviors only. See "Scoring Limitations"
section for what this analysis cannot assess.

[If trend data is available]:
  Last 3 calls: [Score] → [Score] → [Score (this call)]
  Notable trend: [One sentence on direction of key dimension]

═══════════════════════════════════════════════════════════════
SECTION 1: STRENGTHS
What the SE did well — behaviors to repeat deliberately
═══════════════════════════════════════════════════════════════

Two to three strengths, each following SBI structure:
Situation → Behavior → Impact → Transferable Principle

─ Strength 1: [Short skill label, e.g., "Business Impact Discovery"]

  Situation:   At approximately [timestamp / call phase], when [what was
               happening in the conversation — what the customer had just
               said or asked].

  Behavior:    [SE name / "The SE"] [specific observable action]:
               "[Direct quote or close paraphrase from transcript]"

  Impact:      [What the customer did or said in response that signals
               the behavior landed — e.g., "the customer volunteered
               three additional pain points unprompted" or "the customer
               said 'that's exactly our problem'"].

  Repeat because:  [One-sentence transferable principle — not "good job"
                   but "this worked because [mechanism]." Example:
                   "Restating the customer's problem in their own language
                   before asking the follow-up question signals you heard
                   them and converts monologue into dialogue."]

─ Strength 2: [Short skill label]

  [Same structure]

─ Strength 3: [Short skill label — include only if a third distinct
  strength is transcript-supported. Do not fabricate.]

  [Same structure]

═══════════════════════════════════════════════════════════════
SECTION 2: DEVELOPMENT AREAS
What to work on — with specific alternative approaches
═══════════════════════════════════════════════════════════════

Two to three development areas, each following SBI structure plus
alternative approach and rewrite example.

─ Development Area 1: [Short gap label, e.g., "Premature Product
  Introduction"]

  Situation:   At approximately [timestamp / call phase], when [what
               was happening].

  Behavior:    [Specific behavior that fell short]:
               "[Direct quote or close paraphrase from transcript]"

  Impact:      [What happened next that signals the gap mattered —
               e.g., "the customer's subsequent questions were all
               about pricing, not value" or "the customer went quiet
               for 40 seconds after this exchange"].

  Alternative approach:
               Instead of [what was said/done], try [specific technique
               or language pattern].

               Rewrite: "[A rewritten version of the specific moment —
               what the SE could have said that would score higher
               on this criterion. Keep it realistic and in the SE's
               apparent register, not a scripted template.]"

  Why it matters: "[One sentence connecting this gap to deal risk or
                   win-rate evidence — e.g., 'Gong's 2025 dataset shows
                   SE talk time above 65% consistently correlates with
                   lower win rates.']"

─ Development Area 2: [Short gap label]

  [Same structure]

─ Development Area 3: [Short gap label — include only if a third
  distinct gap is transcript-supported and meaningfully different
  from the first two.]

  [Same structure]

═══════════════════════════════════════════════════════════════
SECTION 3: LEARNING POINTS
Transferable principles — the "why" behind the what
═══════════════════════════════════════════════════════════════

Two to three learning points that convert specific call observations
into transferable principles the SE can apply to future calls.

─ Learning Point 1: [Short title, e.g., "The Customer's Question Is
  Not an Interruption — It's the Signal"]

  What happened on this call:
  [One sentence describing the specific observation.]

  The principle:
  [Two to three sentences explaining WHY this behavior produces
   the outcome it does. This is the mechanism, not the prescription.
   Example: "When a customer interrupts a demo to ask a question,
   they are telling you exactly what matters to them. SEs who treat
   this as an interruption keep walking; SEs who stop and explore
   the question discover what to emphasize for the rest of the call.
   The question is a discovery gift."]

  Where this applies:
  [One sentence identifying the call types or moments where this
   principle is most important — "this matters most in mid-demo,
   when the temptation to keep the flow intact is highest."]

─ Learning Point 2: [Short title]

  [Same structure]

─ Learning Point 3: [Short title — optional, only if a third
  genuinely distinct principle is supported by the call]

  [Same structure]

═══════════════════════════════════════════════════════════════
SECTION 4: NEXT-TIME ACTIONS
Maximum three behavioral commitments — prioritized by impact
═══════════════════════════════════════════════════════════════

[Priority] Action 1 (Highest Impact): [Action label]

  On the next [call type], when [specific trigger moment or scenario
  type], do [specific observable behavior].

  How to practice before then:
  [One concrete rehearsal suggestion — a role-play scenario, a
   sentence to memorize, a pre-call checklist item. Should be
   achievable in under 15 minutes of deliberate practice.]

  Success looks like:
  [One observable signal that the SE executed this action on the
   next call — what would appear in the transcript if it worked.]

Action 2: [Action label]

  [Same structure]

Action 3 (Optional): [Action label — only if it addresses a
distinct, high-priority gap]

  [Same structure]

Primary focus recommendation:
  Of the above, [Action 1 / 2] is the highest-leverage change for
  this SE based on the current scoring pattern. Practice this first.
  [One sentence of rationale.]

═══════════════════════════════════════════════════════════════
SECTION 5: SELF-REFLECTION PROMPT
To complete BEFORE the coaching debrief conversation
═══════════════════════════════════════════════════════════════

Before discussing this report with your manager, answer these
two questions in writing:

1. "What one moment on this call are you least satisfied with?
   What would you do differently?"

2. "What is one thing this call showed you about a gap in
   your current approach that you hadn't identified before?"

[Note for managers: The gap between the SE's answer to Q1 and
the primary development area in Section 2 is the most productive
starting point for the coaching conversation. If they identify
the same moment, you have alignment and can move directly to
practice. If they identify a different moment, explore why —
their observation may be valid and may not appear in the
transcript-based analysis.]

═══════════════════════════════════════════════════════════════
SECTION 6: SCORING LIMITATIONS
What this analysis cannot assess from the transcript
═══════════════════════════════════════════════════════════════

This coaching report is based on transcript analysis only.
The following dimensions are NOT captured and should be assessed
through direct observation or supplementary review:

  ✗ Demo visual quality and screen share execution
    (which screens were shown, UI responsiveness, demo environment
    stability) — requires video review

  ✗ Vocal delivery, tone, and confidence
    (pacing, emphasis, hesitation in voice) — requires audio analysis

  ✗ Pre-call preparation quality
    (whether the SE researched the account, reviewed prior
    conversations, built a customized demo environment)

  ✗ Post-call follow-through
    (whether the stated next steps were executed within agreed
    timeframes, follow-up quality and speed)

  ✗ Body language and in-person presence
    (not applicable to recorded virtual calls, but relevant for
    in-person engagements)

  ✗ Technical accuracy verification
    (this analysis scores the PATTERN of confidence, recovery,
    and honesty — not the technical correctness of claims made)

  ✗ Customer engagement beyond language signals
    (prospect sentiment visible only through non-verbal cues,
    reply behavior, and downstream engagement data)

These gaps are inherent to transcript-based analysis.
They do not reduce the validity of the dimensions this report
does score — they define its boundaries.

═══════════════════════════════════════════════════════════════
SOURCES & CONFIDENCE NOTES (for this call's scoring)
═══════════════════════════════════════════════════════════════

  Discovery scoring based on: Vivun Definitive Guide to PreSales
    KPIs; Revenue.io scorecard methodology (Feb 2026). Confidence: MEDIUM.

  Conversation dynamics benchmarks: Gong Labs, 326K+ calls,
    updated March 2025. Confidence: HIGH.

  Value alignment and demo linkage: Vivun (2x close rate finding).
    Confidence: MEDIUM (single study).

  Next-step timing: Gong 2025 (53% more next-step discussion in
    fast-closing deals). Confidence: HIGH.

  Call type determination: Inferred from transcript content.
    Confidence: [HIGH / MEDIUM / LOW — state if ambiguous].

═══════════════════════════════════════════════════════════════
END OF REPORT
Generated by /se-coaching-analysis | Research base: 2026-04-08
═══════════════════════════════════════════════════════════════
```

---

## Part E: Transcript Analysis Prompt Patterns That Work

### The Master Design Principle (Kalvium Labs, 2026)

The AI analysis is the easy part. The hard part is the rubric. Every prompt pattern below assumes the rubric is already written with precision: each criterion is binary (Yes/No), answerable from the transcript alone, and would produce the same answer if two independent human reviewers applied it. If the rubric is vague, no prompt engineering compensates.

---

### Pattern 1: Structured Rubric with JSON Output

*Source: Kalvium Labs build case study, 2026. Validated at 94% agreement with human reviewers.*

This is the highest-accuracy pattern for scorecard scoring. The system prompt defines each criterion as a checkable condition. Output is structured JSON containing per-criterion pass/fail, evidence quote (if passing), and timestamp/call-phase reference (if failing).

```
SYSTEM PROMPT:

You are a pre-sales coaching analyst reviewing a sales engineer's 
call transcript. Your role is to score the SE's performance against 
a specific rubric and produce structured coaching output.

SCORING RULES:
- Score only what is verifiable from the transcript. Do not infer 
  intent or assume behavior that is not evidenced by what was said.
- For each criterion: return "pass", "borderline", or "fail".
- If "pass" or "borderline": quote the specific transcript segment 
  that supports the score (verbatim or close paraphrase with timestamp 
  or phase marker).
- If "fail": identify the specific moment or phase where the behavior 
  should have occurred and did not.
- Do not score dimensions that cannot be determined from text (vocal 
  tone, visual demo quality, pre-call preparation).

CALL TYPE CONTEXT:
Call type identified as: [DISCOVERY / DEMO / EXECUTIVE / POC REVIEW]
Apply the call-type-specific scoring adjustments for this type.
If call type is ambiguous, note this and explain your inference.

RUBRIC:

DIMENSION 1: DISCOVERY QUALITY (25 points)
  1a. Pain Before Product (7 pts)
      CRITERION: Did the SE ask about business pain or current-state 
      challenges before mentioning product capabilities or asking for 
      a demo scenario?
      Pass = Yes, business pain was established before product 
             was introduced.
      Fail = Product, features, or demo were introduced before 
             any pain discovery occurred.
      
  1b. Business Impact Quantification (6 pts)
      CRITERION: Did the SE attempt to get the customer to quantify 
      their pain — attaching a number, time estimate, volume, or 
      frequency to the problem?
      Pass = Yes, a specific quantifying question was asked AND 
             the customer provided or attempted a specific metric.
      Borderline = Quantifying question asked but customer gave 
                   only qualitative answer, and SE did not probe further.
      Fail = No quantifying question asked.

  [Continue for all sub-criteria...]

DIMENSION 2: CONVERSATION DYNAMICS (20 points)
  2a. Talk Ratio (6 pts)
      CRITERION: Based on speaker turn analysis in the transcript, 
      is the SE's estimated talk share within the appropriate range 
      for this call type?
      Discovery call pass: SE estimated at ≤50% of total words spoken.
      Demo call pass: SE estimated at ≤65% of total words spoken.
      Fail: SE clearly dominates — customer responses are brief 
            acknowledgments rather than substantive dialogue.
      Note: You cannot calculate exact talk ratio from transcript 
            without timing data. Estimate based on relative word 
            counts and dialogue pattern. Flag if uncertain.

  [Continue for all sub-criteria...]

OUTPUT FORMAT (return as JSON):

{
  "call_metadata": {
    "call_type_identified": "[type]",
    "call_type_confidence": "[high/medium/low]",
    "call_type_reasoning": "[one sentence]",
    "duration_estimated": "[if inferrable]",
    "participants_identified": ["[list]"]
  },
  "dimension_scores": {
    "discovery_quality": {
      "total_score": [0-25],
      "sub_criteria": {
        "pain_before_product": {
          "score": [0-7],
          "result": "pass|borderline|fail",
          "evidence": "[quote or explanation]",
          "timestamp_or_phase": "[if applicable]"
        },
        [...]
      }
    },
    [...]
  },
  "overall_score": [0-100],
  "overall_band": "strong|developing|needs_intervention",
  "flags": {
    "premature_product_introduction": true|false,
    "talk_time_risk": true|false,
    "no_next_step": true|false,
    "audience_calibration_failure": true|false,
    "over_commitment_detected": true|false
  }
}
```

---

### Pattern 2: Speaker-Separated Analysis

*Source: Conversation intelligence platform design principles; Kalvium Labs finding that combined-transcript analysis produces noisier signal.*

Before passing transcript to the scoring model, separate speaker turns:

```
PRE-PROCESSING STEP (before scoring):

Parse the transcript into two separate streams:

SE_TURNS = [all utterances attributed to the sales engineer]
CUSTOMER_TURNS = [all utterances attributed to the customer]
JOINT = [full interleaved transcript with speaker labels]

For discovery quality scoring: use JOINT (context needed)
For talk ratio estimation: use JOINT with word counts per speaker
For question quality analysis: use SE_TURNS only
For customer engagement signals: use CUSTOMER_TURNS only
For objection handling: use JOINT (need the objection + SE response)

Do not analyze SE question quality against the full transcript —
customer statements can include question-shaped phrasing that 
would inflate the SE question count if not separated.
```

---

### Pattern 3: Per-Phase Analysis

*Source: Gong platform architecture, which segments calls by topic/phase before scoring.*

For long calls (over 45 minutes), per-phase analysis produces more actionable coaching than whole-transcript analysis:

```
PHASE SEGMENTATION PROMPT:

First, segment this transcript into call phases. Use the following
phase labels:
  - OPENING (first 5 minutes or until substantive conversation begins)
  - DISCOVERY (SE asking questions to understand customer situation)
  - PRESENTATION / DEMO (SE explaining product or demonstrating)
  - OBJECTION HANDLING (customer raising concerns, SE responding)
  - CLOSING / NEXT STEPS (final 5-10 minutes)
  - OTHER (transition moments, logistics, pleasantries)

For each phase identified, mark the approximate start and end 
(by paragraph number or timestamp if available).

Then score each dimension within the phase where it is most relevant:
  - Discovery quality: score within DISCOVERY phase only
  - Value alignment: score within PRESENTATION phase only
  - Next-step discipline: score within CLOSING phase only
  - Objection handling: score within OBJECTION HANDLING phase only
  - Conversation dynamics: score across all phases (pattern matters)

Scoring a behavior in the wrong phase produces misleading results.
If a phase is absent (e.g., no identifiable CLOSING), flag this as 
a structural gap before scoring next-step discipline.
```

---

### Pattern 4: Evidence-Grounded Coaching Narrative

*Source: Kalvium Labs finding that Claude 3.5 Sonnet produced better failure explanations; Gong's model of providing transcript evidence alongside each coaching observation.*

After JSON scoring is complete, generate coaching narrative in a second call:

```
COACHING NARRATIVE PROMPT:

You have scored the following call. Now generate the coaching report
sections using the evidence from the scoring output.

RULES FOR COACHING NARRATIVE:
1. Every strength and development area must quote or closely 
   paraphrase a specific transcript moment. No generic statements.
   ("You handled objections well" is rejected. "When the customer 
   raised the SSO concern at [phase], you said '[quote]'" is accepted.)

2. Every development area must include an ALTERNATIVE APPROACH with 
   a rewritten version of the specific moment. The rewrite should 
   sound like this SE — do not produce a scripted template.

3. Learning points must explain the MECHANISM, not repeat the 
   prescription. "Ask follow-up questions" is not a learning point.
   "When a customer gives a short answer to a discovery question, 
   it usually means they don't know how to elaborate — a follow-up 
   question that offers a frame ('is this more of a cost concern or 
   a time concern?') produces more information than silence does" 
   is a learning point.

4. Recommend a MAXIMUM of two development areas and three next-time
   actions. If more gaps exist, prioritize by impact on win rate.
   Coaching lists longer than three items are not absorbed.

5. For Technical Credibility: state explicitly that this analysis 
   scores the PATTERN of confidence and honesty, not the accuracy 
   of technical claims. Flag this caveat in the report.

6. Self-reflection prompt: produce ONE question that targets the 
   specific gap most likely to create a productive debrief 
   conversation for THIS SE based on THIS call. Do not use 
   the generic template question if a more targeted one is 
   available from the transcript.

INPUT: [JSON scoring output from Pattern 1]
TRANSCRIPT: [full labeled transcript]
CALL TYPE: [identified call type]
```

---

### Pattern 5: Trend-Aware Scoring (Multi-Call Context)

*Source: OSKAR coaching model; Gong's longitudinal coaching tracking.*

When multiple call transcripts are available for the same SE:

```
TREND ANALYSIS PROMPT:

You have scored [N] calls for [SE name / identifier] over the 
following dates: [dates].

For each of the following dimensions, identify:
  1. The score on each call (chronological)
  2. The direction of trend (improving / stable / declining)
  3. Whether the SE appears to be working on a previously 
     identified coaching target (look for improvement in dimensions 
     that scored poorly on the first call)

Dimensions to trend:
  - Discovery quality (overall and sub-criteria)
  - Talk ratio (direction)
  - Next-step specificity
  - Objection handling pattern

Flag: If a dimension shows consistent failure across 3+ calls, 
      this requires an escalated coaching conversation, not 
      another coaching report.

Output: Add a "Trend Note" section to the coaching report that 
shows: [Last score → This score] for each dimension, with a 
one-sentence observation on the most meaningful movement 
(or absence of movement).

Do not fabricate trend data. If only one call is available, 
state this and omit the trend section.
```

---

## Part F: Anti-Patterns — What the Skill Should NOT Do

### Anti-Pattern 1: Generic Feedback Without Transcript Grounding

**What it looks like:** "You did a good job on discovery. You could work on your talk ratio."

**Why it fails:** Generic feedback does not change behavior. The SE has no specific moment to replay, rewrite, or practice. Research from CEB/Gartner on sales coaching (cited in SBI Growth 2017 report) consistently shows that feedback without specificity produces no measurable behavior change.

**The fix:** Every observation in the output must reference a specific moment — a quote, a timestamp, a phase marker. If the transcript does not contain evidence for a claim, do not make the claim.

---

### Anti-Pattern 2: Scoring Behaviors That Cannot Be Verified From Transcript

**What it looks like:** "The SE appeared well-prepared and had clearly done pre-call research." Or: "The SE's tone was confident and professional."

**Why it fails:** Pre-call preparation is not verifiable from transcript. Tone requires audio analysis. Scoring these dimensions from text produces confabulation — the model asserts something it has no basis for assessing. Kalvium Labs found this pattern destroys trust in the coaching output: one fabricated observation causes the SE to discount the entire report.

**The fix:** The Scoring Limitations section must appear in every report and must be specific about what cannot be assessed. The Technical Credibility dimension must include a caveat that it scores pattern-of-honesty, not technical accuracy.

---

### Anti-Pattern 3: Scoring Talk Ratio Without Call-Type Context

**What it looks like:** Flagging an SE for 58% talk time on a demo call as a performance failure.

**Why it fails:** Gong's research explicitly distinguishes discovery call benchmarks (43% SE talk time) from demo call patterns (naturally higher). A single talk ratio threshold applied across call types produces incorrect scores and coaching that contradicts the SE's lived experience — destroying credibility with technically sophisticated SEs.

**The fix:** Call type must be identified before any conversation dynamics dimension is scored. The scoring thresholds must adjust by call type as specified in Part C. If call type cannot be determined from the transcript, flag this uncertainty and note that conversation dynamics scoring may be miscalibrated.

---

### Anti-Pattern 4: More Than Three Development Areas

**What it looks like:** A coaching report that identifies seven gaps and produces nine action items.

**Why it fails:** John Care's T3-B3-N3 model and Force Management's debrief framework both specify a maximum of two to three improvement areas per coaching session. Revenue.io's February 2026 scorecard framework explicitly notes that a focused scorecard outperforms a comprehensive one. A coaching output that tries to fix everything simultaneously fixes nothing. SEs who receive extensive correction lists become defensive; SEs who receive one or two specific, actionable targets change behavior.

**The fix:** The coaching narrative should identify a maximum of two development areas, regardless of how many scoring gaps exist. The "Primary focus recommendation" in Section 4 of the report template enforces single-priority discipline. If more than three development areas are present, the skill should select the two with the highest impact on win rate (discovery quality first, then conversation dynamics) and surface the others only in the score summary.

---

### Anti-Pattern 5: Compound Questions in the Rubric

**What it looks like:** Rubric criterion: "Did the SE identify pain AND quantify its business impact AND connect it to stakeholder concerns?"

**Why it fails:** Compound criteria cannot be scored Yes/No reliably. An SE who identified pain and quantified it but did not connect it to stakeholders would score as a partial pass — which the model then must adjudicate arbitrarily. Revenue.io, Gong, and Chorus documentation all explicitly prohibit compound questions in scoring rubrics.

**The fix:** Each compound criterion in this specification has been decomposed into separate sub-criteria (see Part B). Every sub-criterion is independently answerable Yes/No. The point allocation per sub-criterion reflects its relative importance.

---

### Anti-Pattern 6: Confusing Customer Engagement with SE Quality

**What it looks like:** Scoring an SE low on engagement because the customer was quiet, even though the SE did everything correctly.

**Why it fails:** Customer engagement is a proxy for SE performance, not a direct measure. A customer who has already decided not to buy, or who is in a screening call under instructions from their manager, may be quiet regardless of SE quality. Mindtickle's 12-question baseline is a population average, not a per-call threshold.

**The fix:** Engagement Quality scores the SE's *behaviors that invite engagement* (question quality, objection handling, affirmation invitations) — not the customer's *response level* in isolation. Customer questions, affirmations, and vocabulary adoption are treated as confirmatory signals, not primary scoring inputs. If the customer was notably unresponsive, the coaching report should flag this as a contextual note rather than a scoring driver: "Note: Customer engagement was low throughout this call. This may reflect account-specific context not visible in the transcript. Score interpretation should incorporate AE's deal context."

---

### Anti-Pattern 7: Treating the Score as a Performance Evaluation

**What it looks like:** Manager using coaching scores in a performance review context ("Your average score this quarter was 61/100").

**Why it fails:** The scoring model is calibrated for coaching signal, not performance evaluation. It weights discovery heavily because that is the highest-leverage coaching target — not because an SE who scores poorly on discovery should be placed on a performance plan. Using coaching indexes as evaluation metrics creates perverse incentives (gaming the transcript-observable behaviors) and destroys the psychological safety required for honest coaching.

**The fix:** The report template explicitly labels the score as a "coaching index, not a performance evaluation." The skill output should include this label as a fixed element. Trend data is appropriate for coaching conversations; aggregate score data should not be exported to performance management systems without explicit design of a separate evaluation rubric.

---

### Anti-Pattern 8: Analyzing the Transcript Without Speaker Diarization

**What it looks like:** Feeding a transcript where speaker turns are not labeled, or where "Speaker 1" / "Speaker 2" have not been mapped to SE and customer.

**Why it fails:** Kalvium Labs' analysis found that analyzing a combined unlabeled transcript produces noisier signal. The model may attribute customer statements to the SE (inflating question count, talk time, or objection-handling scores) or vice versa. This produces confidently wrong scores.

**The fix:** Speaker diarization is a prerequisite. The skill should require that the transcript input includes speaker labels, or apply a pre-processing step to identify SE vs. customer turns before scoring. If speaker labels cannot be reliably assigned (e.g., three or more participants not labeled), the skill should return a warning and limit analysis to dimensions where speaker identity is not required.

---

## Part G: Knowledge Gaps and Limitations

### Gap 1: Vivun 2x Close Rate Finding — Single Study, Limited Methodology Transparency
**Confidence: MEDIUM.** The Vivun Definitive Guide to PreSales KPIs cites the 2x close rate correlation with best-practice discovery as a study conducted within their customer base. The company is a business spend management platform — the generalizability to cybersecurity, identity management, and other enterprise technology segments is not established. The specific control variables, sample size, and methodology are not published.
**Follow-up:** Seek replication studies or segment-specific data from Gartner or Forrester's presales effectiveness research (check Forrester's 2025 B2B Sales Benchmark report for SE-specific conversion data).

### Gap 2: Market Share Figures for Conversation Intelligence Platforms
**Confidence: LOW.** Gong, Clari, and Chorus relative market share figures cited in the platform comparison are based on 2024 estimates. Gong's 2025 revenue run-rate and Clari's acquisition activity since 2024 may have shifted the competitive landscape materially.
**Follow-up:** Check Gartner's 2025 Revenue Intelligence Market Guide (expected Q3 2025 publication) and G2 category reviews for updated install-base data.

### Gap 3: No SE-Specific Win Rate Data by Conversation Behavior
**Confidence: MEDIUM.** All conversation dynamics benchmarks (talk ratio, question count, monologue length) are from Gong's general sales dataset — not SE-specific. SEs may have systematically different baseline patterns than account executives, and the win-rate correlations may not transfer directly.
**Follow-up:** Gong's research team has published segment-specific analyses in prior years. Request SE-specific data from their research team, or analyze a proprietary dataset of SE calls correlated with technical win outcomes.

### Gap 4: MEDDPICC Adoption Rate
**Confidence: MEDIUM.** The "73% of SaaS companies selling above $100K ARR" figure for MEDDPICC adoption is sourced from a Salesforce-published statistic. The original survey methodology is not specified. This figure may be self-reported by Salesforce customers or based on a non-representative sample.
**Follow-up:** Cross-reference with Pavilion (formerly Revenue Collective) annual survey data or SBI Growth methodology research for independent confirmation.

### Gap 5: Absence of Published Numeric SE Scoring Rubric from PreSales Collective or Presales.rocks
**Confidence: HIGH that the gap is real.** Multiple searches of PreSales Collective's published content and presales.rocks resources found no publicly accessible numeric scoring rubric. The frameworks referenced from these sources are qualitative debrief and coaching frameworks. The 100-point scoring model in this specification is a synthesis from multiple sources, not a documented industry standard.
**Implication:** The weights assigned in this model should be treated as defensible starting points, not validated benchmarks. They should be recalibrated after 20–30 calls have been scored and win-rate correlations can be analyzed against the model's dimension scores.

### Gap 6: Post-Call Engagement Tracking Not Covered
**Confidence: HIGH that the gap is real.** Commercial platforms (Gong, Clari) combine transcript-based conversation scoring with post-call engagement signals (prospect email reply rates, meeting acceptance, content open rates) for deal intelligence scoring. This skill covers only the conversation layer. The deal health implications of the gap are material for POC and late-stage call types where prospect engagement behavior is the primary signal.
**Follow-up:** Consider whether the skill should accept supplementary inputs (CRM activity data, email response metadata) to enable a lightweight deal health overlay on top of the conversation quality score.

---

## Recommendations & Next Steps

*Prioritized by impact on skill quality and feasibility of implementation.*

### Priority 1 (Immediate — Before Build): Validate the Rubric Against 5–10 Winning Calls

**Specific action:** Before writing a single line of the skill's code, identify 5 calls your organization has assessed as strong SE performances (deals that advanced to POC or closed) and 5 that were assessed as weak. Score them manually using the rubric in Part B. If the rubric scores the winning calls 15+ points higher than the losing calls on average, the rubric has predictive validity for your context. If the scores do not separate, the rubric needs adjustment before the skill will produce reliable coaching.

**Evidence base:** Revenue.io's published framework (Feb 2026) specifies this validation step as a prerequisite: "Build from winning calls, not from theory." Kalvium Labs' finding that the rubric quality problem required two days of client workshops before the AI could work should be treated as a direct warning about skipping this step.

**Feasibility:**