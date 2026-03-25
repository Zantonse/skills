---
name: architecture-diagram
description: >
  Generates professional technical architecture diagrams for B2B enterprise sales — especially identity and access management (IAM), identity governance (IGA), Zero Trust, and CIAM. Use this skill whenever the user needs an architecture diagram, solution architecture visual, current-state/future-state comparison, migration roadmap diagram, authentication flow, provisioning lifecycle, or governance architecture for a customer presentation, proposal, or workshop leave-behind. Also use when the user says "create a diagram for [customer]", "architecture slide", "draw the Okta architecture", "show the before and after", or anything involving visual architecture for sales engineering. This skill leverages nano-banana-art (Gemini 3 Pro Image) for generation and includes IAM-specific component taxonomy, color systems, and audience adaptation rules based on extensive research.
---

# Architecture Diagram Generator

Generate polished, customer-specific technical architecture diagrams for B2B sales presentations using AI image generation (nano-banana-art / Gemini 3 Pro Image).

This skill produces **post-discovery deliverables** — follow-up emails, proposal slides, workshop leave-behinds. It is not a whiteboard tool for live discovery sessions.

## Core Principle: Audience First

The audience tier — not the technical accuracy — is the primary quality variable. A Level 2 C4 diagram shown to a VP is a failure regardless of correctness. **Always resolve the audience before generating anything.**

---

## Step 1: Gather Required Inputs

Before generating, collect three things. Infer from conversation context when possible; ask when ambiguous.

### Audience Tier

| Tier | Who | Max Elements | Label Style | Protocol Labels |
|------|-----|-------------|-------------|-----------------|
| `exec` | VP, CIO, CFO | 8 | Business language only | None |
| `ciso` | CISO, VP Security | 12 | Business + security mix | Security-relevant only |
| `architect` | IAM architect, IT director | 20 | Full technical | All (SAML, OIDC, SCIM) |

### Diagram Type

| Type | Layout | Best For |
|------|--------|---------|
| `platform-overview` | Hub-and-spoke | Exec intro to unified identity platform |
| `before-after` | Split panel (current left, future right) | Proposals, workshops — **default if unspecified** |
| `current-state` | Dense, annotated | Discovery follow-up |
| `future-state` | Clean, simplified | Standalone proposal slide |
| `auth-flow` | Left-to-right sequence | Authentication deep-dive |
| `provisioning-flow` | Swimlane (top-to-bottom) | JML lifecycle demo |
| `governance-flow` | IGA-centric with cycles | Certification/SoD discussions |
| `zero-trust` | NIST 800-207 (control/data plane) | CISO Zero Trust briefings |
| `migration-phases` | Three sequential panels | Crawl-Walk-Run roadmaps |

### Customer-Specific Components

Every customer-facing diagram must use the prospect's actual system names. Generic labels ("App 1", "Identity Provider") are an anti-pattern that signals the seller hasn't done account research.

Collect:
- **Customer name** (used in diagram title)
- **Identity platform(s)** — proposed or in-use (Okta, Entra ID, SailPoint, etc.)
- **User populations** — employees, contractors, partners, customers
- **Key applications** (3-5) — their actual names (Salesforce, ServiceNow, SAP, etc.)
- **On-prem systems** — AD, LDAP, legacy apps
- **Compliance frameworks** — FedRAMP, SOX, HIPAA, etc.

If specifics are unknown, substitute plausible IAM defaults and flag them for confirmation.

---

## Step 2: Construct the Prompt

Use the prompt templates in `references/prompt-templates.md` for the selected diagram type. The templates follow a consistent structure:

```
[Diagram description and layout]
[Component list with labels, shapes, colors]
[Connection list with labels and directions]
[Style directives]
```

### Mandatory Prompt Rules

1. **Use color names, never hex codes** — hex codes render as visible text in the image
2. **Specify "no text labels" or use only 1-3 word labels** — AI text rendering fails on dense labels
3. **List every connection explicitly** — state "There are exactly N connections." Unlisted connections invite phantom arrows
4. **Describe layout spatially** — "on the far left", "directly below", not grid counts
5. **Max 8 components per generation pass** — above this threshold, quality degrades. Use multi-pass for complex diagrams
6. **Specify aspect ratio** — 16:9 for slides, 4:3 for documents, 1:1 for social

### Color System

Use these semantic color assignments consistently. See `references/color-system.md` for the full palette with hex values.

