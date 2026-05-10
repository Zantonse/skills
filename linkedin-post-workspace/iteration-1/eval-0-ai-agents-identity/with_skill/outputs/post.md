Most AI agents running in production today don't have their own identity. They borrow one.

The pattern is almost universal: a shared service account, probably used by 3-5 other systems, with credentials that haven't rotated in 18 months. The team ships the agent fast, it works, and nobody asks what principal it's acting as.

This creates a real problem that won't show up until something goes wrong. When an AI agent exfiltrates data, you need to know exactly what it accessed and when. With a shared service account, that attribution is gone. Every other system sharing that identity is now in scope for the investigation. What started as an AI incident becomes a full credential compromise.

The fix isn't complicated. Agents need their own machine identities, scoped to exactly what they need, with full audit trails. Workload identity, short-lived credentials, least-privilege access. This is solved infrastructure for human users. It's barely on the roadmap for AI agents at most companies.

The governance gap isn't malicious, it's just that the tooling for human IAM has a 20-year head start. AI agents are being deployed like it's 2005 and shared service accounts were acceptable.

Are you seeing companies ask about agent identity governance in procurement, or is this still mostly showing up after an incident?

#IdentitySecurity #AIAgents #ZeroTrust #IAM #CyberSecurity

---

## Rationale

**Hook choice:** Opens with a direct assertion about the core problem ("they borrow one") rather than setup or context. The first two sentences establish both the pattern and the implication, which is enough to earn the "see more" click. This is the counter-intuitive truth most people aren't saying out loud.

**Structure used:** Hook assertion, then grounding context (how widespread the pattern is), then the consequence that makes it a real problem (audit trail loss during incident response), then the fix framed as a contrast (solved for humans, unsolved for agents), then the root cause framing (governance gap, not malice), then a specific discussion question.

**Specific angle reinforced:** The "shared service account" framing is kept throughout, not abstracted into "identity hygiene" generalities. This makes the post credible to security practitioners who recognize the pattern immediately.

**Question:** Specific enough to invite actual answers from SEs and security leaders, not a rhetorical closer. "Showing up after an incident" adds a secondary angle that opens a thread direction.

**Note for Craig:** No hyperlinks in the post body per LinkedIn algorithm rules. If linking to an Okta resource on AI agent identity (e.g., Workforce Identity or Privileged Access docs), put it in the first comment. A real customer story or specific incident example would sharpen this considerably if you have one to draw from.
