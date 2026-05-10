# LinkedIn Post

---

Most companies deploying AI agents haven't asked a basic question: what identity does that agent actually run as?

The answer, more often than not, is a shared service account that's been around for years, has access to half the environment, and gets rotated never.

That's not an AI problem. It's an identity problem that AI just made much worse.

When a human employee needs access to a system, we have a process for it. They request it, someone approves it, and if things go sideways there's an audit trail pointing to a person. When that same access is handed to an AI agent running as a generic service account, none of that infrastructure applies. The agent can read documents, call APIs, query databases, and send messages, and the logs just say "svc-ai-prod." That's not accountability.

The attack surface is also completely different. A human account with excessive permissions is a risk. A service account with excessive permissions that's embedded in an AI agent, integrated with your data sources, and capable of taking autonomous actions is a different category of problem. Credential theft isn't the only threat vector. Prompt injection, jailbreaking, and supply chain compromise can all result in an agent doing something it wasn't supposed to, with access it never should have had.

The fix isn't complicated in principle: treat AI agents as first-class identities. Dedicated accounts, scoped to exactly the workflows they need. Lifecycle management. Access reviews. Logging that captures enough context to reconstruct what the agent did and why it was authorized to do it.

We've done this for privileged human accounts for years. We just haven't applied the same discipline to machine identities.

Are the AI projects at your company going through identity review before they go live?

#aiagents #identitysecurity #nhi #zerotrust #machineidentity

---

# Rationale

**Hook choice:** Opens with the specific diagnostic question that most organizations aren't asking. "What identity does that agent actually run as?" is concrete and forces the reader to think about a gap they probably haven't closed. The first two sentences together do the work: here's the question, here's the embarrassing answer.

**Structure used:** Hook (the unasked question) -> Present reality (shared service accounts, the why) -> Reframe (this isn't an AI problem, it's an identity problem AI amplified) -> Human vs. agent accountability contrast (audit trail argument) -> Expanded threat surface (why agents are categorically different, not just incrementally worse) -> The fix stated plainly (first-class identities, scoping, lifecycle, logging) -> Closing callback (we've done this before, for humans) -> Discussion question.

**Voice choices:** No em dashes. Direct assertions throughout. "Credential theft isn't the only threat vector" is the kind of specific technical assertion that lands with security practitioners. The service account detail ("svc-ai-prod") is a realistic, named example that makes it concrete without making it about any particular company. Contractions used throughout. No hedges.

**Word count:** Approximately 320 words — slightly above the 300-word sweet spot but justified by the dual-threat argument (accountability gap + expanded attack surface), which needs the space to land with specificity rather than feeling like a slide deck bullet.

**Link note:** No URLs in the post body. If Craig wants to reference Okta's NHI or AI agent governance capabilities, put the link in the first comment.
