# Salesforce + Okta Demo Setup: Missing Inputs Assessment

## Current State
You're at a critical blocker: **both the Okta tenant AND the Salesforce org lack configuration details**. This means you cannot proceed to integration until you gather baseline information.

---

## Critical Missing Inputs

### Okta Tenant
1. **Okta org URL** (e.g., `dev-123456.okta.com`)
   - Used for SAML ACS URL, API calls, and integration config
   - If you don't have this, you need to identify which demo tenant to use
2. **Okta admin credentials** (org admin account)
   - Required to configure SAML, provisioning rules, and test users
3. **Demo user strategy**
   - How many test users? (typically 3-5 for a demo)
   - Will they sync FROM Okta → Salesforce, or test manual creation?
4. **Provisioning direction**
   - **Push provisioning**: Okta creates/updates users in Salesforce (most common for ILM demo)
   - **Pull provisioning**: Salesforce users sync back to Okta
   - **SSO only**: No provisioning, just federated login

### Salesforce Org
1. **Salesforce instance/org** (e.g., `dev-123.salesforce.com`)
   - Is this a sandbox, dev org, or production org?
   - Does it already exist, or do you need to spin one up?
2. **Salesforce admin account**
   - Must have System Administrator role to configure SAML and API permissions
   - If you don't have access, this is a blocker
3. **License availability**
   - Salesforce licenses available for demo users?
   - Check org capacity before creating test accounts
4. **SAML configuration readiness**
   - Does the Salesforce org allow SAML? (most do, but check permission sets)
   - Any existing SSO integrations that might conflict?

### Integration-Specific
1. **SAML certificate**
   - Will you use Okta's built-in certificate or upload custom?
   - (Okta's built-in is fine for demo; custom is overkill)
2. **App assignment**
   - Which Okta users/groups get access to Salesforce?
   - Demo users should be in a dedicated "Demo" group
3. **Attribute mappings**
   - How do Okta user attributes (first name, last name, email) map to Salesforce fields?
   - Email is critical — mismatches break provisioning
4. **Provisioning rules**
   - Should all assigned users be provisioned, or only specific groups?
   - What happens when a user is unassigned? (suspend, deactivate, or leave as-is?)

---

## What You Can't Do Yet

- **Create the Salesforce integration in Okta** — no org URL to point to
- **Configure SAML in Salesforce** — no Okta org URL or metadata
- **Test provisioning** — no test users to assign
- **Show a live login** — can't verify the flow without both sides configured

---

## Recommended Next Steps

### Phase 1: Inventory What You Have (15 min)
1. Confirm your Okta org URL and that you have admin access
2. Confirm Salesforce org exists (or spin up a sandbox)
3. Confirm you have Salesforce admin access
4. Check Salesforce license capacity for test users

### Phase 2: Decide Demo Scope (5 min)
- **Option A (Full ILM demo)**: SSO + push provisioning + deprovisioning
  - Shows Okta creating Salesforce users, updating attributes, and removing access on departure
  - Most impressive for ILM use case
  - **Time to demo**: 30–45 min setup + 10 min live demo
  
- **Option B (SSO-only)**: Federated login without provisioning
  - Faster setup (~15 min)
  - Less impressive but still shows the identity integration
  - **Time to demo**: 15 min setup + 5 min live demo

- **Option C (Provisioning-only)**: Create users in Salesforce without SSO
  - Shows ILM without federated auth
  - Rarely the ask, but valid if SSO is out of scope
  - **Time to demo**: 20 min setup + 5 min demo

### Phase 3: Gather Configuration Details
Once you've decided the scope, collect:
- Okta org URL + admin email
- Salesforce instance URL + admin email
- Demo user count and naming convention
- Which Okta groups should have Salesforce access
- Email domain for test users (e.g., `testuser@acmecorp.com`)

---

## Why This Matters for Your Demo

**The customer sees the value through concrete examples:**
- "Here's how Okta assigns you to Salesforce when you join our company"
- "Here's your SSO experience — one Okta login, instant Salesforce access"
- "When you leave, Okta removes you from Salesforce automatically"

**Each of these requires:**
- Test users with real Okta assignments
- A real Salesforce org configured to trust Okta
- Pre-tested provisioning rules that actually work

If either system is unconfigured, the demo collapses to slides and screenshots, which kills credibility.

---

## One-Line Ask for Craig

**Before setting this up: What's your preferred demo scope (SSO+provisioning, SSO-only, or provisioning-only), and which Okta org/Salesforce sandbox do you want to use?**

Once you answer that, the setup path is clear.
