---
name: architecture-diagram
description: >
  Generates professional technical architecture diagrams for B2B enterprise sales — especially identity and access management (IAM), identity governance (IGA), Zero Trust, and CIAM. Use this skill whenever the user needs an architecture diagram, solution architecture visual, current-state/future-state comparison, migration roadmap diagram, authentication flow, provisioning lifecycle, or governance architecture for a customer presentation, proposal, or workshop leave-behind. Also use when the user says "create a diagram for [customer]", "architecture slide", "draw the Okta architecture", "show the before and after", or anything involving visual architecture for sales engineering. Primary generation path is the Lucid MCP server (editable, shareable Lucidchart documents with real cloud icons and customer collaboration links). Fallback to nano-banana-art (AI image generation) for sketches and photorealistic needs. Includes IAM-specific component taxonomy, hex color system, Lucid shape registry, and audience adaptation rules.
---

# Architecture Diagram Generator

Generate polished, customer-specific technical architecture diagrams for B2B sales presentations.

**Primary path:** Lucid MCP (`lucid_create_diagram_from_specification`) — produces editable, shareable Lucidchart documents with native text, real AWS/Azure/GCP service icons, and customer collaboration links.

**Fallback path:** AI image generation (nano-banana-art) — use for rapid whiteboard sketches or when photorealistic/illustrated style is needed.

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

| Type | Layout | Best For | Lucid Tool |
|------|--------|---------|-----------|
| `platform-overview` | Hub-and-spoke | Exec intro to unified identity platform | `lucid_create_diagram_from_specification` |
| `before-after` | 2-page document | Proposals, workshops — **default if unspecified** | `lucid_create_diagram_from_specification` |
| `current-state` | Dense, annotated | Discovery follow-up | `lucid_create_diagram_from_specification` |
| `future-state` | Clean, simplified | Standalone proposal slide | `lucid_create_diagram_from_specification` |
| `auth-flow` | Left-to-right sequence | Authentication deep-dive | `lucid_create_sequence_diagram` |
| `provisioning-flow` | Swimlane (top-to-bottom) | JML lifecycle demo | `lucid_create_diagram_from_specification` |
| `governance-flow` | IGA-centric with cycles | Certification/SoD discussions | `lucid_create_diagram_from_specification` |
| `zero-trust` | NIST 800-207 (control/data plane) | CISO Zero Trust briefings | `lucid_create_diagram_from_specification` |
| `migration-phases` | Three sequential panels | Crawl-Walk-Run roadmaps | `lucid_create_diagram_from_specification` |

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

## Step 2: Plan the Diagram Structure

Map the customer context to shapes and colors before writing any JSON.

### Color System (Hex Codes — Required for Lucid)

Lucid requires hex codes in all JSON. Never use color names. For AI image generation prompts (fallback path), use the color names from `references/color-system.md`.

| Role | Hex | `textColor` | AI Image Name |
|------|-----|------------|--------------|
| Identity Platform (Okta/IdP hub) | `#0D9488` | `#FFFFFF` | teal |
| Cloud / SaaS apps | `#0091DA` | `#FFFFFF` | sky blue |
| On-prem / Legacy | `#6B7280` | `#FFFFFF` | slate gray |
| Governance / IGA | `#6B21A8` | `#FFFFFF` | deep purple |
| Risk / Current-state pain | `#D97706` | `#FFFFFF` | amber orange |
| Compliant / Future-state | `#166534` | `#FFFFFF` | forest green |
| PAM / Privileged | `#4C1D95` | `#FFFFFF` | deep indigo |
| Zone background fill | `#F8FAFC` | — | off-white |
| Transparent zone boundary | `#00000000` | — | — |
| Borders / arrows (default) | `#1E293B` | — | dark navy |
| Auth flow arrows (SAML/OIDC) | `#2563EB` | — | blue |
| Provisioning arrows (SCIM) | `#0D9488` | — | teal |
| Governance arrows | `#7C3AED` | — | purple |
| Risk / violation arrows | `#DC2626` | — | red |

### Component Shapes (for Lucid JSON)

