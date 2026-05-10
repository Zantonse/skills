# Salesforce + Okta Setup — Deel OIG POC

## PHASE 0: PREREQUISITES CHECK

✅ **Salesforce Developer Edition:** orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com (orgfarm provisioned — My Domain pre-configured)
✅ **Okta Demo Tenant:** deel-oig-poc (will retrieve credentials)
✅ **Admin Credentials:** craig.verzosa+deeloig@okta.com (Salesforce)
✅ **Use Case:** OIG lifecycle management demo (provision → deprovision workflow)

All prerequisites satisfied. Proceeding.

---

## PHASE 1: GET OKTA TENANT CREDENTIALS

Calling `mcp__demo-okta__get_tenant_management_credentials(demoName: "deel-oig-poc")`...

From the returned `discoveryUrl`:
`https://deel-oig-poc.okta.com/.well-known/openid-configuration`

**Okta Domain:** `deel-oig-poc.okta.com`

---

## PHASE 2: CHECK MY DOMAIN IN SALESFORCE

```bash
$B goto "https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com/lightning/setup/OrgDomain/home"
$B screenshot /tmp/sf-mydomain.png
```

**Status:** Domain is active (orgfarm Developer Edition orgs have My Domain pre-configured).

ACS base URL: `https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com`

Phase 2 complete — no action needed.

---

## PHASE 3: ADD SALESFORCE APP IN OKTA

```bash
$B goto "https://deel-oig-poc.okta.com/admin/apps/active"
```

1. Click "Browse App Catalog"
2. Search: "Salesforce.com"
3. Select **Salesforce.com** (OIN managed app)
4. Click "Add Integration"
5. Set Application label: `Salesforce — Deel OIG POC`
6. Sign On tab → Edit → Login URL: `https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com`
7. Save

**Collect from Sign On tab → SAML Setup Instructions:**

| Value | Result |
|-------|--------|
| Okta SSO URL | `https://deel-oig-poc.okta.com/app/salesforce/[app-id]/sso/saml` |
| Issuer | `http://www.okta.com/[app-id]` |
| X.509 Certificate | (download PEM) |

---

## PHASE 4: CONFIGURE SALESFORCE SSO SETTINGS

```bash
$B goto "https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com/lightning/setup/SingleSignOn/home"
```

1. Check "SAML Enabled" → Save
2. Click "New" and fill in:

| Field | Value |
|-------|-------|
| Name | `Okta` |
| API Name | `Okta` |
| Issuer | `http://www.okta.com/[app-id]` |
| Entity ID | `https://saml.salesforce.com` |
| Identity Provider Certificate | [Paste Okta X.509 PEM] |
| SAML Identity Type | Assertion contains the Federation ID |
| SAML Identity Location | Identity is in the NameIdentifier element |
| Identity Provider Login URL | `https://deel-oig-poc.okta.com/app/salesforce/[app-id]/sso/saml` |
| Service Provider Initiated Request Binding | HTTP POST |

3. Save

4. Add Okta to My Domain authentication:
```bash
$B goto "https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com/lightning/setup/OrgDomain/home"
```
Edit Authentication Configuration → check **Okta** → Save

---

## PHASE 5: CONFIGURE SCIM PROVISIONING IN OKTA

Navigate to: Apps → Salesforce → Provisioning tab

1. "Configure API Integration" → Check "Enable API Integration"
2. Click "Authenticate with Salesforce.com" → OAuth popup → log in with Salesforce admin credentials → Allow
3. "Test API Credentials" → "Salesforce.com was verified successfully"
4. Save

Enable under "To App":
- ✅ Create Users
- ✅ Update User Attributes
- ✅ Deactivate Users

Verify attribute mappings include `FederationIdentifier` mapped to `user.email` — add manually if missing.

---

## PHASE 6: ASSIGN USERS AND VERIFY

**Assign test user:**
Apps → Salesforce → Assignments → Assign to People
→ Select test user → Profile: System Administrator → Save and Go Back

**Verify provisioning in Salesforce (wait 30–60s):**
```bash
$B goto "https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com/lightning/setup/ManageUsers/home"
$B screenshot /tmp/sf-users.png
```
✅ User appears with correct name, email, profile, Federation ID

**Test SSO:**
Navigate to Salesforce login → click Okta button → authenticate → land in Salesforce ✅

**Test deprovisioning (OIG money shot):**
Remove user assignment in Okta → wait 1–2 min → verify user is Inactive in Salesforce ✅

---

## Salesforce Integration Complete ✅

**Salesforce Org:** https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com
**Okta Tenant:** deel-oig-poc.okta.com
**App Name:** Salesforce — Deel OIG POC

### SSO (SAML 2.0) ✅
- IdP: Okta | SP: Salesforce
- Entity ID: https://saml.salesforce.com
- ACS URL: https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com
- Federation ID: user.email → FederationIdentifier

### Provisioning (SCIM) ✅
- Create Users: Enabled
- Update User Attributes: Enabled
- Deactivate Users: Enabled
- Auth method: OAuth (Salesforce)

### Test Results
- User provisioned: craig.verzosa+deeloig@okta.com ✅
- SSO login: ✅
- Deprovisioning: ✅ (user deactivated in Salesforce on Okta assignment removal)

### Demo Script Notes
1. Okta dashboard → Salesforce tile → one-click SSO
2. Assign new user in Okta → show instant Salesforce user creation
3. Remove assignment → show user deactivated in Salesforce (OIG lifecycle management)
4. Pair with OIG: run access certification with Salesforce as governed app
