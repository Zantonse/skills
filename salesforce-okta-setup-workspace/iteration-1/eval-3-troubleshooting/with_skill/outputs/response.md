# Troubleshooting: Users Not Provisioning in Salesforce

## Problem Summary
SAML login is working (you can authenticate to Salesforce via Okta), but users assigned to the Salesforce OIN app in Okta are not appearing in Salesforce or their profiles aren't being set correctly.

This is a **SCIM provisioning issue**, not a SAML issue. The two are independent — SSO works, provisioning doesn't.

---

## Diagnostic Flowchart

### Step 1: Verify SCIM API Integration is Enabled

Go to **Apps > Salesforce > Provisioning tab** (or navigate directly: `https://<okta-domain>/admin/app/salesforce/<app-id>/provisioning/connection`)

Check:
- ✅ **"Enable API Integration"** checkbox is **checked**
- ✅ **"Authenticate with Salesforce.com"** button shows a connected status (green checkmark or "Connected")

**If not connected:**
1. Click **"Authenticate with Salesforce.com"**
2. A browser popup will open — log in with **Salesforce admin credentials** (the same ones you used in Phase 2)
3. Authorize Okta to access Salesforce
4. Return to the Provisioning tab and click **"Test API Credentials"**
5. Should show: "Salesforce.com was verified successfully"

If the OAuth popup is blocked by your browser's popup blocker:
- Allow popups from the Okta domain
- Try again

If OAuth fails with "Invalid credentials" or "Not authorized":
- Verify the Salesforce admin username/password are correct
- The admin account must have API access enabled in Salesforce
- Confirm the Connected App (created by Okta during OAuth) is still valid in Salesforce Setup > Apps > Connected Apps > Manage Connected Apps

---

### Step 2: Check Provisioning Features are Enabled

On the same Provisioning tab, look for the **"To App"** section. Click **Edit** if you haven't already.

Verify these are **checked**:
- ✅ Create Users
- ✅ Update User Attributes
- ✅ Deactivate Users

If any are unchecked, check them and **Save**.

---

### Step 3: Verify Attribute Mappings (Critical)

Go to **Provisioning > Attribute Mappings**

You should see these mappings:

| Okta Attribute | Salesforce Field | Priority |
|---|---|---|
| `user.firstName` | FirstName | Required |
| `user.lastName` | LastName | Required |
| `user.email` | Email | Required |
| `user.login` | Username | Required (must be email format) |
| `user.email` | FederationIdentifier | **Required for SSO** |

**The most common missing mapping:** `FederationIdentifier`

If it's not there:
1. Click **"Add Mapping"** or **"New Mapping"**
2. Set: Okta Attribute = `user.email` | Salesforce Field = `FederationIdentifier` | Priority = Required
3. **Save**

This mapping is **critical for SSO to work** — without it, the user's Okta email won't be linked to their Salesforce federation ID, and SSO login will fail even if provisioning succeeds.

---

### Step 4: Verify User Assignment Has a Profile Set

Go to **Apps > Salesforce > Assignments tab**

Find the test user you assigned. Click on them or click the assignment row.

Check: **What Salesforce Profile is assigned?**

**If no profile is set:**
1. Click **Edit** or **Reassign**
2. Under **Salesforce Profile**, select a profile (usually **System Administrator** for demo purposes)
3. **Save**

**This is required.** Users cannot be provisioned without a profile assigned in Okta.

---

### Step 5: Check Provisioning Tasks for Errors

Back on the **Provisioning tab**, look for a **"Tasks"** or **"Recent Tasks"** section (may say "Provisioning > Tasks").

Click into Tasks and look for the user you just assigned.

