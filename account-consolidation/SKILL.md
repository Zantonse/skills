---
name: account-consolidation
description: >
  Audit and consolidate a multi-page account dashboard to reduce page count, eliminate data
  duplication, and simplify navigation. Use when the user asks to: (1) consolidate, condense,
  or reduce pages in an account dashboard, (2) deduplicate data across data files, (3) merge
  overlapping pages into one, (4) combine related pages into tabs, (5) create shared constants
  from repeated values, (6) derive computed values instead of hardcoding, or (7) audit a
  dashboard for redundancy. Triggers on: 'consolidate', 'condense', 'reduce pages', 'merge
  pages', 'deduplicate', 'too many pages', 'simplify dashboard', 'combine into tabs'.
---

# Account Dashboard Consolidation

Systematic workflow to audit a multi-page dashboard for redundancy and consolidate it through
data deduplication, page merging, and navigation simplification.

## Workflow

```
Audit → Plan → Batch A (data) → Batch B (pages) → Batch C (tabs) → Batch D (wiring) → Verify
```

### Phase 1: Audit

1. Map every page, section component, and data file
2. Identify duplicates by category:
   - **Duplicate scalars** — same literal value in 2+ data files
   - **Duplicate objects** — same structured data in 2+ files
   - **Redundant arrays** — array that is a subset of another
   - **Thematic overlaps** — pages covering 60%+ of the same domain
   - **Derivable values** — hardcoded values computable from existing data
3. Count pages, sections, lines, and data files for a before/after comparison
4. Present findings as a consolidation plan with numbered strategies

### Phase 2: Plan Batches

Group strategies into dependency-ordered batches:

| Batch | Scope | Depends on |
|-------|-------|-----------|
| **A — Data Foundation** | Shared constants, derived values, object deduplication | Nothing |
| **B — Page Merges** | Absorb overlapping pages into surviving pages | Batch A |
| **C — Tab Combinations** | Combine same-domain pages behind tab navigation | Nothing |
| **D — Data Wiring** | Replace inline arrays with imports from canonical sources | Batch B |

### Phase 3: Execute Batches

#### Batch A — Data Foundation (no UI changes)

1. Create `constants.ts` (or equivalent) with shared scalars
2. Update consuming data files to import from constants
3. Replace hardcoded values with computed expressions
4. Deduplicate data objects (import from canonical source)
5. **Check:** circular dependency audit before each new import
6. **Verify:** `tsc --noEmit` (or equivalent type/lint check)

#### Batch B — Page Merges

For each merge (absorbed page → surviving page):

1. Read both section components fully
2. Extract inline data arrays into data files
3. Add unique sections to the surviving component
4. Update surviving component's imports
5. Delete absorbed component and route directory
6. Update sidebar and home page navigation
7. **Verify:** `tsc --noEmit`

#### Batch C — Tab Combinations

For each tab group:

1. Create a `'use client'` tabbed wrapper component
2. Import existing section components (do not merge them)
3. Conditionally render sections behind tabs
4. Update the surviving route to use the tabbed wrapper
5. Delete absorbed route directories
6. Update sidebar (single link) and home page (single card)
7. **Verify:** `tsc --noEmit`

#### Batch D — Data Wiring

1. Replace remaining inline data arrays with imports from canonical data files
2. Adjust rendering code if field shapes differ
3. **Verify:** `tsc --noEmit`

### Phase 4: Final Verification

1. Clear build cache (`rm -rf .next` or equivalent)
2. Run full build
3. Confirm route table matches expected page count
4. Deploy if applicable

## Key Principles

- **Read before modifying.** Never propose changes to code that hasn't been read.
- **Check circular deps.** Before adding `import { X } from './foo'` to `bar.ts`, verify `foo.ts` doesn't import from `bar.ts`.
- **Preserve component shape.** When deduplicating objects, the consuming code's expected shape must not change. Destructure or map if needed.
- **Composition over merging.** For tab combinations, wrap existing components — don't merge them into one monolith.
- **Update both nav sources.** Sidebar config and home page card config are manually synced. Always update both after page changes.
- **Type-check after each batch.** Catch breakage early rather than debugging a large changeset.

## Strategy Reference

For detailed patterns and code examples for each strategy type, read [references/strategies.md](references/strategies.md).
