---
name: se-coaching-analysis
description: |
  Analyze SE call transcripts and score performance out of 100 with dimensional breakdown,
  coaching insights, and actionable next steps. Reads VTT/TXT transcripts or pasted text,
  auto-detects call type (discovery, demo, POC, competitive, executive, QBR, follow-up),
  and produces a structured coaching report with transcript-grounded strengths, development
  areas with alternative approaches, transferable learning points, and behavioral commitments.
  Use this skill whenever the user mentions "score my call", "coach me on this call",
  "analyze this transcript", "how did I do on that call", "SE coaching", "call review",
  "rate my demo", "call score", "coaching report", or pastes/references a call transcript
  and wants performance feedback. Also trigger when the user says "T3-B3-N3", "what went
  well", "call debrief", or wants to improve their SE skills from recorded calls.
---

# SE Call Coaching Analysis

Read a call transcript. Score the SE's performance out of 100. Produce a coaching report
with transcript-grounded insights. Every observation cites a specific moment from the call.

Read `references/scoring-rubric.md` for the complete 100-point scoring model, call-type
adjustments, and coaching report template.

---

## How It Works

### Step 1: Identify Call Type

From the transcript, classify the call as one of:

| Type | Signals in Transcript |
|------|----------------------|
| **Discovery** | Questions about current state, pain, stakeholders. No product shown. |
| **Demo** | Screen sharing references, "let me show you", product walkthrough |
| **POC/Eval** | Success criteria, test results, environment setup |
| **Competitive** | Competitor names, comparison questions, bake-off references |
| **Executive** | CxO titles, business outcomes, strategic language, short call |
| **QBR** | Review of metrics, renewal, expansion, value realized |
| **Follow-up** | References to prior call, next steps, async context |

If unclear, ask. The call type determines which scoring adjustments apply.

### Step 2: Identify Speakers

Parse the transcript to identify:
- **SE** (the person being coached)
- **AE** (if present)
- **Customer contacts** (names, titles if available)

If the transcript uses speaker labels (Speaker 1, Speaker 2), ask the user to identify
which speaker is the SE.

### Step 3: Score Across 7 Dimensions (100 Points)

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| **Discovery Depth** | 25 pts | Did SE excavate business pain before presenting? Quality of questions? Stakeholder mapping? |
| **Value Alignment** | 20 pts | Were capabilities tied to customer-stated pain? Proof points relevant? CotM before/after framing? |
| **Listening & Interactivity** | 15 pts | Talk ratio (target: SE <50% in discovery, <60% in demo). Question distribution. Monologue length. |
| **Objection Handling** | 15 pts | Acknowledged concern? Probed root cause? Addressed with evidence, not defensiveness? |
| **Technical Credibility** | 10 pts | Accurate answers? Honest about gaps? "I'll confirm" over confident wrong answers? |
| **Next Step Discipline** | 10 pts | Specific action + owner + date? Or vague "let's follow up"? |
| **Presence & Collaboration** | 5 pts | AE-SE handoffs clean? Audience-appropriate depth? Composure under pressure? |

**Scoring per dimension:**
- **90-100%**: Exceptional — would use as a training example
- **70-89%**: Strong — solid execution with minor refinements
- **50-69%**: Developing — key behaviors present but inconsistent
- **30-49%**: Needs coaching — significant gaps in this dimension
- **0-29%**: Critical — fundamental skill not demonstrated

### Step 4: Call-Type Scoring Adjustments

| Call Type | Adjust Up | Adjust Down |
|-----------|-----------|-------------|
| **Discovery** | Weight Discovery Depth to 30 pts (steal 5 from Value Alignment) | Technical Credibility less relevant |
| **Demo** | Value Alignment to 25 pts | Discovery Depth to 20 pts (some should be pre-done) |
| **Executive** | Presence & Collaboration to 10 pts | Technical Credibility to 5 pts (answer only when asked) |
| **POC** | Technical Credibility to 15 pts | Presence to 5 pts |
| **Competitive** | Objection Handling to 20 pts | -- |
| **QBR** | Value Alignment to 25 pts (realized value storytelling) | Discovery Depth to 15 pts |

### Step 5: Produce the Coaching Report

