# Consolidation Strategies Reference

## Table of Contents
1. [Shared Constants Extraction](#1-shared-constants-extraction)
2. [Derived Value Computation](#2-derived-value-computation)
3. [Data Object Deduplication](#3-data-object-deduplication)
4. [Page Merging](#4-page-merging)
5. [Tabbed Page Combination](#5-tabbed-page-combination)
6. [Data Source Wiring](#6-data-source-wiring)
7. [Navigation Updates](#7-navigation-updates)

---

## 1. Shared Constants Extraction

**Signal:** The same scalar value (string, number, boolean) appears identically in 2+ data files.

**Pattern:** Create `constants.ts` (or equivalent), export each value as a named constant, then import in consuming files.

**Example duplicates to look for:**
- Employee counts, health scores, risk levels
- Formatted currency strings and their numeric equivalents
- Dates (renewal, contract start/end)
- Boolean flags (auto-renewal, feature toggles)

**Naming convention:** UPPER_SNAKE_CASE for scalars: `EMPLOYEES`, `HEALTH_SCORE`, `C_ARR_VALUE`.

**Circular dependency check:** Before adding an import, verify the target file does not already import from the source file.

## 2. Derived Value Computation

**Signal:** A hardcoded value that can be computed from existing data.

**Common patterns:**
- `totalX = partA + partB` (e.g., total ARR = okta ARR + auth0 ARR)
- `count = array.length` (e.g., open opportunity count)
- `topN = fullArray.slice(0, N).map(...)` (e.g., top 10 apps from full portfolio)

**Why this matters:** Hardcoded values silently drift from their source data. If the source array changes and the hardcoded count doesn't, you get data inconsistency with no error.

**Implementation:** Replace the literal with the expression. Import the source data if in a different file. Verify no circular dependency.

## 3. Data Object Deduplication

**Signal:** The same structured object (breach history, company profile subset) appears in 2+ files with overlapping fields.

**Pattern:** Identify the richer/canonical version. Have the other file import from it.

**Decision rule:** The canonical version is whichever has more fields, is more specific to the domain, or lives in the more obvious location.

**Preserve shape:** If the consuming code expects a different shape, destructure or map from the canonical source rather than changing the consumer.

## 4. Page Merging

**Signal:** Two pages share 60%+ thematic overlap (e.g., "Company Research" and "Business Intelligence" both cover company financials, strategy, executives).

**Process:**
1. Read both section components fully
2. Identify unique content in the page being absorbed
3. Extract any inline data arrays into the appropriate data file
4. Add the unique sections to the surviving component (numbered sequentially)
5. Update the surviving component's imports
6. Delete the absorbed component and its route directory
7. Update sidebar and home page navigation

**Section numbering:** Continue sequentially from the surviving component's last section number.

## 5. Tabbed Page Combination

**Signal:** Multiple pages that cover the same domain but different facets (e.g., PAM Overview / PAM Technical / PAM Call Prep).

**Pattern:** Create a thin `'use client'` tabbed wrapper that conditionally renders the existing section components. Do not merge the section components themselves.

```tsx
// Tabbed wrapper pattern
'use client';
import { useState } from 'react';

const tabs = [
  { key: 'overview', label: 'Overview' },
  { key: 'technical', label: 'Technical Fit' },
] as const;
type TabKey = (typeof tabs)[number]['key'];

export default function DomainTabbed() {
  const [activeTab, setActiveTab] = useState<TabKey>('overview');
  return (
    <>
      {/* Tab bar */}
      {activeTab === 'overview' && <OverviewSection />}
      {activeTab === 'technical' && <TechnicalSection />}
    </>
  );
}
```

**Advantages:** Existing section components remain untouched and independently testable. Extraction back to separate pages is trivial if needed.

## 6. Data Source Wiring

**Signal:** An inline data array in a component duplicates or overlaps with data already in a data file.

**Pattern:** Delete the inline array and import from the canonical data file. Adjust the rendering code if the shape differs (map fields as needed).

## 7. Navigation Updates

After any page addition/removal, update **both** navigation sources:

1. **Sidebar:** `navGroups[]` array (usually in `Sidebar.tsx` or a nav config)
2. **Home page:** `cardGroups[]` array (usually in the root `page.tsx`)

These are manually kept in sync — there is no shared config between them. Always update both.

**Checklist after page removal:**
- [ ] Sidebar link removed
- [ ] Home page nav card removed
- [ ] Route directory deleted (including empty parent dirs)
- [ ] Component file deleted (if fully absorbed)
- [ ] No remaining imports reference the deleted files
