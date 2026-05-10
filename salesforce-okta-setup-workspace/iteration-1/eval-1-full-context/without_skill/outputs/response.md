# Salesforce SSO + SCIM Setup for Deel OIG POC — Okta Configuration Guide

## Overview

This guide walks through setting up Salesforce single sign-on (SSO) and System for Cross-domain Identity Management (SCIM) provisioning with Okta for the Deel OIG POC demo.

**Environment Details:**
- Salesforce org: `orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com`
- Okta admin: `craig.verzosa+deeloig@okta.com`
- Okta demo environment: `deel-oig-poc`
- Setup method: SAML 2.0 for SSO, SCIM 2.0 for user/group provisioning

---

## Part 1: Salesforce Configuration — Generate SAML Metadata

### Step 1a: Enable SAML in Salesforce

1. Log in to Salesforce as admin (`craig.verzosa+deeloig@okta.com`)
2. Navigate to **Setup** (gear icon, top right)
3. Search: `Single Sign-On Settings`
4. Go to **Security** → **Single Sign-On Settings**
5. Click **Edit** and check: **SAML Enabled** ✓
6. Click **Save**

### Step 1b: Create SAML Configuration

1. In Setup, search: `SAML Single Sign-On Settings`
2. Click **New** to create a new SAML SSO configuration
3. Fill in the form:
   - **Name:** `Okta` (or `Deel OIG POC`)
   - **API Version:** `61.0` (latest for your org)
   - **Entity ID:** Accept default or use: `https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com`
   
4. **Identity Provider Certificate:** Leave blank for now — you'll paste Okta's certificate in the next step
5. Click **Save** — Salesforce generates a certificate and keypair

### Step 1c: Download Salesforce Metadata

1. After save, re-enter the SAML config you just created
2. Click **Download Metadata** — this saves an XML file locally
3. **Keep this file** — you'll upload it to Okta in Part 2

