# Salesforce SCIM Provisioning Troubleshooting

## Problem Summary
SAML authentication works, but users aren't being provisioned when assigned to the Salesforce OIN app in Okta. This is a classic SCIM configuration issue — the identity federation piece (SAML) is separate from the provisioning piece (SCIM), and both must be configured independently.

---

## Diagnostic Checklist

### 1. Verify SCIM is Enabled in the App Integration
**In Okta Admin Console:**
1. Go to **Applications** > **Applications** > Find your Salesforce app
2. Click the app
3. Go to the **Provisioning** tab
4. Check that **Provisioning to App** is **Enabled**
5. If it's grayed out or missing, SCIM provisioning is not active for this app

**What this means:** Even with a working SAML integration, SCIM provisioning must be explicitly enabled. They're two different connections.

---

### 2. Check Salesforce SCIM Endpoint & Auth Token

**In Okta:**
1. **Provisioning** tab → **Integration** section
2. Verify the **SCIM Base URL** is populated (should be: `https://<your-salesforce-instance>.salesforce.com/services/scim/v2`)
3. Verify the **API Token** is set

**In Salesforce:**
1. Log in as Admin → **Setup** → **Users** > **Connected Apps & OAuth Tokens**
2. Search for the Okta SCIM integration
3. If it's not there or has no token, the integration was not completed properly
4. Alternatively, go to **Setup** → **Security** > **Named Credentials** and look for the Okta integration

**Common issue:** The Salesforce instance URL doesn't match. If your Salesforce org is `acme.my.salesforce.com` but the token is for `acme.salesforce.com`, provisioning will fail silently.

---

### 3. Check User Assignment & Profile Mapping

**In Okta:**
1. Go to **Applications** > **Applications** > Your Salesforce app
2. Click **Assignments** tab
3. Verify users/groups are actually assigned to the app (they should show in the list)
4. If no users are assigned, provisioning can't trigger

**Then check Profile Mapping:**
1. Go to **Provisioning** tab → **To App** section
2. Click **Edit** next to Salesforce attribute mapping
3. Verify at least these attributes are mapped:
   - `user.firstName` → First Name
   - `user.lastName` → Last Name
   - `user.email` → Email (or Username if different in your Salesforce)
   - `user.login` → Username (if applicable)

**Common issue:** Missing email mapping. Salesforce requires a unique identifier (usually email or custom username). If the mapping is incomplete, users silently fail to create.

---

### 4. Check SCIM Provisioning Actions

**In Okta:**
1. **Provisioning** tab → **To App** section
2. Verify these are **enabled**:
   - **Create Users** ✓
   - **Update User Attributes** ✓
   - **Deactivate Users** ✓ (or keep disabled if you prefer manual offboarding)

If "Create Users" is **disabled**, new user assignments won't trigger provisioning.

---

### 5. Review Provisioning Logs

**In Okta:**
1. Go to **System Log** (top right corner search)
2. Filter by:
   - Event: `app.user_app_assign` (assignment action)
   - Event: `app.provisioning.provision_user` (provisioning attempt)
   - Source: Your Salesforce app name
3. Look for recent events in the last 1-2 hours (check the time your test happened)

**What to look for:**
- **Success (202 response):** User was created
- **400/401 error:** Token is invalid or expired — regenerate in Salesforce
- **400 Bad Request:** Attribute mapping error — missing required field
- **409 Conflict:** User already exists in Salesforce with that email/username
- **403 Forbidden:** Token doesn't have permission to create users in Salesforce

---

### 6. Test with System Log

**Manual trigger method (if log shows no activity):**
1. Go to **Applications** > Your Salesforce app
2. Click **Assignments** tab
3. Find a test user → Click the **three dots** menu
4. Select **Deprovision** (if already assigned)
5. Wait 10 seconds
6. Click the **three dots** again → **Edit Assignment**
7. Click **Save** → This should trigger a fresh provisioning attempt
8. Check System Log again immediately

This forces a provisioning event and helps you see real-time errors.

---

## Most Common Causes (Ranked)

1. **SCIM Provisioning Not Enabled** — Check Provisioning tab, confirm "Provisioning to App" is ON
2. **Missing or Expired API Token** — Regenerate the token in Salesforce and update in Okta
3. **Incomplete User Assignment** — No users actually assigned to the app in Okta
4. **Wrong Salesforce Instance URL** — SCIM endpoint doesn't match your Salesforce org
5. **Attribute Mapping Missing Email** — Salesforce can't identify the user without email or username
6. **Create Users Action Disabled** — Confirm it's enabled in the Provisioning > To App section
7. **SCIM Base URL Malformed** — Should be `https://<instance>.salesforce.com/services/scim/v2` (no trailing slash, correct endpoint)

---

## Quick Fix Steps (In Order)

1. **Open the Salesforce OIN app in Okta** → Go to **Provisioning** tab
2. **Confirm "Provisioning to App" is Enabled** (not grayed out)
3. **Check the SCIM Base URL** is correct (ask yourself: "Is this my actual Salesforce instance?")
4. **Verify the API Token exists** and is not blank
5. **Go to Assignments** and assign at least one test user
6. **Trigger a re-sync:** De-assign the user, wait 5 seconds, re-assign them
7. **Check System Log** for the provisioning event — look for error messages
8. **If still failing:** Log into Salesforce as Admin and check if the Okta SCIM app/token exists in **Connected Apps**

---

## After You Fix It

- Monitor the **System Log** for 24 hours to ensure consistent provisioning
- Test user **deprovisioning** (assign, then unassign) to confirm the reverse flow works
- Verify user **attribute updates** (change a user's first name in Okta, wait 5 min, confirm it updates in Salesforce)

---

## If You're Still Stuck

- **Check the Salesforce sandbox** — Are you testing against a sandbox or production org? Sandboxes require their own SCIM setup
- **Confirm permission:** The Salesforce user/token must have "Manage Connected Apps" and "Manage Profiles and Permission Sets" permissions
- **Verify Okta has network access to Salesforce** — Check if there's a firewall or IP allowlist blocking SCIM calls (unlikely, but possible in locked-down environments)
- **Escalate to Salesforce Support:** If the SCIM endpoint is unreachable or the token is valid but rejected, there may be an org-level setting in Salesforce blocking it

---

## Key Takeaway

SAML (login) and SCIM (provisioning) are completely separate integrations. Getting login working doesn't automatically enable provisioning — you have to configure SCIM explicitly and verify the token, endpoint, and mappings are correct. Start with the System Log — it will show you exactly where the provisioning attempt failed.
