# Lucid MCP Shape Registry for IAM Architecture Diagrams

Reference for `lucid_create_diagram_from_specification`. All shape type names are exact — wrong types produce `"invalid_file"` 400 errors.

Before calling the tool, **always read `lucid://diagram-specification`** to get the full spec. This file is a curated IAM-specific quick-reference only.

---

## IAM Component → Shape Mapping

| IAM Component | `type` | Notes |
|---|---|---|
| Okta / Generic IdP | `rectangleContainer` | Use `containerTitle: {text: "Okta WIC"}` — no `text` property on containers |
| SaaS Application | `roundedRectangleContainer` | Use `containerTitle` for name |
| On-prem / Legacy App | `rectangle` | Sharp corners = on-prem convention |
| Active Directory / LDAP | `database` | Flowchart library cylinder shape |
| Policy Decision Point | `decision` | Flowchart library diamond |
| Security Gateway / PEP | `hexagon` | Standard library hexagon |
| Approval Workflow | `process` | Flowchart library rectangle |
| Auth Flow Start/End | `terminator` | Flowchart library oval |
| Privileged Vault | `database` | Flowchart library; add amber fill |
| Risk Annotation | `note` | Flowchart library; amber fill |
| Trust Zone Boundary | `rectangleContainer` | Transparent fill `#00000000`, dashed stroke |

---

## AWS Named Shapes (`type: "namedShape"`)

All default to `#DD344C` fill. Override with `style.fill.color`.

### IAM / Identity (Security Category)

| `className` | Label |
|---|---|
| `ArchAWSIdentityandAccessManagementAWS2024` | AWS IAM |
| `ArchAWSIAMIdentityCenterAWS2024` | IAM Identity Center (SSO) |
| `ArchAmazonCognitoAWS2024` | Amazon Cognito (CIAM) |
| `ArchAWSDirectoryServiceAWS2024` | AWS Directory Service |
| `ResAWSDirectoryServiceAWSManagedMicrosoftADAWS2024` | AWS Managed Microsoft AD |
| `ResAWSDirectoryServiceADConnectorAWS2024` | AD Connector |
| `ArchAWSSecretsManagerAWS2024` | AWS Secrets Manager |
| `ArchAWSCertificateManagerAWS2024` | ACM |
| `ArchAWSCloudHSMAWS2024` | CloudHSM |
| `ArchAWSKeyManagementServiceAWS2024` | KMS |
| `ArchAmazonVerifiedPermissionsAWS2024` | Verified Permissions |
| `ArchAWSSSOAWS2024` | AWS SSO (legacy) |
| `ResAWSIdentityAccessManagementRoleAWS2024` | IAM Role |
| `ResAWSIdentityAccessManagementMFATokenAWS2024` | MFA Token |
| `ResAWSIdentityAccessManagementAWSSTSAWS2024` | AWS STS |
| `ResAWSIdentityAccessManagementPermissionsAWS2024` | IAM Permissions |
| `ArchAWSSecurityHubAWS2024` | Security Hub |
| `ArchAmazonGuardDutyAWS2024` | GuardDuty |
| `ArchAWSAuditManagerAWS2024` | Audit Manager |

### AWS Container Shapes (`type: "namedContainer"`)

| `className` | Label | Default border |
|---|---|---|
| `AWSCloudAWS2024` | AWS Cloud | `#242f3e` |
| `RegionAWS2024` | Region | `#00a4a6` |
| `AvailabilityZoneAWS2024` | Availability Zone | `#00a4a6` |
| `VirtualPrivateCloudVPCAWS2024` | VPC | `#8C4FFF` |
| `PrivateSubnetAWS2024` | Private Subnet | `#00a4a6` |
| `PublicSubnetAWS2024` | Public Subnet | `#7aa116` |
| `SecurityGroupAWS2024` | Security Group | `#dd344c` |
| `AWSAccountAWS2024` | AWS Account | `#242f3e` |
| `CorporateDataCenterAWS2024` | Corporate Data Center | gray |
| `GenericGroupAWS2024` | Generic Group | gray |

