# Architecture Diagram Prompt Templates

Ready-to-use templates for Nano Banana Pro (Gemini 3 Pro Image) via nano-banana-art. Replace bracketed placeholders with customer-specific values.

**Critical rules for all templates:**
- Use color NAMES, never hex codes (hex renders as visible text)
- Max 8 labeled components per single generation pass
- Describe layout spatially ("on the far left"), not as grid counts
- List every connection explicitly with direction and label
- Specify aspect ratio: 16:9 for slides, 4:3 for documents

---

## Template 1: Platform Overview (Hub-and-Spoke)

**Use case:** Executive intro to a unified identity platform. VP/CISO audience. Max 8 elements.

```
Create a clean enterprise architecture diagram for a B2B technology sales presentation.

DIAGRAM TYPE: Hub-and-spoke identity platform overview
LAYOUT: Center hub with radiating spokes. White background. 16:9 aspect ratio.
Generous whitespace between all components — at least 40% of canvas is empty.

CENTER HUB: One large rounded rectangle labeled [IDENTITY PLATFORM NAME].
Apply teal fill with white text. This is the visual anchor.

LEFT SIDE (Identity Sources) — 2 components arranged vertically:
- Sharp rectangle labeled [HR SYSTEM], slate gray fill
- Cylinder shape labeled [DIRECTORY e.g. Active Directory], slate gray fill
Both connected to center hub with solid arrows pointing right.

RIGHT SIDE (Target Applications) — 3 components arranged vertically:
- Rounded rectangle labeled [APP 1], sky blue fill
- Rounded rectangle labeled [APP 2], sky blue fill
- Rounded rectangle labeled [APP 3], sky blue fill
All connected from center hub with solid arrows pointing right.

TOP (Users): One box or icon group labeled [USER POPULATION].
Connected to center hub with a downward arrow.

There are exactly 6 connections in this diagram.

STYLE: Flat vector illustration, no gradients, no drop shadows.
Clean thin borders on all components. Color palette: white background,
teal for hub, slate gray for sources, sky blue for SaaS apps, dark navy text.
No hex codes in any visible text. Bold clean sans-serif font.
```

---

## Template 2: Before/After (Current State / Future State)

**Use case:** Proposals and workshops. Shows transformation. All audience tiers.

```
Create a split-panel technical architecture diagram for a B2B enterprise proposal.

LAYOUT: Two equal panels side by side, separated by a thin vertical divider.
16:9 aspect ratio. White canvas.

LEFT PANEL — "Current State":
Header bar at top: dark gray fill, white text: "Current State"
Show [NUMBER] disconnected components with NO central hub.
Include: [LEGACY SYSTEM 1], [LEGACY SYSTEM 2], [MANUAL PROCESS],
[APP 1], [APP 2], [APP 3] — connected by tangled crossing arrows.
Apply amber warning annotations on 2 components.
Visual impression: complex, fragmented, crowded.

RIGHT PANEL — "Future State":
Header bar at top: teal fill, white text: "With [VENDOR NAME]"
Show ONE central hub: [IDENTITY PLATFORM] in teal fill.
Sources (left of hub): [DIRECTORY], [HR SYSTEM]
Applications (right of hub): [APP 1], [APP 2], [APP 3]
Clean directional arrows, no crossing lines.
Apply green badges on 2-3 components.
Visual impression: simple, ordered, spacious.

STYLE: Flat vector, no gradients. Enterprise presentation quality.
Left panel: slightly desaturated, cool gray tones ("before").
Right panel: higher contrast, teal accent ("after").
Both panels at identical abstraction level. No hex codes in text.
```

---

## Template 3: Provisioning Flow (Joiner-Mover-Leaver Swimlane)

**Use case:** IGA demo or technical workshop. Architect audience.

```
Create a technical process flow diagram showing the identity governance lifecycle.

DIAGRAM TYPE: Swimlane process flow
LAYOUT: Three horizontal swim lanes from top to bottom. Left-to-right progression.
White background. 16:9 aspect ratio.

SWIM LANE 1 (top): Header "[HR SYSTEM]" — pale blue header bar.
Contents: "Joiner Event", "Role Change Event", "Leaver Event" — spaced left to right.

SWIM LANE 2 (middle): Header "[IGA PLATFORM]" — pale purple header bar.
Contents: "Access Request", "Approval Workflow", "Certification Campaign", "Revocation"

SWIM LANE 3 (bottom): Header "Target Systems" — pale teal header bar.
Contents: "[APP 1]", "[DIRECTORY]", "[APP 2]"

CONNECTIONS: Vertical arrows from Lane 1 down to corresponding Lane 2 boxes.
Vertical arrows from Lane 2 down to Lane 3 labeled "Provision" and "Deprovision".
Horizontal arrows in Lane 2 showing left-to-right sequence.
One return arrow from Lane 3 back to Lane 2 labeled "Scheduled Review".

There are exactly [N] connections.

STYLE: Flat design. Swimlane fills: pale blue / pale purple / pale teal.
Solid arrows for active flows, dashed for async/scheduled. Dark navy text. No hex codes.
```

