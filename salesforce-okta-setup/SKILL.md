---
name: salesforce-okta-setup
description: |
  Configure Salesforce Developer Edition as a SAML SSO + SCIM/LCM application connected to
  an Okta demo tenant. Use this skill whenever an SE needs to add Salesforce to an Okta demo
  environment — for ILM/LCM demos, OIG provisioning walkthroughs, or any SSO use case.

  Invoke immediately when you see: "set up Salesforce in my demo", "add Salesforce SSO",
  "configure Salesforce provisioning", "Salesforce SCIM", "integrate Salesforce with Okta",
  "Salesforce OIG demo", or "attach Salesforce to my demo tenant". Also triggers when the
  user provides a Salesforce org URL (*.salesforce.com or *.force.com) and mentions Okta.

  Uses the browse tool for Salesforce UI navigation and Okta MCP for the Okta-side
  configuration. Produces a working SAML + SCIM integration ready to demo in under 30 minutes.
---

# salesforce-okta-setup

End-to-end configuration of Salesforce Developer Edition with Okta — SAML SSO and SCIM
provisioning, both sides fully configured. Output: a working integration ready to demo
for ILM, OIG lifecycle management, and SSO use cases.

## What This Produces

```
Okta (IdP)                       Salesforce (SP)
──────────────────────────────────────────────────────
SAML App (Salesforce OIN)  ────► My Domain + SSO Settings
SCIM Provisioning          ────► Connected App (OAuth)
User Lifecycle (assign/    ────► User create / update /
  deactivate)                     deactivate
```

## Prerequisites Check

Before starting, verify:
- [ ] Salesforce Developer Edition org provisioned (developer.salesforce.com/signup)
- [ ] Okta demo tenant provisioned via `/demo-provision` or already exists
- [ ] Salesforce admin credentials (email + password)
- [ ] Access to the Okta demo tenant (via demo-okta MCP)

If the Salesforce org doesn't exist yet, guide the user to sign up at
https://developer.salesforce.com/signup and wait for the verification email before
proceeding. The org URL format will be:
`https://[orgid]-dev-ed.develop.lightning.force.com`

## Inputs to Collect

Gather these before Phase 1. Most will come from the user's message — only ask for
what's missing.

| Input | Example | Where to find it |
|-------|---------|-----------------|
| Salesforce org URL | `https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com` | Verification email or browser URL |
| Salesforce admin username | `craig.verzosa+deeloig@okta.com` | Whatever was used at signup |
| Salesforce admin password | `Admiral1$$` | Whatever was set after email verification |
| Okta demo name | `deel-oig-poc` | From `demo-provision` output or `/list_demos` |

---

## Phase 1 — Get Okta Tenant Credentials

Get management credentials for the Okta demo tenant so you can configure it via API.

```
mcp__demo-okta__get_tenant_management_credentials(demoName: "<demo-name>")
```

This returns an object like:
```json
{
  "type": "okta",
  "clientId": "0oaXXX...",
  "discoveryUrl": "https://<okta-domain>/.well-known/openid-configuration",
  "tokenEndpoint": "https://<okta-domain>/oauth2/v1/token"
}
```

Extract the **Okta domain** from `discoveryUrl` — everything between `https://` and
`/.well-known/`. This is your `<okta-domain>` for all subsequent steps.

If the demo uses an API token instead, it will be in the credentials object. Use
`SSWS <token>` in Authorization headers.

---

## Phase 2 — Check My Domain in Salesforce

My Domain is required for SSO. Check its status before doing anything else.

```bash
$B goto "<sf-org-url>/lightning/setup/OrgDomain/home"
$B screenshot /tmp/sf-mydomain.png
```

**If "Your domain is active"** (common for orgfarm-provisioned orgs) → skip to Phase 3.

**If domain is not yet configured:**
1. Enter a domain name (e.g., `okta-demo-<yourname>`)
2. Click "Check Availability" then "Register Domain"
3. Wait 2-5 minutes for DNS propagation
4. Click "Deploy to Users" when the status shows ready

Record the resulting domain: `https://<domain>.my.salesforce.com`

For orgfarm Developer Edition orgs (URLs containing `develop.lightning.force.com`), the
My Domain is pre-configured — the org URL itself is the ACS base URL.

---

## Phase 3 — Add Salesforce App in Okta

Navigate to the Okta Admin Console to add the Salesforce OIN app.

```bash
$B goto "https://<okta-domain>/admin/apps/active"
$B screenshot /tmp/okta-apps.png
```