**What to note from the metadata file:**
- `entityID` (Salesforce's identifier)
- `AssertionConsumerServiceURL` (where Okta will send SAML responses)
- `SingleLogoutServiceURL` (optional, for logout)

---

## Part 2: Okta Configuration — Add Salesforce App

### Step 2a: Add Salesforce Application

1. Log in to your Okta demo org (`deel-oig-poc`)
2. Navigate to **Applications** → **Applications** (or **Catalog**)
3. Search: `Salesforce`
4. Select the **Salesforce** app (by Okta)
5. Click **Add / Integrate this app**

### Step 2b: Configure SAML Settings

1. Choose configuration mode: **SAML 2.0** (default)
2. Click **Next** to enter SAML settings

3. **Identity Provider Details** — Okta auto-fills these:
   - Single Sign-On URL: `https://deel-oig-poc.okta.com/app/amazon_aws/exk...` (Okta's SAML endpoint)
   - Audience URI: `https://saml.salesforce.com` (Salesforce expects this)
   
4. **Attribute Mappings** (critical for SSO):
   - Okta's `user.email` → Salesforce's `email`
   - Okta's `user.firstName` → Salesforce's `firstName`
   - Okta's `user.lastName` → Salesforce's `lastName`
   - (Okta pre-populates these; verify they're correct)

5. **Application Settings:**
   - Username: `${user.email}` (Salesforce will use email as username)
   - Leave other fields as default

6. Click **Next**

### Step 2c: Choose App Launch Type

- Select: **I'm an Okta customer adding an internal app** (since this is a demo/POC)
- Click **Finish**

### Step 2d: Upload Salesforce's SAML Metadata (Alternative Path)

If the above doesn't work, use the manual metadata upload path:

1. In the Salesforce app settings, click **SAML 2.0 Configuration**
2. Look for **Upload metadata** or **Edit SAML configuration**
3. Upload the XML file you downloaded from Salesforce in Step 1c
4. Okta auto-populates the SAML endpoints from the metadata

---

## Part 3: Salesforce Configuration — Add Okta Metadata

### Step 3a: Return to Salesforce Setup

1. Log back into Salesforce
2. Go to **Setup** → **Security** → **SAML Single Sign-On Settings**
3. Click on the `Okta` configuration you created in Step 1b

### Step 3b: Enter Okta's SAML Details

You need Okta's SAML metadata. In Okta:

1. Go to **Applications** → **Salesforce** (the app you just added)
2. Click the **Sign On** tab
3. Scroll down to **SAML Signing Certificates**
4. Click on the **active certificate** link
5. A new window opens showing the certificate details. Note the **Issuer URL** (e.g., `https://deel-oig-poc.okta.com`)
6. Find the SAML metadata URL: `https://deel-oig-poc.okta.com/app/abc123/exk456/sso/saml/metadata`

Back in Salesforce SAML config:

1. Find **Identity Provider Certificate** field
2. Download Okta's certificate from the Okta cert detail page (or copy the public cert text)
3. Paste it into Salesforce's **Identity Provider Certificate** field

4. Fill in **Identity Provider Single Sign-On URL:**
   - From Okta's SAML config: `https://deel-oig-poc.okta.com/app/abc123/exk456/sso/saml` (without `/metadata`)

5. (Optional) **Identity Provider Single Logout URL:**
   - `https://deel-oig-poc.okta.com/app/abc123/exk456/sso/saml` (same endpoint)

6. Click **Save**

---

## Part 4: Test SAML SSO

### Step 4a: Assign Users in Okta

1. In Okta, go to the **Salesforce** app
2. Click **Assignments**
3. Click **Assign** → **Assign to People**
4. Search for users to assign (e.g., your test users)
5. For each user, set:
   - **Email:** Must match Salesforce username (typically email)
   - **First Name:** User's first name
   - **Last Name:** User's last name
6. Click **Save and Go Back**
7. Click **Done**

### Step 4b: Test Login

1. In Okta, click the **Salesforce** app icon (from the app dashboard)
2. Okta initiates a SAML flow and redirects to Salesforce
3. You should land in Salesforce **without** being prompted for a password
4. If it works: SSO is configured ✓

### Step 4c: Troubleshooting SSO

- **Assertion Consumer Service URL mismatch:** Verify Salesforce's ACS URL matches the one in Okta config
- **Email not found:** Ensure the Okta user's email attribute matches an existing Salesforce username
- **Blank screen or redirect loop:** Check browser console for SAML errors; download Okta's assertion XML from the Okta logs

---

## Part 5: SCIM Provisioning — Enable in Okta

### Step 5a: Enable SCIM in the Salesforce App

1. In Okta, go to **Applications** → **Salesforce**
2. Click the **Provisioning** tab
3. Click **Configure API Integration**
4. Check: **Enable API integration** ✓
5. Okta needs Salesforce SCIM endpoint details:
   - **SCIM Base URL:** `https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com/services/scim/v2`
   - **API Token:** See Step 5b below

6. Click **Test API Credentials** (after you add the token)
7. Click **Save**

### Step 5b: Generate Salesforce OAuth Token for SCIM

1. Log into Salesforce as admin
2. Go to **Setup** → **Apps** → **App Manager**
3. Click **New Connected App**
4. Fill in:
   - **Connected App Name:** `Okta SCIM`
   - **API Name:** `Okta_SCIM` (auto-populated)
   - **Contact Email:** Your email
   - **Enable OAuth Settings:** Check ✓
   - **Callback URL:** `https://deel-oig-poc.okta.com/oauth2/v1/authorize/callback`
   - **Selected OAuth Scopes:** Add `full` and `refresh_token, offline_access`
5. Click **Save**

6. A **Consumer Key** and **Consumer Secret** are generated. Note these.

7. Go to **Setup** → **Users** → **Users**
8. Click on your admin user
9. Click **Generate Token** (or find in authentication settings)
10. Copy the OAuth **access token** (valid for 24 hours) — this is your SCIM API Token

### Step 5c: Enter SCIM Credentials in Okta

Back in Okta's Salesforce app **Provisioning** tab:

1. **SCIM Base URL:** `https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com/services/scim/v2`
2. **API Token:** Paste the Salesforce OAuth token from Step 5b
3. Click **Test API Credentials** → Should show "Success"
4. Click **Save**

### Step 5d: Configure Provisioning Rules

1. Still in **Provisioning** tab, go to **To App** section
2. Enable:
   - **Create Users** ✓
   - **Update User Attributes** ✓
   - **Deactivate Users** ✓ (optional, for offboarding)
3. Click **Save**

### Step 5e: Map Okta Attributes to Salesforce

1. In the **Provisioning** tab, find **Attribute Mappings**
2. Verify the following mappings exist:
   - Okta `user.email` → Salesforce `email` (username)
   - Okta `user.firstName` → Salesforce `firstName`
   - Okta `user.lastName` → Salesforce `lastName`
   - Okta `user.login` → Salesforce `userName`
3. Add custom mappings if needed for your POC (e.g., department, phone)
4. Click **Save**

---

## Part 6: Test SCIM Provisioning

### Step 6a: Assign New User in Okta

1. In Okta, go to **Salesforce** app → **Assignments**
2. Click **Assign** → **Assign to People** → **Assign** (or select an unassigned test user)
3. Fill in the provisioning profile (email, first name, last name)
4. Click **Save and Go Back**

### Step 6b: Monitor Provisioning

1. Go to **Provisioning** → **To App** section
2. Watch the **Push Status** field — should show "Sent" or "Success"
3. Check Okta logs: **Reports** → **System Log** (search for the user's provisioning event)

### Step 6c: Verify in Salesforce

1. Log into Salesforce as admin
2. Go to **Setup** → **Users** → **Users**
3. Search for the newly created user (by email)
4. Confirm the user exists with correct first/last name
5. SCIM provisioning is working ✓

---

## Part 7: OIG Integration (Identity Governance)

For the Deel OIG POC, integrate Salesforce into the identity governance workflow:

### Step 7a: Import Salesforce Users into OIG

1. In Okta, go to **Identity Governance** (or **OIG**)
2. Click **Resources** or **Connected Systems**
3. Add **Salesforce** as a resource
4. Point to the same SCIM endpoint + OAuth token
5. Click **Sync** to import Salesforce users as a resource in OIG

### Step 7b: Create Access Certification Campaign

1. In OIG, go to **Access Certifications** → **Create Campaign**
2. Select **Salesforce** as the resource
3. Choose certifiers (IT admins, managers)
4. Set campaign review period (e.g., 2 weeks)
5. Click **Launch Campaign**
6. OIG will surface all Salesforce app assignments for review and recertification

### Step 7c: Automate Remediation

1. In OIG, set up **Remediation Rules**:
   - When a user is not recertified: Remove Salesforce license
   - When a user is removed from Okta: Deactivate in Salesforce (via SCIM)
2. Map these to your Deel organizational policies

---

## Troubleshooting Checklist

| Issue | Solution |
|-------|----------|
| **SSO fails: Assertion Consumer Service URL mismatch** | Verify `AssertionConsumerServiceURL` from Salesforce metadata matches Okta's app config |
| **SSO works but user lands on Salesforce setup page** | User doesn't have permission in Salesforce. Assign profile/permission sets in Salesforce. |
| **SCIM fails: Invalid credentials** | Salesforce token expired (24-hour lifetime). Generate new OAuth token. |
| **SCIM works but attributes don't sync** | Check attribute mappings in Okta's provisioning config. Ensure Salesforce field names are correct. |
| **Blank screen after clicking Salesforce app in Okta** | Check browser console for SAML/CORS errors. Verify Okta's SAML endpoint is accessible. |
| **Users created but can't log in** | Ensure username (email) format matches Salesforce's expectation. Assign permission sets/profiles in Salesforce. |
| **OIG not showing Salesforce resource** | Confirm SCIM connection is healthy in OIG's resource settings. Re-sync if needed. |

---

## Configuration Verification Checklist

- [ ] Salesforce SAML enabled in Setup
- [ ] Salesforce SAML config created with Okta cert and endpoint
- [ ] Okta Salesforce app added and SAML configured
- [ ] Attribute mappings verified (email, firstName, lastName)
- [ ] SSO test successful (click Salesforce app → lands in Salesforce, no password prompt)
- [ ] Salesforce OAuth token generated for SCIM
- [ ] Okta SCIM integration enabled with correct SCIM base URL and API token
- [ ] SCIM provisioning attributes mapped
- [ ] Test user provisioned from Okta to Salesforce
- [ ] OIG connected to Salesforce resource
- [ ] OIG certification campaign created with Salesforce

---

## Demo Script (OIG POC)

For the demo, walk through:

1. **SSO Flow:** Log in via Okta, click Salesforce app, appear in Salesforce (no re-auth)
2. **SCIM Provisioning:** Create a new user in Okta, show the auto-created Salesforce user
3. **OIG Certification:** Show OIG access certification for Salesforce roles, recertify, auto-remediate
4. **Compliance Outcome:** "Now you have auditable, certified access to Salesforce across your organization"

---

## Notes for Deel POC

- Use Deel employee personas in the Okta users to simulate real provisioning
- Set up a test group in Okta (e.g., "Deel Finance") and assign the Salesforce app to the group
- Test deprovisioning: remove a user from Okta, confirm they're deactivated in Salesforce
- Capture screenshots of OIG certification results for the follow-up business case
