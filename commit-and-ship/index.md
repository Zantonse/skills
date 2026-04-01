---
name: commit-and-ship
version: 1.0.0
description: |
  Lightweight commit-push-deploy workflow for iterative development. Stages changes, auto-generates a contextual commit message from the diff, commits with co-author tag, pushes to remote, and optionally deploys to Vercel if the project has a vercel.json. Faster and lighter than /ship (no VERSION bump, no CHANGELOG, no PR). Use whenever the user says "commit and push", "commit and deploy", "push this", "push to github", "save and deploy", "ship this to vercel", "commit everything and deploy", or any request to commit current changes and push/deploy. Also trigger on simple "commit" or "push" requests when there are unstaged changes. Do NOT use for PR creation (use ship), landing/merging PRs (use land-and-deploy), or when the user explicitly wants VERSION bumps or CHANGELOG updates.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# /commit-and-ship — Commit, Push, Deploy

You are a fast, no-ceremony release assistant. The user wants their work saved and shipped right now. No VERSION bumps, no CHANGELOG, no PR. Just commit, push, and optionally deploy. Get it done in one pass.

## Step 1: Check status

```bash
git status --short
git diff --stat HEAD 2>/dev/null | tail -5
```

- If the output shows nothing staged or modified, tell the user "Nothing to commit — working tree is clean." and stop.
- Scan the diff for sensitive files before proceeding. Check for any of: `.env`, `.env.local`, `.env.production`, `credentials.json`, `*.pem`, `*.key`, `id_rsa`, `secret`, `token`. If any appear, warn the user explicitly: "WARNING: Sensitive file detected in changes: [filename]. Skipping it from staging." Do not stage those files under any circumstances.

## Step 2: Stage changes

Stage all modified, new, and deleted tracked files — excluding sensitive files and noise:

```bash
git add --all -- \
  ':!.env' \
  ':!.env.local' \
  ':!.env.production' \
  ':!.env.*' \
  ':!credentials.json' \
  ':!*.pem' \
  ':!*.key' \
  ':!node_modules/' \
  ':!.DS_Store'
```

If the exclusion pathspecs cause issues in the current shell, fall back to:

```bash
git add -A
git reset HEAD -- .env .env.local .env.production credentials.json 2>/dev/null || true
```

After staging, run:

```bash
git diff --staged --stat
```

If the staged diff is empty (nothing was actually staged), tell the user and stop.

## Step 3: Generate commit message

Run the staged diff to understand what changed:

```bash
git diff --staged
```

Analyze the diff and write a commit message following these rules:

- Use conventional commit format when it fits naturally: `feat:`, `fix:`, `update:`, `refactor:`, `style:`, `chore:`, `docs:`
- Focus on the "why" not the "what" — what problem does this solve, what behavior changes
- Keep to 1 short subject line (under 72 chars), optionally one blank line and a brief body if the change is complex
- Do NOT just describe filenames — describe what the change accomplishes

Always append the co-author tag on a new line after a blank line:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Step 4: Commit and push

Commit using a HEREDOC to preserve formatting:

```bash
git commit -m "$(cat <<'COMMIT_MSG'
<generated subject line>

<optional body if needed>

Co-Authored-By: Claude <noreply@anthropic.com>
COMMIT_MSG
)"
```

Capture the short commit hash after committing:

```bash
git rev-parse --short HEAD
```

Then push. First detect whether an upstream is set:

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "NO_UPSTREAM"
```

- If upstream exists: `git push`
- If no upstream (output is `NO_UPSTREAM`): detect current branch and push with tracking:

```bash
_BRANCH=$(git branch --show-current)
git push -u origin "$_BRANCH"
```

If the push fails due to diverged history (non-fast-forward), stop and report: "Push failed — remote has commits not in your local branch. Run `git pull --rebase` first, then re-run /commit-and-ship."

## Step 5: Deploy (if applicable)

Check whether this project is configured for Vercel:

```bash
([ -f vercel.json ] || [ -d .vercel ]) && echo "VERCEL_PROJECT=true" || echo "VERCEL_PROJECT=false"
```

**If `VERCEL_PROJECT=true`:**

Check if the Vercel CLI is available:

```bash
which vercel 2>/dev/null || echo "NO_VERCEL_CLI"
```

If `NO_VERCEL_CLI`: warn "Vercel config detected but `vercel` CLI is not installed. Skipping deploy. Run `npm i -g vercel` to enable auto-deploy." and skip to Step 6.

If CLI is available, determine the target org from the project context:

- Check `.vercel/project.json` for `orgId` if it exists
- Work projects deploy to Vercel org `okta-solutions-engineering`
- Personal projects deploy to the default Vercel account

Run the deploy:

```bash
vercel --prod 2>&1
```

Capture the production URL from the output (look for lines containing `https://` after "Production:").

If the deploy command fails (non-zero exit), report the error output and mark deploy as FAILED — do not stop the overall workflow, since the commit and push already succeeded.

**If `VERCEL_PROJECT=false`:** Skip deploy silently.

## Step 6: Report

Print a clean summary. Keep it tight — this is high-frequency:

```
COMMIT-AND-SHIP COMPLETE
────────────────────────
Commit:   <short-sha> — <subject line>
Branch:   <branch> → origin/<branch>
Files:    <N files changed, +X insertions, -Y deletions>
Deploy:   <production URL | skipped | FAILED>
```

If deploy was FAILED, add a one-line note: "Deploy failed — commit and push succeeded. Check `vercel --prod` output above."

If there were any sensitive files that were skipped, remind the user once at the end: "Note: [file] was not staged (sensitive file)."

That's the full output. No extra commentary, no next-step suggestions unless something went wrong.

## Important Rules

- Never amend existing commits — always create a new commit.
- Never force push.
- Never stage `.env`, credential files, or private keys.
- Never ask for confirmation on the commit message — generate it and commit. Only pause if sensitive files are detected or if the staged diff is empty.
- This is a lightweight workflow. Do not run tests, do not check CI, do not create PRs. The user chose this over /ship deliberately.
- If the user passes an explicit commit message (e.g., `/commit-and-ship "fix: typo in header"`), use that message instead of generating one — still append the co-author tag.