| IAM Component | Lucid `type` | Notes |
|---|---|---|
| Okta / Generic IdP | `rectangleContainer` | Use `containerTitle: {text: "Okta WIC"}` — containers have no `text` property |
| SaaS App | `roundedRectangleContainer` | `containerTitle` for name |
| On-prem / Legacy App | `rectangle` | Sharp corners = on-prem convention |
| AD / LDAP / Database | `database` | Flowchart library |
| Policy Decision Point | `decision` | Flowchart library diamond |
| Security Gateway / PEP | `hexagon` | Standard library |
| Approval Workflow step | `process` | Flowchart library |
| Auth Flow Start/End | `terminator` | Flowchart library |
| Risk Annotation | `note` | Flowchart library; amber fill |
| AWS IAM | `namedShape` | `className: "ArchAWSIdentityandAccessManagementAWS2024"` |
| AWS IAM Identity Center | `namedShape` | `className: "ArchAWSIAMIdentityCenterAWS2024"` |
| Amazon Cognito | `namedShape` | `className: "ArchAmazonCognitoAWS2024"` |
| Azure AD / Entra ID | `namedShape` | `className: "AzureActiveDirectoryAzure2021"` |
| Azure AD B2C | `namedShape` | `className: "AzureADB2CAzure2021"` |
| Azure Identity Governance | `namedShape` | `className: "IdentityGovernanceAzure2021"` |
| AWS Cloud boundary | `namedContainer` | `className: "AWSCloudAWS2024"` |
| AWS VPC boundary | `namedContainer` | `className: "VirtualPrivateCloudVPCAWS2024"` |

See `references/lucid-shape-registry.md` for the full AWS/Azure/GCP shape library, zone fill patterns, and swimlane templates.

---

## Step 3: Generate with Lucid MCP (Primary Path)

### Pre-flight: Always Read the Spec First

**Before calling `lucid_create_diagram_from_specification`:** read `lucid://diagram-specification`. The MCP validates strictly — wrong shape type names, missing required properties, and incorrect endpoint formats produce `"invalid_file"` 400 errors with no indication of which field failed.

**Before calling `lucid_create_sequence_diagram`:** read `lucid://sequence-diagram-specification`.

**For AWS/Azure/GCP named shapes:** read the relevant library resource first:
- `lucid://shape-libraries/aws-2024/security-identity-and-compliance` (Okta-adjacent)
- `lucid://shape-libraries/aws-2024/common` (top 36 shapes)
- `lucid://shape-libraries/azure-2021/identity`
- `lucid://shape-libraries/gcp-2021/security`

### Tool Selection

| Diagram Type | Tool | `use_assisted_layout` |
|---|---|---|
| platform-overview, future-state, current-state | `lucid_create_diagram_from_specification` | `false` (containers present) |
| before-after | `lucid_create_diagram_from_specification` | `false` (2 pages or split zones) |
| provisioning-flow, governance-flow, zero-trust | `lucid_create_diagram_from_specification` | `false` (swimLanes present) |
| migration-phases | `lucid_create_diagram_from_specification` | `false` (spatial layout) |
| auth-flow (SAML, OIDC, token exchange) | `lucid_create_sequence_diagram` | N/A |

Set `use_assisted_layout: false` whenever the diagram uses containers, swimlanes, or zone-based spatial positioning. Use `true` only for simple linear flowcharts with no containers.

### JSON Construction Rules (Prevents 400 Errors)