---

## Azure Named Shapes (`type: "namedShape"`)

### Identity Category

| `className` | Label |
|---|---|
| `AzureActiveDirectoryAzure2021` | Azure Active Directory / Entra ID |
| `AzureADB2CAzure2021` | Azure AD B2C (CIAM) |
| `AzureADDomainServicesAzure2021` | Azure AD Domain Services |
| `AzureADIdentityProtectionAzure2021` | Azure AD Identity Protection |
| `ActiveDirectoryConnectHealthAzure2021` | AD Connect Health |
| `AppRegistrationsAzure2021` | App Registrations |
| `EnterpriseApplicationsAzure2021` | Enterprise Applications |
| `IdentityGovernanceAzure2021` | Identity Governance |
| `ManagedIdentitiesAzure2021` | Managed Identities |
| `ConditionalAccessAzure2021` | Conditional Access |
| `GroupsAzure2021` | Groups |
| `UsersAzure2021` | Users |
| `KeyVaultsAzure2021` | Key Vaults |

### Azure Container Shapes (`type: "namedContainer"`)

| `className` | Label |
|---|---|
| `SubscriptionAzure2021` | Azure Subscription |
| `ResourceGroupAzure2021` | Resource Group |
| `VirtualNetworkAzure2021` | Virtual Network |
| `SubnetAzure2021` | Subnet |

---

## GCP Named Shapes (`type: "namedShape"`)

### IAM / Security Category

| `className` | Label |
|---|---|
| `GCP2021IdentityAndAccessManagementIcon` | Cloud IAM |
| `GCP2021IdentityawareProxyIcon` | Identity-Aware Proxy |
| `GCP2021IdentityPlatformIcon` | Identity Platform (CIAM) |
| `GCP2021WorkloadIdentityPoolIconV2` | Workload Identity Pool |
| `GCP2021BeyondcorpIcon` | BeyondCorp (Zero Trust) |
| `GCP2021PolicyAnalyzerIcon` | Policy Analyzer |
| `GCP2021SecretManagerIcon` | Secret Manager |

### GCP Container Shapes (`type: "namedContainer"`)

| `className` | Label |
|---|---|
| `GCP2021GoogleCloudLogoContainer` | Google Cloud |
| `GCP2021ContainerRegion` | Region |
| `GCP2021ContainerSubNetwork` | Subnet |
| `GCP2021ContainerZone` | Zone |

---

## No Vendor IdP Shape Libraries

There are **no Lucid shape libraries** for Okta, Auth0, Ping Identity, ForgeRock, SailPoint, or CyberArk. Represent these as:

| Vendor | Shape | Title |
|---|---|---|
| Okta WIC | `rectangleContainer` | `containerTitle: {text: "Okta WIC"}` |
| Okta OIG | `rectangleContainer` | `containerTitle: {text: "Okta OIG"}` |
| Auth0 / CIC | `rectangleContainer` | `containerTitle: {text: "Auth0 / CIC"}` |
| SailPoint ISC | `rectangleContainer` | `containerTitle: {text: "SailPoint ISC"}` |
| CyberArk PAM | `rectangleContainer` | `containerTitle: {text: "CyberArk PAM"}` |
| Ping Identity | `rectangleContainer` | `containerTitle: {text: "Ping Identity"}` |

Use `style.stroke` color to match the semantic zone (teal for identity platform, purple for governance, amber for privileged access).

---

## Color Hex Codes (Required — Never Use Color Names in Lucid JSON)

