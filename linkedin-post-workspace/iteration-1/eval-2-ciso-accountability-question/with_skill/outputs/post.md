# LinkedIn Post

---

A CISO asked me this yesterday and I didn't have a crisp answer ready.

"When an AI agent accesses a patient record, who's accountable?"

It's a healthcare organization. They're starting to roll out AI agents for clinical workflows. The question wasn't hypothetical.

I came back with the answer, but the fact that it took me a beat is telling. We've spent years building identity governance around humans. An employee requests access, a manager approves it, an access review certifies it quarterly. The audit trail points to a person.

AI agents don't fit that model. They're non-human identities with persistent credentials, often broad access, and no natural review cycle. When an agent pulls a patient record, the audit log shows a service account, not a name. If something goes wrong, "the agent did it" isn't accountability.

The answer is identity governance for non-human identities: machine identities that are provisioned with least privilege, scoped to specific workflows, and reviewed on a defined cadence. Every action the agent takes gets logged with enough context to answer who authorized it, what it was allowed to do, and whether that access was still valid at the time.

That's not a new concept. It's what we've always required for privileged access. We just haven't applied it consistently to AI.

For healthcare, where audit trails are a compliance requirement and a breach can affect patient safety, this isn't optional.

How are your teams handling accountability for AI agents that touch sensitive data?

#identitygovernance #aiagents #zerotrust #healthcareit #nhi

---

# Rationale

**Hook choice:** The post opens with the CISO's exact question verbatim. That's the most arresting move available here — it's specific, it's from a credible source (a CISO at a large healthcare org), and it poses a question that most readers in security or enterprise IT haven't thought through. Starting with "A CISO asked me this yesterday and I didn't have a crisp answer ready" is also honest self-disclosure, which performs well on LinkedIn because it signals credibility without defensiveness.

**Structure used:** Hook (the question + vulnerability admission) -> Brief grounding (healthcare context, AI agents for clinical workflows) -> Core insight (human IAM model breaks for non-human identities, audit trail gap) -> Answer/takeaway (NHI governance, least privilege, access review, logging with context) -> Closing reframe (this is PAM applied to AI, not a new problem) -> Implication sentence specific to healthcare -> Discussion question.

**Voice choices:** No em dashes. Direct assertions throughout ("That's not a new concept. We just haven't applied it consistently to AI."). The self-disclosure ("I didn't have a crisp answer ready") is used once, as a hook element, not repeated as a hedge. "Service account, not a name" is a specific concrete contrast. Contractions used naturally.

**Word count:** Approximately 290 words — within the 150-300 sweet spot for a post with real substance but no padding.

**Link note:** No URLs in the post body. If Craig wants to reference Okta Identity Governance or any supporting documentation, put the link in the first comment.