| Role | Color Name | Usage |
|------|-----------|-------|
| Cloud / SaaS | Sky blue | Cloud-native components, SaaS apps |
| On-prem / Legacy | Cool slate gray | On-premises systems, legacy apps |
| Identity platform | Teal | Vendor platform hub, key controls |
| Governance / IGA | Deep purple | IGA platform, governance layer, SoD |
| Risk / Gap | Amber orange | Pain annotations, current-state risk zones |
| Compliance | Forest green | Certified access, compliant flows |
| Text / Borders | Near-black navy | All labels, borders, arrows |
| Background | Off-white | Canvas base |

### Component Shapes

| Shape | Meaning |
|-------|---------|
| Rounded rectangle | SaaS app, cloud service |
| Sharp rectangle | On-premises system, legacy app |
| Cylinder | Database, directory, vault |
| Hexagon | Security enforcement point (gateway, PEP, PAM) |
| Diamond | Decision/policy evaluation point |
| Cloud outline | Cloud region or tenant boundary |
| Dashed rectangle | Optional, future state, or out-of-scope |

---

## Step 3: Generate with nano-banana-art

Use the nano-banana-art tool to generate:

```bash
npx tsx ~/.claude/skills/nano-banana-art/tools/generate-image.ts \
  --model nano-banana-pro \
  --prompt "[CONSTRUCTED PROMPT]" \
  --size 2K \
  --aspect-ratio 16:9 \
  --output /path/to/output.png
```

### Multi-Pass Strategy (for diagrams with >8 components)

For complex diagrams, generate in layers:

1. **Pass 1** — User/application tier (users, browsers, apps)
2. **Pass 2** — Identity platform tier (IdP, MFA, provisioning engine)
3. **Pass 3** — Target systems tier (AD, cloud apps, governance)

Then composite the layers or generate a simplified version that fits within the 8-component limit for the target audience tier.

### Before/After Diagrams

Generate as a **single image** with split-panel layout:
- Left panel: "Current State" — dense, tangled, amber risk annotations
- Right panel: "With [Vendor]" — clean, hub-and-spoke, green compliance badges
- The visual simplicity of the future state IS the sales argument

---

## Step 4: Review and Post-Process

After generation, review the image for:

1. **Label accuracy** — AI-generated text may have spelling errors. Flag any labels that need correction.
2. **Connection accuracy** — verify arrows match the intended connections
3. **Layout quality** — check whitespace meets audience tier requirements (40% for exec, 30% for CISO, 20% for architect)

### Post-Processing Guidance

For customer-facing materials, recommend the user:
- Import the generated image into **Canva** or **Figma** as a background layer
- Add all text labels as native text elements (guarantees correct spelling and brand fonts)
- Add compliance badges, risk callouts, and metric cards as overlay elements
- Export final PNG at 2K or 4K resolution

For internal or draft use, the AI-generated diagram is often sufficient as-is.

---

## Step 5: Add Sales Annotations

Transform the technical artifact into a sales artifact:

**On current-state diagrams:**
- Amber callout cards quantifying pain: "~200 orphaned accounts", "14 manual steps per onboarding"
- Risk zone highlights with compliance framework references

**On future-state diagrams:**
- Green metric cards showing transformation: "Provisioning: 4.5 hrs → 12 min"
- Compliance badges: SOC 2 Type II, FedRAMP, HIPAA

**On all diagrams:**
- Title with customer name and scenario
- Date and version number
- Legend/key for all colors and shapes

---

## Anti-Patterns Checklist

Before delivering any diagram, verify none of these apply:

1. **Generic labels** — "App 1", "Identity Provider" instead of customer's actual system names
2. **Unlabeled arrows** — every connection needs a direction and label
3. **Wrong abstraction for audience** — protocol details shown to a VP, or outcomes-only shown to an architect
4. **No current state** — jumping to future state without validating current state understanding
5. **Too many elements** — exceeding the audience tier's max component count
6. **Color without text/shape backup** — relying on color alone to encode meaning (fails for colorblind and grayscale print)
7. **Feature-centric layout** — vendor product as the center of the universe instead of the customer's use case
8. **No legend** — never assume the audience knows your notation
9. **Undated/untitled** — every diagram needs: title, customer name, date, version
10. **Over-complexity as credibility** — if a viewer can't extract the central message in 10 seconds, the diagram has failed

---

## Reference Files

For detailed specifications, read these files as needed:

| File | Contents |
|------|----------|
| `references/prompt-templates.md` | Ready-to-use prompt templates for each diagram type |
| `references/color-system.md` | Full color palette with hex values, zone fills, arrow colors |
| `references/iam-taxonomy.md` | Complete IAM component taxonomy with shapes, colors, and groupings |

The full research synthesis is available at: `~/Documents/ObsidianNotes/Claude-Research/architecture-diagram-research-synthesis-2026-03.md`