### Add the Salesforce.com OIN Integration

1. Click "Browse App Catalog"
2. Search for "Salesforce.com"
3. Select **"Salesforce.com"** (the Salesforce-managed OIN app — not "Salesforce Sandbox")
4. Click "Add Integration"

### Configure the App

On the General tab:
- **Application label**: `Salesforce` (or `Salesforce - <customer-name>` for multi-tenant demos)

On the Sign On tab, click Edit:
- **Login URL**: `https://<sf-domain>.my.salesforce.com`
  - For orgfarm orgs: use `https://<orgid>-dev-ed.develop.lightning.force.com`

Click Save.

### Collect SAML Values

On the Sign On tab, scroll to "View SAML setup instructions" or "Metadata details":

Record these — you'll need them in Phase 4:

| Value | Where to find |
|-------|--------------|
| **Okta SSO URL** | Identity Provider Single Sign-On URL |
| **Okta Issuer** | Identity Provider Issuer (format: `http://www.okta.com/<app-id>`) |
| **Okta Certificate** | X.509 Certificate (download or copy PEM) |
| **Metadata URL** | `https://<okta-domain>/app/salesforce/<app-id>/sso/saml/metadata` |

```bash
$B screenshot /tmp/okta-saml-values.png
```

---

## Phase 4 — Configure Salesforce SSO Settings

### Enable SAML in Salesforce

```bash
$B goto "<sf-org-url>/lightning/setup/SingleSignOn/home"
```

1. Check "SAML Enabled" at the top
2. Click Save

### Create the Okta SSO Configuration

Click "New" and fill in:

| Field | Value |
|-------|-------|
| Name | `Okta` |
| API Name | `Okta` |
| Issuer | `http://www.okta.com/<okta-app-id>` (from Phase 3) |
| Entity ID | `https://saml.salesforce.com` |
| Identity Provider Certificate | Paste the Okta X.509 certificate PEM |
| SAML Identity Type | **Assertion contains the Federation ID** |
| SAML Identity Location | **Identity is in the NameIdentifier element** |
| Identity Provider Login URL | The Okta SSO URL (from Phase 3) |
| Service Provider Initiated Request Binding | **HTTP POST** |

Click Save.

**Record the "Salesforce Login URL"** shown on the SSO config page — this is the SP-initiated URL you can use for testing.

### Add Okta to My Domain Authentication

```bash
$B goto "<sf-org-url>/lightning/setup/OrgDomain/home"
```

1. Click "Edit" in the Authentication Configuration section
2. Under Authentication Services, check **Okta**
3. Optionally uncheck "Login Page" to force SSO (only for pure demo tenants)
4. Click Save

---

## Phase 5 — Configure SCIM Provisioning in Okta

### 5a — Create a Connected App in Salesforce

Okta's Salesforce provisioning uses OAuth via a Salesforce Connected App. Use either a classic **Connected App** or a newer **External Client App** (via App Manager) — both work, but Developer Edition / orgfarm orgs often require the External Client App path (see Common Issues).

In Salesforce Setup, search for **"App Manager"** in Quick Find and open it.

**Option A — External Client App (recommended for Developer Edition / orgfarm orgs):**

1. Click **"New External Client App"**
2. Fill in:
   - **External Client App Name**: `Okta_SCIM`
   - **API Name**: `Okta_SCIM`
   - **Contact Email**: (admin email)
3. Under **OAuth Settings**, enable OAuth and configure **exactly** as follows:

| Setting | Value |
|---------|-------|
| **Callback URL** | `https://system-admin.okta.com/admin/app/generic/oauth20redirect` |
| Enable for Device Flow | ❌ disabled |
| Use digital signatures | ❌ disabled |
| **OAuth Scopes** | `Manage user data via APIs (api)` + `Perform requests at any time (refresh_token, offline_access)` |
| Require PKCE | ❌ disabled |
| Require Secret for Web Server Flow | ✅ enabled |
| Require Secret for Refresh Token Flow | ✅ enabled |
| Enable Client Credentials Flow | ❌ disabled |

> **The callback URL is fixed — copy it as-is.** It's `https://system-admin.okta.com/admin/app/generic/oauth20redirect` for every Okta org. Do not substitute your org domain.

4. Save the External Client App
5. Go to the app's detail page → **"Manage Consumer Details"** → verify identity if prompted
6. Record the **Consumer Key** and **Consumer Secret**
7. Click **"Manage"** → verify **Refresh Token Policy** is set to **"Refresh token is valid until revoked"**

