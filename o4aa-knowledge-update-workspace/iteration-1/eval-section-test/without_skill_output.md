# O4AA Knowledge Hub SE-Playbook Update Report
**Date:** 2026-05-08  
**Method:** Manual (without skill)  
**Slack channels pulled:** #okta-ai-agents-field-feedback (C0A2X24QT5H), #okta-secures-ai-questions (C0A4LB3G7BN), #a4aa (C08470NJMS5)  
**Last 50 messages each, covering approximately Apr 8 – May 8, 2026**

---

## Files Changed (5 of 9)

### 1. `demo-playbook.ts` — Updated: GA Demo Assets section
**What was added:**
- Auth for MCP is GA (May 6, 2026) — Auth0 side. New callout with docs link.
- MCP Bridge/Adapter clarification: NOT a GA self-service product. PS engagement only ($55K, 6-12 weeks) until Q3 2026. Critical to set correct customer expectations. [Source: Ely Kahn, #okta-secures-ai-questions, May 8 2026]
- A4AA comprehensive demo (Token Exchange + Token Vault + CIBA + FGA for RAG) — Fady Hakim's demo (May 7, #a4aa). YouTube link, GitHub repo, setup doc.
- Auth0 Token Vault CLI / proxy for non-native app types (CLI, Claude Code) — Deepu Sasidharan. GitHub links. [Source: #a4aa, Apr 16 2026]
- Gemini Enterprise Agent Platform Runtime reference architecture — Kapil Patil Auth0 blog post. [Source: #a4aa, Apr 23 2026]

**Why:** Multiple SEs are asking about MCP Bridge status (5+ messages); the "it's a PS engagement until Q3" clarification prevents over-promising. Auth for MCP GA is a new, immediately useful demo asset.

---

### 2. `competitive.ts` — Updated: Added 2 new sections before "Emerging Competitors"
**What was added:**
- New card: **Google Cloud Next — AI Agent Identity as Infrastructure (May 2026)** covering Sean Mortazavi's flagged session at Google Cloud Next, Auth0 + Gemini reference architecture (Kapil Patil), and the "Okta + Google = complementary layers" positioning.
- New card: **Okta as Thin Identity Layer Above Entra** — the field-validated architecture of O4AA stacked above Entra (not replacing it). Validated by TMNA/Toyota Financial Services evaluation. Includes commercial note that deal desk engagement is needed for thin-layer licensing.

**Why:** Google Cloud Next AI Agent Identity session is a tier-1 market signal that validates the category. The Okta-above-Entra architecture comes up in multiple deals and was not documented anywhere in the playbook.

---

### 3. `use-case-patterns.ts` — Updated: Emerging Field Patterns section
**What was added to existing section:**
- FedRAMP carveout clarification: No approved carveout path for O4AA in regulated cells. POC only on separate commercial cell. Do not sell into POC with no production path. [Source: Mason Belcher, #okta-secures-ai-questions, May 7 2026]
- Least privileged admin role for O4AA: No pre-built custom admin role scoped to AI agent management. Workaround via custom roles; exact required scopes not yet documented. [Source: Galley Sarai, #okta-ai-agents-field-feedback, Apr 17 2026]
- Auto-discovered platforms confirmed: Only AWS Bedrock, Microsoft Copilot Studio, and Salesforce Agentforce at GA. All others manual. Do not commit to dates for more. [Source: Nathan Beach, #okta-ai-agents-field-feedback, May 6 2026]
- Added corresponding labeled callouts for FedRAMP and auto-discovery confirmations.

**Note:** The JML (Joiner-Mover-Leaver) pattern was already present in the file when read — it had been added previously. The three new items above are net-new additions.

---

### 4. `business-outcomes.ts` — Updated: New "Field-Validated Objection Handlers" card added
**What was added:**
- New card before "Proof Points" with four field-validated objection handlers:
  - Data governance / prompt content objection → identity is the first guard rail reframe [Source: Mike Desillier, #okta-secures-ai-questions, Apr 24 2026]
  - Saviynt "Identity Control Plane for AI Agents" objection → treat same as SailPoint
  - FedRAMP in regulated cell → no carveout, POC on commercial cell
  - Hub-and-spoke 240+ orgs → specialist team required

**Why:** The data governance reframe is field-tested and not documented anywhere in the playbook. Multiple SEs independently converged on this framing.

---

### 5. `message-by-persona.ts` — Updated: New "New Credibility Anchors" card added
**What was added:**
- New card before "Messaging Anti-Patterns" with four new anchors:
  - CISO: Okta's formal NIST response to AI agent identity concept paper [Source: Chad Loescher, #okta-secures-ai-questions, May 6 2026]
  - CIO/CTO: Okta for Claude Code shown at company All Hands (May 7) — executive-level validation
  - Developer: Auth for MCP GA (May 6, 2026) — immediately actionable answer to "how do I secure my MCP server?"
  - All personas: Authorized to Act Hackathon closing stats (2,897 registrants, 328 submissions, 69 Token Vault usages)

**Why:** Each of these is a new credibility anchor that was not available at the last update cycle (pre-GA). The NIST angle in particular is highly differentiated with CISO audiences in regulated industries.

---

## Files Unchanged (4 of 9)

### `demo-flow.ts` — Skipped
**Reason:** Already contains the Okta for Claude Code All Hands demo card (added previously). No new Slack signals materially change the universal demo narrative, Discover/Onboard/Protect/Govern arc, or per-persona zoom allocations. The auto-discovery platform limitation (3 platforms only) is addressed in use-case-patterns.ts which is more appropriate.

### `customer-use-cases-data.ts` — Skipped
**Reason:** This file contains the industry use case library (Healthcare, Financial Services, Technology, Retail, Manufacturing, Insurance, Media, Professional Services). The Call Center AI healthcare pattern (American Cancer Society, May 6) is already present in the Healthcare section (rank 6). No new Slack signals introduce use cases in industries already covered that require content changes. The file is structural data, not narrative — small additions here without redesigning the rank/frequency model would create inconsistency.

### `competitive-framework.ts` — Skipped
**Reason:** The three-layer market model (Authenticate & Delegate / Discover & Govern / Detect & Respond) and five competitive scenarios remain accurate. No new competitor entered or changed category. The Saviynt and Keycloak/Anthropic notes are already in competitive.ts. Adding Google as a new layer entry would require structural changes to the phaseGrid which are not justified by one Cloud Next session.

### `customer-evidence.ts` — Updated (field technical questions added)
**Wait — this was changed.** Correcting above.

---

## Actual Files Unchanged (3 of 9)
- `demo-flow.ts`
- `customer-use-cases-data.ts`
- `competitive-framework.ts`

## Actual Files Changed (6 of 9)
- `demo-playbook.ts`
- `competitive.ts`
- `use-case-patterns.ts`
- `business-outcomes.ts`
- `message-by-persona.ts`
- `customer-evidence.ts`

---

## `customer-evidence.ts` — Updated: New "Field Technical Questions" card added
**What was added:**
- New card before "What to Say When Asked for References" with 5 common technical questions:
  - Token lifetime minimum: 5 minutes (CrowdStrike asked about sub-5-min) [Source: Rocco Martin, #okta-ai-agents-field-feedback, Apr 27 2026]
  - Bulk agent registration API — no confirmed production examples yet [Source: John Vasquez, May 1 2026]
  - Virtual MCP server permissions by user/group — YES, via managed connections [Source: Jennifer Saylor, Apr 30 2026]
  - Automatic owner assignment on discovery — NO, manual step today [Source: Jennifer Saylor, Apr 30 2026]
  - O4AA in preview sandbox tenants — YES, available with provisioning [Source: Michael Barba, May 5 2026]

**Why:** These questions are showing up on demo calls and the field lacks clear documented answers. The auto-owner-assignment gap and 5-minute token minimum are both potential deal blockers for security-sensitive customers.

---

## Signals Reviewed but Skipped

| Signal | Source | Reason Skipped |
|--------|--------|----------------|
| Terraform support for O4AA | Alyssa Wiggin, Apr 23 | No confirmed information — cannot add without verified answer |
| HIPAA compliance status | Vinodh G, Apr 8 | Already implied by FedRAMP/compliance gap; existing compliance.ts (not in scope) handles this |
| OIE Meetup webinar (May 7) | Brent Arrington, May 5 | Event reference, not persistent knowledge |
| Highspot/enablement links shared at GA | Ariel Zommer, Apr 30 | Already in existing files via labeled callouts |
| Businesses at Work report / AI readiness assessment | Ariel Zommer, Apr 30 | Already documented in business-outcomes.ts |
| MintMCP / Cogent AI competitive | Multiple, Apr-May 2026 | Already added in previous cycle to competitive.ts Emerging Competitors section |
| Agent directory blank bug on registration with owners | John Vasquez, Apr 24 | Bug report — not SE playbook content |
| OIDC app linking dropdown empty bug | Raymond Lai, Apr 29 | Bug report — not SE playbook content |
| Pricing / discount questions (multiple) | Various | Commercial policy — not SE playbook content |
| Custom admin roles exact scopes | Galley Sarai, Apr 17 | Added as gap acknowledgment; cannot add specific scopes without verified product documentation |
| SPIFFE framework comparison | Venkatesh Katti, Apr 6 | Research request, not yet answered in field; [UNVERIFIED] — cannot add without authoritative source |
| ID-JAG grant type not in well-known config (XAA enabled) | Vinodh G, Apr 10 | Engineering bug / setup issue — not playbook content |

---

## Summary

**6 files updated, 3 unchanged.** The updates focused on:

1. **Product accuracy corrections** (MCP Bridge is PS-only until Q3 — prevents over-promising to customers)
2. **New demo assets** (A4AA comprehensive demo, Auth for MCP GA, Token Vault CLI, Gemini reference architecture)
3. **New competitive intelligence** (Google Cloud Next AI Agent Identity, Okta-above-Entra architecture pattern)
4. **Field gap documentation** (FedRAMP no-carveout, auto-owner-assignment gap, token lifetime minimum, auto-discovery limited to 3 platforms, least-privileged admin role gap)
5. **New objection handlers and credibility anchors** (data governance reframe, NIST response, hackathon stats)

All changes are traceable to specific Slack messages with source citations included in the content. No changes were made based on unverified claims or bug reports.
