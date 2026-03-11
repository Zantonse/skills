---
name: organize-vault
description: >
  Organize an Obsidian vault by sorting loose notes into a clean folder taxonomy.
  Use this skill whenever the user asks to organize, sort, tidy, clean up, or
  restructure their Obsidian notes or vault — even if they just say something like
  "my vault is a mess" or "organize my notes." Also trigger when the user asks to
  "file away" notes, "categorize" notes, or mentions loose/unfiled notes in Obsidian.
  This skill handles the full workflow: audit the vault, design a folder structure
  based on content themes, move all files, and report what changed.
---

# Organize Obsidian Vault

Sort loose Obsidian notes into a logical folder taxonomy based on filenames, existing folder structure, and frontmatter tags. Execute autonomously and report a summary when done.

## Why This Approach Works

Obsidian vaults accumulate loose notes over time — research output, meeting notes, project artifacts — that end up in a flat pile. Organizing by filename patterns and existing folder context is fast and accurate because note filenames almost always encode their topic (e.g., `OAuth-2.1-Core-Specification.md` clearly belongs in an identity/protocols folder). Reading full note content is unnecessary in most cases and dramatically slower for large vaults.

## Workflow

### Phase 1: Audit

1. **Get vault stats** — call `get_vault_stats` with `recentCount: 20` to understand scale (total notes, folders, size, recent activity).

2. **Map the full structure** — call `list_directory` on the root `/`, then recursively on every subdirectory. Build a complete mental model of:
   - Which folders already exist and are well-organized (leave these alone)
   - Which folders are dumping grounds with mixed content
   - Which loose files exist at the root or in top-level directories
   - Which folders overlap in purpose and should be merged

3. **Identify the problem files** — the primary targets are:
   - Loose notes sitting directly in the root or in a catch-all folder
   - Files in folders that don't match their content (based on filename)
   - Near-duplicate folders that should be consolidated (e.g., `stocks/` and `investments/`)

### Phase 2: Design Taxonomy

Design a folder structure by clustering filenames into natural groups. Follow these principles:

- **Preserve what works.** If a folder is already well-organized (e.g., `competitive-intel/` with 9 competitor profiles), leave it alone. Don't reorganize for the sake of reorganizing.
- **Group by domain, not format.** A folder called `pdfs/` is useless. Group by what the notes are *about* — `identity-protocols/`, `career/`, `personal/`, `accounts/`.
- **Use lowercase-kebab-case** for new folder names. Keep naming consistent with any existing convention in the vault.
- **Aim for 5-15 files per folder.** A folder with 1 file is premature; a folder with 50 is too broad. Split or merge accordingly.
- **Absorb redundant folders.** If `stocks/` has 1 file and `investments/` has 14, merge `stocks/` into `investments/`. If `Design/` and `design/` both exist, consolidate.
- **Nest sparingly.** One level of subfolder is fine (e.g., `accounts/Robinhood/`). Two levels deep should be rare. Deep nesting makes notes hard to find.
- **Respect existing substructure.** If a folder like `oig-strategic-insights/` has numbered files (`00-executive-summary.md` through `09-strategic-recommendations.md`), it's intentionally ordered — keep it intact.

### Phase 3: Execute Moves

Move files using `move_note`. Key execution patterns:

- **Batch by destination** — move all files destined for the same folder in a single parallel call. This is faster and makes it easy to verify each batch.
- **Move 8-10 files per batch** — this is the practical limit for parallel MCP calls.
- **Handle conflicts** — if `move_note` fails because the target exists, use `overwrite: true` only if you're certain the source and target are the same file (e.g., consolidating `Design/` into `design/`). Otherwise, rename the incoming file.
- **Don't move dotfiles** (`.DS_Store`, `.obsidian/`). These are system files.
- **Don't move canvas files** unless explicitly asked. They may have position-dependent references.

### Phase 4: Verify and Report

1. **Verify** — call `list_directory` on `Claude-Research/` (or wherever the main content lives) and confirm zero loose files remain at the top level.

2. **Report** — present a clean summary showing:
   - The final folder tree with file counts
   - What was moved where (grouped by action type: "sorted loose files", "merged folders", "moved root files")
   - Any empty folders left behind (Obsidian auto-cleans these on restart)

## Categorization Heuristics

When a filename doesn't obviously belong to one folder, use these signals in priority order:

1. **Filename prefix/keywords** — `OIG-*` → oig folder, `Okta-*` → okta-platform, crypto ticker symbols → crypto
2. **Date-stamped research** — files like `topic-2026-03.md` are research artifacts; group by topic, not by date
3. **Frontmatter tags** — if present, read with `get_frontmatter` to disambiguate (e.g., `tags: [oauth, identity]` → identity-protocols)
4. **Existing folder neighbors** — if 3 similar files are already in a folder and a 4th is loose, it goes with its siblings
5. **Ask the user** — if a file genuinely could go in two places and the signals are ambiguous, pick the more specific folder rather than a general one. Only ask the user if you truly can't decide.

## Edge Cases

- **Vault with no existing folders**: Design the taxonomy from scratch using filename clustering. Start with broad categories and split if any folder would exceed ~20 files.
- **Vault with great existing structure**: If the audit shows few or no loose files, say so. Don't reorganize for the sake of it.
- **Non-markdown files**: Images, PDFs, and attachments should stay near the notes that reference them. Use `move_file` (not `move_note`) for binary files if needed, but generally leave attachments alone.
- **Wiki-links**: Moving notes may break `[[wiki-links]]`. Obsidian's "Automatically update internal links" setting handles this if enabled. Mention this to the user if the vault has many cross-references.