Set IP Relaxation to **"Relax IP restrictions"** under the app's OAuth policies.

**Option B — Classic Connected App:**

Follow Salesforce's "Configure Basic Connected App Settings" then "Enable OAuth Settings for API Integration" with the same callback URL and scope values from Option A above.

### 5b — Authenticate Okta to Salesforce

Navigate to the Salesforce app's Provisioning tab in Okta:

```bash
$B goto "https://<okta-domain>/admin/app/salesforce/<app-id>/provisioning/connection"
```

1. Click **"Configure API Integration"**
2. Check **"Enable API Integration"**
3. **Enter the credentials from Step 5a FIRST — this is required before Authenticate will work:**
   - **OAuth Consumer Key**: (from the External Client App)
   - **OAuth Consumer Secret**: (from the External Client App)
   
   > **Critical:** The Consumer Key and Consumer Secret must be populated in the form fields **before** clicking "Authenticate with Salesforce.com". The button is gated on having credentials present. If you click Authenticate with empty fields, the request will fail silently or return an unhelpful error.
   
   > **When transferring to a new Okta org:** If you are moving a working SCIM integration from one Okta tenant to another, you must **manually re-enter** the Consumer Key and Consumer Secret into the new app. Credentials from the old Okta org do not carry over — each Okta app stores its own copy. Re-use the same Salesforce Connected App credentials; the callback URL (`https://system-admin.okta.com/admin/app/generic/oauth20redirect`) is the same for all Okta orgs so no Salesforce-side changes are needed.

4. Click **"Authenticate with Salesforce.com"**
   - A popup opens — log in with Salesforce admin credentials and click Allow
5. Click **"Test API Credentials"** — expect: "Salesforce.com was verified successfully"
6. Click **Save**

> **Why External Client App:** Classic Connected Apps use an older OAuth credential format that Okta's Salesforce SCIM connector rejects during the post-OAuth admin verification step. External Client Apps (created via App Manager in Lightning Setup) generate credentials in the format Okta expects. This applies specifically to Developer Edition orgs with `develop.my.salesforce.com` URLs and newer Lightning-first orgs.

> **Demo tip:** Before a customer meeting, always run "Test API Credentials" to confirm the OAuth token is still valid. Tokens expire if the authorizing admin's password was reset.

### 5b — Enable Provisioning Features

Under **"To App"**, click Edit and enable:
- ✅ **Create Users** — provisions new Okta users as Salesforce users on assignment
- ✅ **Update User Attributes** — syncs profile changes from Okta to Salesforce
- ✅ **Deactivate Users** — deactivates Salesforce user when removed from the Okta app (the OIG money shot)

Under **"To Okta"**: leave disabled unless you need reverse sync (not needed for demo).

Click **Save**.

### 5c — Configure Attribute Mappings

Go to **Provisioning > Attribute Mappings** (or "To App" > "Go to Profile Editor").

Verify these 5 critical mappings exist. Add any that are missing:

| Okta Attribute | Salesforce Field | Notes |
|----------------|-----------------|-------|
| `user.firstName` | `FirstName` | Required |
| `user.lastName` | `LastName` | Required |
| `user.email` | `Email` | Required |
| `user.login` | `Username` | Must be email format — Salesforce usernames are globally unique |
| `user.email` | `FederationIdentifier` | **Critical** — links the Okta identity to the Salesforce SSO record. Without this, SSO fails even when provisioning succeeds. |

**To add a missing mapping:**
1. Click "Add Mapping" or the pencil icon next to the Salesforce field
2. Set the Okta attribute source
3. Set Priority to "Required" for core fields
4. Save

**Optional demo-value mappings** (add these to show richer ILM):

| Okta Attribute | Salesforce Field | Why it matters |
|----------------|-----------------|----------------|
| `user.department` | `Department` | Shows org structure syncing |
| `user.title` | `Title` | Shows job role syncing |
| `user.mobilePhone` | `MobilePhone` | Shows full profile sync |
| `user.manager` | `ManagerId` | Advanced — requires manager's Salesforce ID lookup |

### 5d — Verify the Connected App Permissions (if provisioning fails)

If SCIM calls return 403 or users fail to create, the Salesforce integration user may lack API permissions:

```bash
$B goto "<sf-org-url>/lightning/setup/ManageUsers/home"
```