1. **Hex codes only** — `"#0D9488"` not `"teal"`. Color names are silently ignored or cause errors.
2. **No emoji in text** — render as solid black boxes.
3. **Shape type names are exact strings** — copy from `lucid://diagram-specification`. `"rectangleContainer"` not `"rectangle-container"`.
4. **Containers have no `text` property** — use `containerTitle: {text: "Zone Name"}` on types that support it: `rectangleContainer`, `roundedRectangleContainer`, `circleContainer`, `pillContainer`. `swimLanes`, `braceContainer`, `bracketContainer` do NOT support `containerTitle`.
5. **`text` shapes have no `style` property** — adding `style` to `type: "text"` causes an error.
6. **Endpoint `position`: both or neither** — smart auto-routing omits `position` from both `shapeEndpoint` objects. Specifying position on only one endpoint causes failure.
7. **Shapes fully inside containers** — entire bounding box must fit strictly inside the container with padding on all sides. Edge-touching is not contained.
8. **swimLane lane width math** — `vertical: true` (side-by-side columns): sum of lane `width` values = `boundingBox.w`. `vertical: false` (stacked rows): sum of lane `width` values = `boundingBox.h`.
9. **`assistedLayout` on the container shape** — for `swimLanes` and `bpmnPool`, set `assistedLayout: true` on the container, NOT on individual lane objects.
10. **Shape IDs are unique strings** — never reuse IDs across the document; never use integer IDs.
11. **Z-index = array order** — shapes defined later appear in front. Put background containers and zone boundaries first in the shapes array.
12. **2MB limit** — use compact JSON (no whitespace indentation) for large diagrams.
13. **ERD, DFD, ArchiMate shapes are unsupported** by the MCP as of May 2026. Use standard shapes.
14. **No vendor IdP shape libraries** — Okta, Auth0, Ping, SailPoint have no Lucid library. Represent as labeled `rectangleContainer` with semantic stroke color.

### Container Layout Patterns

**Hub-and-spoke (platform-overview, future-state):**
- One `rectangleContainer` per zone — User/Device, On-Premises, Cloud Identity, SaaS Apps, Governance
- Set `assistedLayout: true` on each container (for its contents)
- Pass `use_assisted_layout: false` to the tool call
- Zone fills from `references/lucid-shape-registry.md`

**Swimlane (provisioning-flow, JML):**
- `swimLanes` with `vertical: false` (stacked rows)
- Set `assistedLayout: true` on the `swimLanes` shape
- Standard actor sequence: HR System → IdP / Lifecycle → Target Apps → Governance

**Before/After:**
- Two-page document: page 1 = current state, page 2 = future state
- Or single wide canvas: current-state shapes at x=0–600, future-state at x=750–1350
- Current: amber zone fills, dense connections, `note` shapes for pain callouts
- Future: clean containers, minimal connections, green metric `note` shapes

**Zero-trust (NIST 800-207):**
- `swimLanes` with `vertical: false`, two rows: Control Plane (PDP) / Data Plane (PEP + resources)

**Migration phases:**
- Three `rectangleContainer` shapes side-by-side with `containerTitle` Phase 1 / Phase 2 / Phase 3

### Auth Flow PlantUML Rules (Sequence Diagrams)

Supported participants: `participant`, `actor`, `database`, `boundary`, `control`, `entity`

Supported arrows: `->` `-->` `->>` `-->>` `<->` `<-->` `<<->>` `<<-->>`

Supported groupings: `alt`/`else` (else only inside alt), `loop`, `opt`, `par`, `critical`, `group`

**Do NOT use** (causes parse errors):
- `skinparam` directives of any kind
- `activate A #color` (color modifier on activate)
- `destroy`, `newpage`, `return`, `ref over`
- `== Section ==` dividers, `...` delays
- Lines starting with `!` (preprocessor directives)
- Lost message arrows (`->x`, `[->`, `->]`)
- `else` outside an `alt` block
- `collections`, `queue` participant types

### Post-Generation Workflow

After `lucid_create_diagram_from_specification` or `lucid_create_sequence_diagram` returns:

1. **Share the edit URL** with the account team for internal review.
2. **Export PNG**: call `lucid_export_document_as_PNG` — use in slide decks and email attachments.
3. **Customer share link**: call `lucid_create_document_share_link`
   - `role: "comment"` for customer review/feedback
   - `role: "edit"` for collaborative refinement
   - `restrict_to_account: false` when sharing with external customers
4. **Optional direct access**: call `lucid_share_document_with_collaborators` with customer email.

---

## Step 4: Generate with AI Image (Fallback Path)

Use nano-banana-art when Lucid MCP is unavailable, when photorealistic/illustrated style elements are needed, or for quick internal whiteboard sketches.

### Mandatory Prompt Rules

