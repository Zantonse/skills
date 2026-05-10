## O4AA Knowledge Hub Update — 2026-05-08

### Section Scope
`--section=se-playbook` (9 files): demo-flow, demo-playbook, business-outcomes, use-case-patterns, customer-use-cases-data, competitive, competitive-framework, message-by-persona, customer-evidence

---

### Sources Pulled

- **#okta-ai-agents-field-feedback** (C0A2X24QT5H): 50 messages, Apr 2 – May 8 2026
- **#okta-secures-ai-questions** (C0A4LB3G7BN): 50 messages, Apr 24 – May 8 2026
- **#a4aa** (C08470NJMS5): 50 messages, Mar 25 – May 8 2026
- **#presales-o4aa-a4aa-champions** (C0A964KANA0): 50 messages, Jan 22 – Mar 25 2026 (channel is less active, most recent signal was the NIST NCCoE Agent Identity project note from Brandon Iske)
- **Confluence**: 15 pages returned matching `text ~ "Okta for AI Agents" AND lastmodified >= now("-30d")`. Pages were mostly engineering/ops (TFLO ceremonies, FY27-8 Support O4AA docs, PIA Security AI Agent, performance test plans). No field-facing content in the 15 results relevant to se-playbook updates.

---

### Files Updated (1 total)

**Minor additions:**
- `use-case-patterns.ts`: Added AI Agent JML (Joiner-Mover-Leaver) lifecycle pattern to the "Emerging Field Patterns (May 2026)" card. Added one paragraph documenting what works today (owner deprovisioning revokes delegated sessions via Universal Logout) and what does not (Workload Principal registration does NOT auto-deactivate — admin must manually reassign or deactivate). Added labeled callout `AI Agent JML Lifecycle — Partial Gap` (amber). [Source: Abhishek Singh, #okta-secures-ai-questions, May 8 2026]

---

### Files Skipped (already current): 8 files

- **demo-flow.ts**: Already has the "Okta for Claude Code — All Hands Recording" card from May 7 2026. Current.
- **demo-playbook.ts**: GA demo assets card (Apr 28-30 2026 David Edwards updates), OPA legacy systems recording, Claude Code recording callouts — all present. MCP Adapter labeled as "$55K, 6-12 weeks PS engagement" which is accurate. Current.
- **business-outcomes.ts**: Yahoo and Ramp named references (Apr 30), BV Metrics gap callout (May 2026), AI Readiness Assessment resource — all present. Current.
- **customer-use-cases-data.ts**: All 7 industries with full use case library including Healthcare > Call Center AI (voice+chat). Current.
- **competitive.ts**: Prisma AI / Credo AI field note (May 7), CrowdStrike AI SPM (May 4), Oasis (May field thread), MintMCP (Apr 27), Auth for MCP GA May 6 in MintMCP callout — all present. Current.
- **competitive-framework.ts**: Three-layer market model, five scenarios, where Okta honestly loses — current through April 2026.
- **message-by-persona.ts**: All four personas (CISO, CIO/CTO, Developer, Board/Executive) fully documented including developer FAQ on ROPG deprecated pattern. Current.
- **customer-evidence.ts**: Yahoo + Ramp named references (Apr 30), Authorized to Act Hackathon final numbers (2,897 registrants, 328 submissions, 69 Token Vault usages), Bread Financial + Dell OSAI win stories on Highspot, April active field engagements (H-E-B, TMNA, AXP, etc.). Current.

---

### Topics Needing Deeper Research

- **Google Agent Identity at Google Cloud Next**: Sean Mortazavi (Craig's own AE) asked May 4 about Google's AI Agent Identity solution presented at Google Cloud Next. competitive.ts covers Google Vertex AI as a discovery target and ISPM integration, but does not cover Google's own identity product for AI agents as a competitive threat. Worth a targeted competitive-intel pull if this comes up in deals.
- **MCP Bridge Q3 timeline confirmation**: Ely Kahn confirmed May 8 that MCP Bridge will be a product feature in Q3 (vs. PS-only today). The skill's Common Pitfalls already notes this. Suggest adding a specific Q3 date callout to the demo-playbook.ts when the product date is officially announced.
- **Token lifetime minimum below 5 minutes**: Rocco Martin (#okta-ai-agents-field-feedback, Apr 27) asked about setting access token lifetimes below 5 minutes for agent tokens. Inline hook schema supports seconds but the documented minimum is 5 minutes. This is a field gotcha that may affect short-TTL agent architectures. Needs a product answer before documenting.

---

### Key Intelligence This Cycle

1. **AI Agent JML lifecycle is a field gap being surfaced.** The question "what happens to an AI agent when its human owner leaves the company" is now being asked in customer conversations. Today's answer: delegated sessions revoke via Universal Logout, but the Workload Principal registration requires manual admin action. This is a partial gap SEs must be able to articulate honestly.

2. **MCP Bridge confirmed as PS-only through Q2.** Ely Kahn (Product) explicitly corrected a field misconception on May 8: MCP Bridge is NOT part of the GA product yet. It will be part of the product in Q3. This correction is critical — SEs who pitch MCP Bridge as a self-service GA feature are overpromising.

3. **Okta for Claude Code demo is in the field and customer-shareable.** Justin Artim confirmed the All Hands recording is available and appropriate to share with customers. This is one of the most concrete, immediately-relatable AI agent governance demos available for developer-facing accounts.

4. **Auth for MCP went GA May 6.** Karan Chhina confirmed in #a4aa. This is the Auth0 product that makes MCP servers natively OAuth-aware — distinct from the Okta Agent Gateway. The distinction matters for SEs who need to explain which product covers which scenario (Auth0 Auth for MCP = developer-facing MCP server auth; Okta Agent Gateway = proxy for internal enterprise MCP servers).

5. **All major se-playbook files were already current.** The prior knowledge hub update cycle (also today) had captured all the high-signal items from the April 28–May 7 window. The only net-new item in this cycle is the JML lifecycle gap from May 8.