| Role | Hex | `textColor` |
|---|---|---|
| Identity Platform (Okta) | `#0D9488` | `#FFFFFF` |
| Cloud / SaaS apps | `#0091DA` | `#FFFFFF` |
| On-prem / Legacy | `#6B7280` | `#FFFFFF` |
| Governance / IGA (OIG, SailPoint) | `#6B21A8` | `#FFFFFF` |
| Risk / Current-state pain | `#D97706` | `#FFFFFF` |
| Compliant / Future-state | `#166534` | `#FFFFFF` |
| PAM / Privileged | `#4C1D95` | `#FFFFFF` |
| Zone background fill | `#F8FAFC` | N/A |
| Transparent zone boundary | `#00000000` | N/A |
| Borders / arrows (default) | `#1E293B` | N/A |
| Auth flow arrows (SAML/OIDC) | `#2563EB` | N/A |
| Provisioning arrows (SCIM) | `#0D9488` | N/A |
| Governance flow arrows | `#7C3AED` | N/A |
| Risk / violation arrows | `#DC2626` | N/A |
| AWS Security default fill | `#DD344C` | `#FFFFFF` |
| Azure Identity default fill | `#50E6FF` | `#1E293B` |

---

## IAM Zone Container Patterns

### Standard Zone Layout (Hub-and-Spoke)

Use `rectangleContainer` per zone. Set `assistedLayout: true` on each. Pass `use_assisted_layout: false` to the tool call (because containers are present).

```
Zone: User / Device    → fill #FFFFFF, stroke #E2E8F0 solid 1px
Zone: On-Premises      → fill #F1F5F9, stroke #6B7280 solid 2px
Zone: DMZ / Gateway    → fill #FFF7ED, stroke #D97706 dashed 2px
Zone: Cloud Identity   → fill #EFF6FF, stroke #2563EB solid 2px
Zone: SaaS Apps        → fill #F0FDF4, stroke #16A34A solid 1px
Zone: Governance       → fill #FAF5FF, stroke #7C3AED solid 2px
```

### Swimlane Layout (Provisioning / JML)

Use `swimLanes` with `vertical: false` (stacked rows = actors as lanes).

```json
{
  "type": "swimLanes",
  "boundingBox": {"x": 0, "y": 0, "w": 1400, "h": 600},
  "vertical": false,
  "assistedLayout": true,
  "titleBar": {"height": 40, "verticalText": false},
  "lanes": [
    {"title": "HR System (Workday)", "width": 150, "headerFill": "#6B7280", "laneFill": "#F1F5F9"},
    {"title": "Okta Lifecycle Mgmt", "width": 150, "headerFill": "#0D9488", "laneFill": "#EFF6FF"},
    {"title": "Target Apps",         "width": 150, "headerFill": "#0091DA", "laneFill": "#F0FDF4"},
    {"title": "Governance / OIG",    "width": 150, "headerFill": "#6B21A8", "laneFill": "#FAF5FF"}
  ]
}
```

Lane `width` values (150×4=600) must equal `boundingBox.h` for `vertical: false`.

---

## Common Gotchas

| Gotcha | Rule |
|---|---|
| Containers have no `text` property | Use `containerTitle: {text: "..."}` instead |
| `text` shapes have no `style` | Don't add `style` to `type: "text"` shapes |
| Color names cause failures | Always use hex: `"#0D9488"` not `"teal"` |
| No emoji in any `text` field | Renders as black boxes |
| Assisted layout breaks containers | Set tool `use_assisted_layout: false` when using swimLanes or nested containers |
| Shape IDs must be unique strings | Never reuse IDs; never use integer IDs |
| `position` on endpoints: both or neither | Smart lines omit `position` on both endpoints |
| Container containment is strict | Entire shape bounding box must fit inside container — no edge-touching |
| swimLane lane widths must sum correctly | Columns (`vertical:true`): sum = `boundingBox.w`; Rows (`vertical:false`): sum = `boundingBox.h` |
| BPMN braceNote properties are top-level | `rightFacing` and `braceWidth` are NOT inside a `shape` sub-object |
| `lucidCard` has no `text` property | Use `title`, `description`, `status` fields |
| Shape z-index = array order | Later shapes appear in front; put background containers first |
| 2MB document.json limit | Use compact JSON (no indentation) for large diagrams |
| ERD / DFD / ArchiMate not supported | These shape libraries are unsupported in MCP as of May 2026 |
