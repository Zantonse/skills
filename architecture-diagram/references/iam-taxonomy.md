# IAM Component Taxonomy

Standard components for identity and access management architecture diagrams. Derived from CISA ICAM Reference Architecture v1.3, IDPro Body of Knowledge, NIST SP 800-207, and vendor documentation (Okta, SailPoint, Microsoft Entra, Ping Identity, Broadcom).

## Identity Authority Layer (Source of Truth)

| Component | Labels | Shape | Color | Arrow Direction |
|-----------|--------|-------|-------|----------------|
| HR System | "HR System (Workday)", "HRIS" | Sharp rectangle | Slate gray | Unidirectional out → IGA/IdP |
| Active Directory | "Active Directory", "AD" | Cylinder | Slate gray | Unidirectional out → Connector |
| LDAP Directory | "LDAP Directory", "Red Hat DS" | Cylinder | Slate gray | Unidirectional out → Connector |
| Identity Store | "User Store", "Identity Register" | Cylinder | Navy blue | Bidirectional ↔ IdP |

Mark authoritative sources with a "Source of Truth" sub-label or gold border.

## Identity Management Layer (Control Plane)

| Component | Labels | Shape | Color | Notes |
|-----------|--------|-------|-------|-------|
| Identity Provider | "Okta WIC", "Entra ID", "PingFederate" | Rounded rectangle | Vendor brand color | Central hub |
| Directory Connector | "Okta AD Agent", "Azure AD Connect" | Double-arrow-in-box | Gray + blue outline | Straddles on-prem/cloud |
| SCIM Engine | "Provisioning Engine", "SCIM Gateway" | Rounded rectangle | Teal | Bidirectional is correct |
| Identity Broker | "Federation Hub" | Hexagon | Navy | M&A and multi-IdP |
| MFA Service | "Adaptive MFA", "Okta Verify" | Shield icon | Amber | Inline in auth flow |

## Access Management Layer (Enforcement)

| Component | Labels | Shape | Color | NIST Mapping |
|-----------|--------|-------|-------|-------------|
| Policy Decision Point | "Policy Engine", "Conditional Access" | Diamond/hexagon | Deep navy | PDP (PE + PA) |
| Policy Enforcement Point | "Access Gateway", "PEP" | Hexagon | Amber | At each resource boundary |
| Access Gateway | "Okta Access Gateway", "Ping Access" | Hexagon | Amber | DMZ placement |
| Session Manager | "Token Service" | Cylinder | Teal | Auth tier |

## Governance Layer (IGA)

| Component | Labels | Shape | Color |
|-----------|--------|-------|-------|
| IGA Platform | "SailPoint ISC", "Saviynt", "Okta OIG" | Rounded rectangle | Deep purple |
| Workflow Engine | "Approval Engine", "Access Request Workflow" | Process box | Light purple |
| Entitlement Catalog | "Entitlement Catalog", "Access Profiles" | Cylinder | Light purple |
| SoD Policy Engine | "SoD Engine", "Conflict Detection" | Diamond | Red-amber |
| Certification Manager | "Access Reviews", "Certification Engine" | Rounded rectangle | Purple |
| Access Request Portal | "Self-Service Portal" | Browser icon | Blue |
| Identity Analytics | "AI Risk Scoring" | Chart icon | Deep purple |

## Connector Types

| Type | Visual | Arrow Style | Direction |
|------|--------|------------|-----------|
| HR Connector | Plug icon | Solid, thick | Inbound only |
| SCIM 2.0 | REST badge | Solid or dashed | Bidirectional |
| LDAP | Network icon | Solid | Bidirectional |
| JDBC | Database icon | Dashed | Bidirectional |
| CSV / Flat File | File + clock | Dashed | Usually inbound |
| Cloud API | Cloud + REST | Solid | Bidirectional |

## Target Applications

| Category | Examples | Zone | Shape |
|----------|---------|------|-------|
| SaaS | Microsoft 365, Salesforce, ServiceNow | Cloud (sky blue) | Rounded rectangle |
| On-Premises | SAP ERP, Legacy apps, Mainframe | On-prem (gray) | Sharp rectangle |
| Cloud Infra | AWS IAM, Azure RBAC, GCP IAM | Cloud (sky blue) | Cloud outline |
| PAM | CyberArk, Delinea | Separate lane | Hexagon, purple |

## Zone Structure

| Zone | Fill | Border | Contents |
|------|------|--------|----------|
| User / Device | White | None or thin gray | End users, browsers, devices |
| On-Premises | Light gray | Gray solid 2px | AD, LDAP, legacy apps, agents |
| DMZ | Light amber | Amber dashed 2px | Reverse proxy, gateway, WAF |
| Cloud Identity | Light blue | Blue solid 2px | IdP, MFA, provisioning |
| SaaS Apps | Light green | Green solid 1px | M365, Salesforce, ServiceNow |
| Governance | Light purple | Purple solid 2px | IGA, SoD, certifications |

## Arrow Conventions

| Flow | Color | Style | Label Convention |
|------|-------|-------|-----------------|
| Authentication | Blue | Solid 2px | Protocol: "SAML 2.0", "OIDC" |
| Provisioning | Teal | Dashed (async) or solid | "Provision / Deprovision (SCIM)" |
| Governance | Purple | Dash-dot | "Certification Review", "SoD Check" |
| HR Inbound | Slate | Solid 1px | "JML Events" — always unidirectional |
| Risk / Violation | Red | Solid 2px | "SoD Violation", "Block" |
