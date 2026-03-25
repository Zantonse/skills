# Architecture Diagram Color System

Semantic color assignments for IAM/IGA architecture diagrams. Colors encode deployment type, ownership, or status — never used purely for aesthetics.

## Primary Palette

| Role | Name | Hex | Prompt Name | WCAG on White |
|------|------|-----|-------------|---------------|
| Text / Borders | Near-black navy | `#1E293B` | "dark navy" | 14.7:1 |
| Canvas | Off-white | `#F8FAFC` | "white background" | N/A |
| Cloud / SaaS | Sky blue | `#0091DA` | "sky blue" | 3.1:1 (white text) |
| On-prem / Legacy | Cool gray | `#6B7280` | "slate gray" | 4.7:1 |
| Identity Platform | Teal | `#0D9488` | "teal" | 4.5:1 |

## Secondary Palette

| Role | Name | Hex | Prompt Name |
|------|------|-----|-------------|
| Governance / IGA | Deep purple | `#6B21A8` | "deep purple" |
| Risk / Gap | Amber | `#D97706` | "amber orange" |
| Critical Violation | Red | `#DC2626` | "red" (sparingly) |
| Compliance / OK | Forest green | `#166534` | "forest green" |
| PAM / Privileged | Purple-blue | `#4C1D95` | "deep indigo" |

## Callout Card Backgrounds

| Use | Background | Border | Text |
|-----|-----------|--------|------|
| Risk callout | `#FEF3C7` | `#D97706` | `#92400E` |
| Compliance badge | `#DCFCE7` | `#16A34A` | `#14532D` |
| Protocol badge | `#EFF6FF` | `#2563EB` | `#1D4ED8` |
| Metric card | `#FFFFFF` | `#CBD5E1` | `#1E293B` |

## Zone Fill Colors

| Zone | Fill | Border |
|------|------|--------|
| User / Device | `#FFFFFF` | None or `#E2E8F0` |
| On-Premises | `#F1F5F9` | `#6B7280` solid 2px |
| DMZ / Gateway | `#FFF7ED` | `#D97706` dashed 2px |
| Cloud Identity | `#EFF6FF` | `#2563EB` solid 2px |
| SaaS Apps | `#F0FDF4` | `#16A34A` solid 1px |
| Governance | `#FAF5FF` | `#7C3AED` solid 2px |

## Arrow Colors

| Flow Type | Color | Hex | Style |
|-----------|-------|-----|-------|
| Authentication (SAML, OIDC) | Blue | `#2563EB` | Solid 2px |
| Provisioning (SCIM, LDAP) | Teal | `#0D9488` | Dashed (async) or solid (real-time) |
| Governance / Audit | Purple | `#7C3AED` | Dash-dot |
| HR Inbound | Slate | `#475569` | Solid 1px, unidirectional |
| Risk / Violation | Red | `#DC2626` | Solid 2px with warning |

## Accessibility Rules

1. Never encode meaning in color alone — always add shape, icon, or text label
2. Minimum 4.5:1 contrast for body text on colored backgrounds
3. Red/green combinations must include shape differentiation (check vs. X)
4. All diagrams must be legible in grayscale print