**You'll see one of these:**
- ✅ **Success** — user was provisioned to Salesforce (check Salesforce to verify they're there)
- ❌ **Failed** — an error occurred. Click the failed task to see the error message

**Common error messages and fixes:**

| Error | Cause | Fix |
|---|---|---|
| "Profile mapping missing" | No Salesforce Profile assigned in Okta | Go back to Assignments, set a profile for the user |
| "401 Unauthorized" | OAuth token expired or revoked | Re-authenticate: Provisioning > Configure API Integration > "Authenticate with Salesforce.com" |
| "User already exists" | User was manually created in Salesforce with the same username | Delete or rename the Salesforce user and retry the assignment |
| "FederationIdentifier not found in request" | FederationIdentifier attribute mapping missing | Add the mapping: `user.email` → `FederationIdentifier` (Phase 5, Step 3) |
| "Invalid profile name" | The profile name in Okta doesn't exist in Salesforce | Go to Salesforce > Setup > Profiles and verify the exact name, then update the Okta assignment |

---

### Step 6: Manual Retry

If the task failed, fix the underlying issue (steps 1-4), then:
1. Go to **Assignments tab**
2. Click the user assignment
3. Look for a **"Retry"** button or similar option
4. Click it

The provisioning task will run again. Check Tasks to see if it succeeds this time.

---

### Step 7: Verify in Salesforce

Once provisioning shows **Success** in Okta Tasks:

1. Go to **<sf-org-url>/lightning/setup/ManageUsers/home**
2. Search for the user by email or name
3. Click on the user record

Confirm:
- ✅ **First Name** is populated
- ✅ **Last Name** is populated
- ✅ **Email** is correct
- ✅ **Username** is set (usually the email)
- ✅ **Profile** matches what you assigned in Okta
- ✅ **Federation ID** equals the user's Okta email (this is what links SSO)

If any field is blank or wrong, the attribute mapping is likely incorrect or the user's Okta profile is missing that data. Fix in Okta and retry.

---

## Common Root Causes (From Common Issues Table)

| Symptom | Root Cause | Fix |
|---|---|---|
| User not appearing in Salesforce after assignment | Profile mapping missing | Set Salesforce Profile in Okta assignment dialog |
| User appears but fields are blank | Attribute mapping incomplete or wrong | Verify all 5 mappings in Provisioning > Attribute Mappings |
| "SCIM OAuth popup blocked" | Browser popup blocker | Allow popups from Okta domain and retry OAuth |
| "401 Unauthorized" when testing API credentials | OAuth token expired | Re-authenticate: Provisioning > Configure API Integration |
| "FederationIdentifier not found" | FederationIdentifier not mapped | Add `user.email` → `FederationIdentifier` mapping |

---

## Quick Checklist

Run through this before asking for help:

- [ ] SCIM API Integration is enabled and authenticated (green checkmark or "Connected")
- [ ] Provisioning features (Create, Update, Deactivate) are all **checked**
- [ ] All 5 attribute mappings are present, including `FederationIdentifier`
- [ ] User is assigned in Okta with a Salesforce Profile selected
- [ ] Provisioning > Tasks shows **Success** (not Failed or Pending)
- [ ] User appears in Salesforce > Manage Users with all fields populated
- [ ] User's Federation ID in Salesforce matches their Okta email

---

## If Still Not Working

If you've checked all of the above and provisioning is still failing:

1. **Check the exact error in Okta Provisioning > Tasks** — this is the diagnostic gold
2. **Verify OAuth is still valid** — run "Test API Credentials" on the Provisioning tab. If it fails, re-authenticate
3. **Confirm the Salesforce Connected App wasn't revoked** — in Salesforce, go to Setup > Apps > Connected Apps > Manage Connected Apps and look for the Okta app. If it's revoked, you'll need to re-authenticate in Okta
4. **Check Salesforce API limits** — if your org is hitting API rate limits, provisioning will fail silently. Check Salesforce Setup > System Overview for API usage
5. **Reach out with the exact error from Okta Tasks** — that will point to the exact issue

---

## Success Indicators

Once provisioning is working:

✅ User assigned in Okta → appears in Salesforce within 60 seconds
✅ User profile in Salesforce matches what you set in Okta
✅ SSO login works (user can click Okta dashboard tile and land in Salesforce)
✅ Deprovisioning works (remove user from Okta app → user becomes inactive in Salesforce within 1-2 minutes)
