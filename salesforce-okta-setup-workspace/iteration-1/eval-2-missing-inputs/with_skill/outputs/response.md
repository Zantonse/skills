# Salesforce + Okta Setup — Missing Inputs

Great use case — Salesforce + Okta for ILM is one of the best demos for showing lifecycle management end-to-end. Before I can start the configuration, I need a few things.

**Do you already have a Salesforce Developer Edition org provisioned?**

If not, sign up for free at: https://developer.salesforce.com/signup
- Use your work email for the admin account
- After email verification, you'll set a password and get an org URL like:
  `https://[orgid]-dev-ed.develop.lightning.force.com`
- Takes about 5–10 minutes including email verification

**Once you have the org, I'll need:**

1. **Salesforce org URL** — the full URL from your browser after logging in
   (e.g., `https://orgfarm-7d8ff5c5c1-dev-ed.develop.lightning.force.com`)

2. **Salesforce admin username** — the email you used to sign up
   (e.g., `yourname@yourcompany.com`)

3. **Okta demo name** — the name of your demo tenant
   (Run `/list_demos` if you're not sure, or provision a new one with `/demo-provision`)

Once you have these, I'll handle both sides of the configuration — adding Salesforce to your Okta tenant as a SAML app with SCIM provisioning enabled, and configuring the Salesforce SSO settings to trust Okta as the identity provider. The full setup takes about 20–30 minutes.