Find the admin user who authorized the OAuth connection. Click their profile and verify:
- ✅ **API Enabled** permission is on
- ✅ **Manage Users** permission is on (required to create users)
- ✅ **Modify All Data** or **Modify All Users** (required for deactivation)

For Developer Edition orgs, System Administrator profile has all of these by default. No action needed unless you see permission errors in Okta's provisioning tasks.

---

## Phase 6 — Assign Users, Verify Provisioning, and Test Deprovisioning

### 6a — Assign a Single Test User

In the Okta Salesforce app > **Assignments** tab:
1. Click **"Assign"** > **"Assign to People"**
2. Find your test user
3. In the assignment dialog, set:
   - **Salesforce Profile**: `System Administrator` (for demo orgs — gives full access)
   - Username field: confirm it's email format (auto-populated from `user.login`)
4. Click **"Save and Go Back"**

Provisioning runs asynchronously — typically within 30–60 seconds.

### 6b — Monitor the Provisioning Task

Check the task immediately to catch errors before you're in a customer meeting:

In the Okta Salesforce app, go to **Provisioning** > **Tasks** (or Dashboard > Tasks):

- ✅ **Success** — user was created in Salesforce
- ⚠️ **Pending** — still running, wait 30s and refresh
- ❌ **Failed** — click the failed task to see the exact error code

**Most common task failures:**

| Error in Tasks log | Root cause | Fix |
|-------------------|-----------|-----|
| `Profile mapping missing` | No Salesforce Profile set in assignment | Edit assignment → set Salesforce Profile |
| `FederationIdentifier not found` | Attribute mapping missing | Add `user.email → FederationIdentifier` in mappings |
| `INVALID_FIELD: Username` | Username not email format | Check `user.login` value in Okta — must be `name@domain.com` |
| `ALREADY_IN_USE: Username` | Another Salesforce org has this username globally | Change the Okta username to something unique (Salesforce usernames are globally unique across ALL orgs) |
| `401 Unauthorized` | OAuth token expired | Re-authenticate: Provisioning > Configure API Integration > Authenticate with Salesforce.com |
| `REQUEST_LIMIT_EXCEEDED` | Salesforce API limits hit | Wait and retry; Developer Edition orgs have a daily API call limit |

### 6c — Verify the User in Salesforce

```bash
$B goto "<sf-org-url>/lightning/setup/ManageUsers/home"
$B screenshot /tmp/sf-users-provisioned.png
```

Click the provisioned user and confirm all 5 fields:
- ✅ **First Name / Last Name** — matches Okta profile
- ✅ **Email** — matches Okta email
- ✅ **Username** — email format, matches `user.login`
- ✅ **Profile** — System Administrator (or whichever was set)
- ✅ **Federation ID** — must match the user's Okta email exactly (this is what links SSO to the account)

If Federation ID is blank, SSO will fail even though the user exists. Fix: update the FederationIdentifier attribute mapping and re-push the user (edit and save the assignment in Okta).

### 6d — Assign a Group (for bulk demo)

For a more impressive demo, assign a whole Okta group instead of individual users:

In Assignments tab > **"Assign"** > **"Assign to Groups"**:
1. Select a demo group (e.g., "Salesforce Users" or "Demo Users")
2. Set the default Salesforce Profile for the group
3. Save

All current group members are provisioned immediately. New members added to the group later are provisioned automatically — this is the live ILM demo.

### 6e — Test SSO Login

```bash
$B goto "<sf-org-url>"
```

The login page should show an **"Okta"** button (or your custom button label). Click it:
- Redirects to Okta login page → authenticate → lands in Salesforce ✅

If the button isn't visible: navigate directly to the SP-initiated URL:
```
https://<sf-domain>.my.salesforce.com/idp/login?app=0sp...
```
(Get the full URL from Salesforce Setup > Single Sign-On Settings > your Okta config > "Login URL")

Or launch from the Okta End User Dashboard tile — the Salesforce app tile triggers IdP-initiated SSO.

### 6f — Test Deprovisioning (OIG Demo — the key moment)

This is the step that closes OIG deals. Do it slowly so the customer can see it happen.

**In Okta:**
1. Go to the Salesforce app > Assignments tab
2. Find the test user
3. Click the **"X"** to remove the assignment
4. Confirm removal

**Immediately show the customer Salesforce:**
```bash
$B goto "<sf-org-url>/lightning/setup/ManageUsers/home"
```

Refresh after ~60 seconds. The user status changes from **Active** to **Inactive**.