```
SE CALL COACHING REPORT
═══════════════════════════════════════════════════

Call: [Type] | Date: [Date] | Duration: [Minutes]
Attendees: SE: [Name] | AE: [Name] | Customer: [Names/Titles]
Deal Stage: [If known]

OVERALL SCORE: [XX] / 100

┌─────────────────────────┬────────┬───────┐
│ Dimension               │ Weight │ Score │
├─────────────────────────┼────────┼───────┤
│ Discovery Depth         │   25   │  XX   │
│ Value Alignment         │   20   │  XX   │
│ Listening & Interactivity│  15   │  XX   │
│ Objection Handling      │   15   │  XX   │
│ Technical Credibility   │   10   │  XX   │
│ Next Step Discipline    │   10   │  XX   │
│ Presence & Collaboration│    5   │  XX   │
└─────────────────────────┴────────┴───────┘

KEY METRICS:
• Talk ratio: SE [X]% / Customer [X]%
• Questions asked by SE: [N] (open: [N], closed: [N])
• Longest SE monologue: ~[N] minutes
• Customer questions: [N]
• Next step: [Specific / Vague / None]
```

**Section 1: STRENGTHS (What You Did Well)**

3 specific moments from the transcript using SBI format:

> **[Skill Label]** (Dimension: [X], Score contribution: +[N])
>
> **Situation:** At [timestamp/context], when [what was happening]...
> **Behavior:** You [specific action — quote the transcript]
> **Impact:** The customer [responded/reacted — quote if possible]
>
> *Pattern to reinforce:* [One-sentence transferable principle]

**Section 2: DEVELOPMENT AREAS (What to Work On)**

2-3 specific moments, same SBI format, with alternative approach:

> **[Gap Label]** (Dimension: [X], Score impact: -[N])
>
> **Situation:** At [timestamp/context], when [what was happening]...
> **Behavior:** You [specific action — quote the transcript]
> **Impact:** The customer [response that signals the gap]
>
> *Alternative approach:* Instead of "[what you said]", try:
> "[Specific rewritten language the SE could have used]"

**Section 3: LEARNING POINTS**

2-3 transferable principles (not call-specific — applicable to future calls):

> **[Learning Point Title]**
> What happened: [One sentence from this call]
> The principle: [Why this pattern works or doesn't — transferable to other calls]
> Where this applies: [Types of calls or moments where this matters most]

**Section 4: NEXT-TIME ACTIONS**

Maximum 3 behavioral commitments:

> **Action 1: [Label]**
> On your next [call type], when [specific trigger], do [specific behavior].
> How to practice: [One rehearsal suggestion]

**Section 5: SELF-REFLECTION PROMPT**

> Before discussing this report: What moment on this call are you least
> satisfied with, and what would you do differently?

---

## Scoring Rules

1. **Every score must cite transcript evidence.** "Discovery was weak" is not scoring.
   "SE asked zero questions about business impact in the first 15 minutes, jumping
   directly to 'let me show you our dashboard'" is scoring.

2. **Binary checks first, then quality.** For each dimension, first check: did the
   behavior occur at all? (Binary.) Then: how well was it executed? (Quality scale.)

3. **Calibrate to call type.** A demo with 55% SE talk time scores differently than
   a discovery call with 55% SE talk time. The demo might be fine; the discovery isn't.

4. **Positive before constructive.** Strengths section always comes first. This builds
   trust in the report's fairness before presenting development areas.

5. **One primary focus.** The "Suggested focus for next call" in the footer should name
   ONE dimension. Trying to fix everything at once fixes nothing.

6. **Quote the transcript.** Every coaching observation references specific words from
   the call. "You handled that objection well" is worthless. "When the CTO said 'we're
   concerned about vendor lock-in,' you responded with 'that's a fair concern — let me
   show you our open standards approach' — that acknowledgment before response is what
   kept the conversation productive" is coaching.

---

## What This Skill Cannot Assess (Transparency)

Flag these limitations in every report:

- **Demo quality** — screen share content, UI navigation, demo environment quality
- **Vocal delivery** — tone, pace, confidence (transcript only captures words)
- **Body language** — engagement signals visible on video but not in text
- **Post-call execution** — whether follow-up was sent, CRM updated, etc.
- **Pre-call preparation quality** — whether research was done beforehand

Note: "This analysis scores what was SAID on the call. Demo execution quality,
vocal delivery, and post-call follow-through require separate evaluation."

---

## Anti-Patterns (What This Skill Must NOT Do)

1. **Never score without evidence.** If a dimension can't be assessed from the transcript
   (e.g., no objections occurred, so objection handling is untestable), mark it N/A
   and adjust weights proportionally. Do not guess.

2. **Never fabricate positive feedback.** If the call was weak, say so with specificity
   and compassion. Inflated scores erode trust in the tool.

3. **Never give more than 3 development areas.** Research shows more than 3 creates
   defensiveness and diffuses focus. Pick the highest-impact 2-3.

4. **Never use adjectives without evidence.** "Good job on discovery" fails.
   "Asked 4 open-ended questions about business impact before presenting" passes.

5. **Never score the AE.** This tool coaches the SE. AE behavior may be noted as context
   but is not scored.