1. **Use color names, never hex codes** — hex codes render as visible text in the image
2. **Specify "no text labels" or use only 1-3 word labels** — AI text rendering fails on dense labels
3. **List every connection explicitly** — state "There are exactly N connections." Unlisted connections invite phantom arrows
4. **Describe layout spatially** — "on the far left", "directly below", not grid counts
5. **Max 8 components per generation pass** — above this threshold, quality degrades. Use multi-pass for complex diagrams
6. **Specify aspect ratio** — 16:9 for slides, 4:3 for documents, 1:1 for social

Prompt templates are in `references/prompt-templates.md`. Color names map to hex via `references/color-system.md`.

### Multi-Pass Strategy (for diagrams with >8 components)

1. **Pass 1** — User/application tier (users, browsers, apps)
2. **Pass 2** — Identity platform tier (IdP, MFA, provisioning engine)
3. **Pass 3** — Target systems tier (AD, cloud apps, governance)

Then composite layers or generate a simplified version that fits within 8 components for the target audience tier.

```bash
npx tsx ~/.claude/skills/nano-banana-art/tools/generate-image.ts \
  --model nano-banana-pro \
  --prompt "[CONSTRUCTED PROMPT]" \
  --size 2K \
  --aspect-ratio 16:9 \
  --output /path/to/output.png
```

### Before/After (AI Image)

Generate as a **single image** with split-panel layout:
- Left panel: "Current State" — dense, tangled, amber risk annotations
- Right panel: "With [Vendor]" — clean, hub-and-spoke, green compliance badges
- The visual simplicity of the future state IS the sales argument

---

## Step 5: Review

After generation, verify:

**For Lucid diagrams:**
1. All shapes are correctly contained within zone boundaries (no shapes crossing container edges)
2. Connection arrows have correct labels (SAML 2.0, SCIM 2.0, OIDC, etc.)
3. `containerTitle` text is readable at target screen size
4. Export PNG at 2K for slides — confirm labels are legible
5. Share link permissions match intent (comment vs. edit, internal vs. external)

**For AI-generated images:**
1. **Label accuracy** — AI text may have spelling errors. Flag any labels that need correction.
2. **Connection accuracy** — verify arrows match the intended connections
3. **Layout quality** — whitespace meets audience tier requirements (40% for exec, 30% for CISO, 20% for architect)

For customer-facing AI images, recommend importing into **Canva** or **Figma** as a background layer, adding native text elements, and exporting at 2K–4K resolution.

---

## Step 6: Add Sales Annotations

Transform the technical artifact into a sales artifact:

**On current-state diagrams:**
- Amber callout cards quantifying pain: "~200 orphaned accounts", "14 manual steps per onboarding"
- Risk zone highlights with compliance framework references

**On future-state diagrams:**
- Green metric cards showing transformation: "Provisioning: 4.5 hrs → 12 min"
- Compliance badges: SOC 2 Type II, FedRAMP, HIPAA

**In Lucid:** Use `note` shapes for callouts — amber fill for pain, green fill for metrics. Use `text` shapes for compliance badges (no `style` property on `text` types).

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
11. **[Lucid] Color names in JSON** — hex codes only; color names cause silent failure or errors
12. **[Lucid] Skipping the spec** — always read `lucid://diagram-specification` before generating JSON
13. **[Lucid] Vendor logos that don't exist** — Okta, SailPoint, CyberArk have no Lucid shape library. Use labeled `rectangleContainer` with semantic stroke color.
14. **[Lucid] `use_assisted_layout: true` with containers** — always `false` for zone-based IAM diagrams

---

## Reference Files

| File | Contents |
|------|----------|
| `references/lucid-shape-registry.md` | IAM component → Lucid shape type mapping; AWS/Azure/GCP named shape classNames; hex color table; zone container patterns; complete gotchas list |
| `references/prompt-templates.md` | Ready-to-use prompt templates for AI image generation (fallback path) |
| `references/color-system.md` | Full color palette with hex values, color names, zone fills, arrow colors |
| `references/iam-taxonomy.md` | Complete IAM component taxonomy with shapes, colors, and groupings |

The full research synthesis is available at: `~/Documents/ObsidianNotes/Claude-Research/architecture-diagram-research-synthesis-2026-03.md`
