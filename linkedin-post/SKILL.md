---
name: linkedin-post
description: Write a LinkedIn post in Craig Verzosa's authentic voice. Trigger this skill whenever the user wants to write, draft, or create a LinkedIn post — whether they hand you a rough topic idea, bullet points, a story from a call or event, an existing draft, or anything to turn into a post. Also trigger for: "post about X", "help me write a LinkedIn", "draft a post", "turn this into a LinkedIn post", "write something for LinkedIn about", or any variation. Don't wait for explicit "use the LinkedIn post skill" language — if the intent is a LinkedIn post, use this.
---

## What you're building

A polished LinkedIn post in Craig's voice, ready to copy-paste. No generic AI-sounding content. No corporate preamble. Just a sharp, specific post that sounds like him.

Output two things:
1. **The post** — formatted for LinkedIn, ready to use
2. **Rationale** (3-5 lines) — what hook you chose and why, what structure you used

---

## Craig's Voice (adapted for LinkedIn)

Craig is an Okta Sales Engineer. His natural register is direct, technically precise, and low-hedge. These rules govern the post:

**Always do:**
- Open with substance — the hook IS the point, no "I'm excited to share" or "Wanted to take a moment to..." preamble
- Make direct assertions — state what you observed, not what someone "might want to consider"
- Use exact names: product names, company names, real numbers, specific scenarios (this is what makes a post credible)
- Use contractions naturally: couldn't, isn't, don't, we've, they're
- Give the reader brief grounding before the insight — context, then observation, then implication
- End with a genuine, specific question that invites real discussion (not a rhetorical one, not a generic "what do you think?")

**Never do:**
- Em dashes — use a comma or period instead
- Corporate jargon: best-in-class, synergy, leverage (as verb), exciting, thrilled, honored, game-changer
- Hedge language as a social softener: "maybe", "I think", "could be" — only hedge when genuine product uncertainty warrants it
- Walls of text — white space is a feature on LinkedIn, use it

---

## LinkedIn Post Mechanics

**The hook is everything.**
Only the first ~150 characters show before "see more." Most people won't click. Start with the most interesting, specific, or counter-intuitive thing — not the setup, not the context.

Good hook: "Most AI agent demos break at identity. Here's the part nobody talks about."
Bad hook: "Had a great conversation with a customer last week and wanted to share some thoughts."

**Structure that works:**
- Hook (1-2 lines — the arresting thing)
- Brief grounding context if needed (2-3 lines max)
- Core insight or observation (2-4 lines)
- Implication or takeaway (1-2 lines)
- Question to drive comments (1 line)

**Formatting rules:**
- Blank line between every paragraph — LinkedIn renders this as breathing room and it dramatically improves readability on mobile
- Prose over bullet lists — bullets feel like slide decks; prose feels like a person
- 150-300 words is the sweet spot; up to 500 for a story with real tension
- 3-5 hashtags at the very end, lowercase, relevant

**One hard rule:** No hyperlinks in the post body — they suppress algorithmic reach. If there's a URL worth sharing, tell the user to put it in the first comment and note that in your rationale.

---

## Handling different input types

**Rough topic ("write a post about X"):**
Check if there's a specific angle or story worth anchoring to. If not, write from the topic — but note in your rationale that a real story or specific observation would make it stronger, and suggest a concrete direction.

**Bullet points:**
Find the most interesting tension or counter-intuitive point. That's your hook. Build the post around it, not around the list.

**Story or experience:**
Identify the moment of insight — the specific thing that made it worth sharing. Start the post there, not at "I was in a meeting..." Open with what you learned or observed, then let the story provide the supporting context.

**Existing draft:**
Diagnose what's weak (usually: too slow an opener, too many hedges, too generic). Rewrite applying the voice rules. Don't change the substance, just the shape and word choices. Show the rewrite, not a list of edits.

---

## Audience

Craig's LinkedIn spans security practitioners, enterprise buyers, fellow SEs, and a general professional network. Write so a non-Okta person grasps the point without explanation, but don't dumb down the technical substance. Specificity is what makes it credible to the technical readers and interesting to everyone else.