> **Why "Inactive" not "Deleted"?** Salesforce can't delete users once they've been created (Salesforce audit trail constraint). Okta sends a SCIM `active: false` which Salesforce maps to deactivation. The user still exists in Salesforce but can no longer log in. This is the correct behavior — demonstrate it deliberately: "Access revoked in Okta, access revoked in Salesforce. That's lifecycle management."

**Re-provision:** Re-assign the user in Okta → Salesforce reactivates them. Demonstrate the full hire → terminate → rehire cycle if time permits.

---

## Output Summary

After completing all phases, produce this summary for the SE:

```
## Salesforce Integration Complete ✅

**Salesforce Org**: <org-url>
**Okta Tenant**: <okta-domain>
**App Name**: Salesforce (Okta app ID: <app-id>)

### SSO (SAML 2.0) ✅
- IdP: Okta
- SP: Salesforce
- Entity ID: https://saml.salesforce.com
- ACS URL: <sf-org-url>
- Okta SSO URL: https://<okta-domain>/app/salesforce/<app-id>/sso/saml

### Provisioning (SCIM) ✅
- Create Users: Enabled
- Update User Attributes: Enabled
- Deactivate Users: Enabled
- Auth method: OAuth (Salesforce Connected App)

### Test Results
- User provisioned: <test-user-email> ✅
- SSO login: ✅
- Deprovisioning: ✅

### Demo Script Notes
- Show Okta dashboard → one-click SSO to Salesforce
- Create a new user in Okta, assign Salesforce → show instant provisioning
- Remove assignment → show access revoked (Salesforce user deactivated)
- Pair with OIG: run an access certification campaign with Salesforce as a governed app
```

---

## Common Issues

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| **"Could not verify Salesforce administrator credentials"** | **Classic Connected App used instead of External Client App** | **Create the OAuth app via App Manager → New External Client App (not the classic Connected Apps page). Classic Connected Apps generate credentials Okta's verification rejects on Developer Edition / orgfarm orgs.** |
| "Authenticate with Salesforce.com" fails or returns unexpected error | Consumer Key and Secret not filled in before clicking Authenticate | Populate both OAuth credential fields first — the Authenticate button is gated on credentials being present. Without them the OAuth call cannot be made. |
| Transferring SCIM to a new Okta org — credentials rejected | Consumer Key and Secret not re-entered in the new Okta app | Credentials are per-app and don't transfer automatically. Re-enter the existing Consumer Key and Secret in the new app's provisioning form. No Salesforce-side changes needed — the callback URL (`https://system-admin.okta.com/admin/app/generic/oauth20redirect`) is the same for all Okta orgs. |
| "SAML assertion invalid" at login | Issuer URL mismatch | Verify Issuer in Salesforce SSO Settings matches exactly `http://www.okta.com/<app-id>` |
| "Federation ID not found" | FederationIdentifier not mapped | Add `user.email → FederationIdentifier` in Okta attribute mappings |
| SCIM OAuth popup blocked | Browser popup blocker | Allow popups from the Okta domain |
| User not provisioned after assignment | Profile mapping missing | Set Salesforce Profile in assignment dialog; check Provisioning Tasks for errors |
| "My Domain not deployed" error | Domain setup incomplete | Complete Phase 2 before Phase 4 |
| Okta cert expired / wrong cert | Downloaded wrong cert | Re-download from app Sign On tab; use SHA-256 cert |
| SCIM test fails "401 Unauthorized" | OAuth token expired | Re-authenticate in Provisioning > Configure API Integration |

---

## Quick Reference: Key URLs

| Resource | URL Pattern |
|----------|-------------|
| Salesforce Setup Home | `<sf-org>/lightning/setup/SetupOneHome/home` |
| My Domain | `<sf-org>/lightning/setup/OrgDomain/home` |
| SSO Settings | `<sf-org>/lightning/setup/SingleSignOn/home` |
| Manage Users | `<sf-org>/lightning/setup/ManageUsers/home` |
| **App Manager (External Client Apps)** | **`<sf-org>/lightning/setup/AppManager/home`** |
| Connected Apps (classic — avoid for SCIM) | `<sf-org>/lightning/setup/ConnectedApplication/home` |
| Okta App Catalog | `https://<okta-domain>/admin/apps/add-app` |
| Okta App List | `https://<okta-domain>/admin/apps/active` |
| Okta Salesforce Provisioning | `https://<okta-domain>/admin/app/salesforce/instance/<app-id>/#tab-provisioning` |