---

## Template 4: Zero Trust Architecture

**Use case:** CISO Zero Trust briefing. CISO + architect audience.

```
Create a Zero Trust identity architecture diagram for a cybersecurity presentation.

DIAGRAM TYPE: Zero Trust Architecture (NIST 800-207 pattern)
LAYOUT: Three horizontal tiers. Clear separation. 16:9 aspect ratio.
Dark charcoal background. Light text. High contrast.

TOP TIER — "Subjects":
Row of subject icons: "Workforce", "Partners", "Service Accounts", "Devices"

MIDDLE TIER — "Identity Control Plane" (visually dominant, 40% larger than other elements):
Two boxes side by side:
  - "Policy Engine" — hexagon shape, teal fill, white text
  - "Policy Administrator" — rounded rectangle, teal fill, white text
Connected with bidirectional arrow. Enclose both in a labeled area.

BOTTOM TIER — "Data Plane":
Three hexagon shapes (Policy Enforcement Points), each connected to a resource:
  "[APP 1]", "[NETWORK ZONE]", "[CLOUD WORKLOADS]"

CONNECTIONS:
Thick arrows from Control Plane down to each PEP labeled "Access Decision"
Thin arrows from each Subject to Policy Engine labeled "Access Request"
Thin dashed arrows from Subjects to PEPs labeled "Resource Request"

There are exactly [N] connections.

STYLE: Dark mode — charcoal background, teal accent for control plane,
amber for PEPs, white for subjects and resources. Clean vector lines.
Subtle glow on control plane zone. White text. No hex codes.
```

---

## Template 5: Migration Phases (Crawl-Walk-Run)

**Use case:** Phased roadmap. All audience tiers.

```
Create a phased migration roadmap diagram for an enterprise identity transformation.

DIAGRAM TYPE: Three sequential phase panels
LAYOUT: Three panels arranged left to right, each equally sized. 16:9 aspect ratio.
White background with subtle gray dividers between panels.

PANEL 1 — "Phase 1: Foundation" — Blue header bar:
- 3-4 items listed vertically: [ITEM 1], [ITEM 2], [ITEM 3]
- Timeline label at bottom: "[TIMELINE e.g. 0-90 days]"
- Success gate label: "[METRIC]"

PANEL 2 — "Phase 2: Expand" — Teal header bar:
- 3-4 items listed vertically: [ITEM 1], [ITEM 2], [ITEM 3]
- Timeline: "[TIMELINE]"
- Gate: "[METRIC]"

PANEL 3 — "Phase 3: Optimize" — Purple header bar:
- 3-4 items listed vertically: [ITEM 1], [ITEM 2], [ITEM 3]
- Timeline: "[TIMELINE]"
- Gate: "[METRIC]"

Thick forward arrows between panels labeled "Gate Review".

STYLE: Clean, minimal, flat design. Each phase slightly more vibrant than the last
(desaturated left, saturated right — visual progress). Sans-serif font. No hex codes.
```

---

## Template 6: Authentication Flow

**Use case:** Technical deep-dive on auth. Architect audience.

```
Create a technical authentication flow diagram for an enterprise identity presentation.

DIAGRAM TYPE: Left-to-right authentication sequence
LAYOUT: Horizontal flow. White background. 16:9 aspect ratio.

LEFT: Icon/box for "[USER / BROWSER]"
CENTER-LEFT: Box for "[SERVICE PROVIDER / APP]"
CENTER: Large box for "[IDENTITY PROVIDER e.g. Okta]" with teal fill
CENTER-RIGHT: Box for "[MFA SERVICE]" (if applicable)
RIGHT: Box for "[PROTECTED RESOURCE]"

FLOW (numbered sequence):
1. User requests access to Service Provider (arrow right)
2. SP redirects to IdP (arrow right, labeled "[PROTOCOL e.g. SAML Redirect]")
3. IdP authenticates user (internal arrow)
4. IdP issues assertion (arrow left back to SP, labeled "[SAML Assertion / ID Token]")
5. SP grants access to resource (arrow right)

NUMBER each step with circled digits on the arrows.

STYLE: Flat design, enterprise technical diagram. Blue arrows for auth flow.
Teal fill on IdP. Slate gray on other components. White background.
Numbered sequence callouts. No hex codes.
```

---

## Prompt Modifiers

Add these to any template based on context:

**For CISO audience:** Add "Include a compliance badge labeled [FRAMEWORK] on [COMPONENT]."

**For executive audience:** Add "Remove all protocol labels. Replace connection labels with business outcomes: 'Auto-provision access', 'Single sign-on'."

**For before/after:** Add "The current state should look visually more complex and dense than the future state. The simplicity of the future state IS the value proposition."

**For customer-specific:** Replace every generic label with the customer's actual system names from discovery.
