---
name: save-obsidian
description: Save content to Obsidian with proper naming and retry logic
---

# Save to Obsidian

When invoked, save the specified content to the Obsidian vault with a unique filename and retry on failure.

## Filename Format

Generate the filename using this pattern:
`{AccountOrTopic}_{YYYY-MM-DD}_{ContentType}_{ShortHash}.md`

- `AccountOrTopic`: customer account name or topic slug (lowercase, hyphens for spaces)
- `YYYY-MM-DD`: today's date
- `ContentType`: one of `notes`, `brief`, `summary`, `transcript`, `qa`, `email`, `action-items`
- `ShortHash`: 4-character hex string derived from the content (take first 4 chars of the MD5 of the first 100 chars of content, or generate a random 4-char hex if hashing is unavailable)

Example: `samsara_2026-05-05_discovery-notes_a3f1.md`

## Write Location

Target vault path: `~/Documents/ObsidianNotes/Claude-Research/accounts/`

Always include YAML frontmatter:
```yaml
---
date: YYYY-MM-DD
account: [account or topic name]
tags: [accounts, relevant-tags]
source: claude-code
---
```

## Write Procedure

1. Construct the full file path: `~/Documents/ObsidianNotes/Claude-Research/accounts/{filename}`
2. Attempt the write using the Obsidian MCP tool (or Write tool if MCP unavailable)
3. If the write succeeds, confirm the save location to the user
4. If the write fails with a 403 or permission error:
   - Wait 3 seconds
   - Retry the write exactly once
5. If the retry also fails:
   - Save the file locally to `./obsidian-queue/{filename}` instead
   - Inform the user: "Obsidian write failed twice. Saved locally to `./obsidian-queue/{filename}` — move it to Obsidian manually when the vault is accessible."
6. Always end by telling the user the final save location (Obsidian path or local fallback path)
