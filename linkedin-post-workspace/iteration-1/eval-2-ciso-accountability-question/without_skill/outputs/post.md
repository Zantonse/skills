A CISO asked me a question yesterday I didn't have a crisp answer to.

We were in a meeting talking about AI adoption in their clinical workflows. Healthcare org, serious security posture. Then she paused and asked:

"When our AI agent accesses a patient record — who's accountable?"

I gave a decent answer in the moment. But not a crisp one. That bothered me on the drive home.

Here's the answer I should have given:

The accountability gap in AI agents isn't a new problem. It's the same identity governance problem we've had with service accounts for 20 years — just faster, more autonomous, and now touching PHI.

When a human accesses a patient record, the audit trail is clear: a person authenticated, accessed the record, and their identity is logged. If something goes wrong, you know who to call.

When an AI agent does it, you need the same thing: a non-human identity with a defined owner, scoped permissions, and a complete audit trail of every action the agent took — what it accessed, when, and why.

Three things that have to be in place:

1. **Every AI agent gets a machine identity** — not a shared service account, not borrowed credentials. Its own identity with an owner (a human or team) who is accountable for its behavior.

2. **Least privilege, enforced** — the agent gets access to exactly what it needs for the task, nothing more. In healthcare, that means access scoped to the specific workflow, not a blanket read on the patient database.

3. **An immutable audit log** — every record access, every action, timestamped and signed. Not just for compliance. For explainability. When a regulator or a patient asks "why did the AI look at my record," you need to be able to answer.

The CISO's question wasn't really about AI. It was about whether your identity governance program has caught up to your AI adoption pace.

For most organizations I talk to, the honest answer is: not yet.

That's the gap worth closing before the next AI workflow goes to production.

---

Okta | Identity Governance | Non-Human Identity | Healthcare Security | AI Security
