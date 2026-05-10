---
name: okta-slides
description: Generate a branded Okta Google Slides presentation as a copy-paste Google Apps Script. Use when the user wants to create a slide deck, presentation, or slides following Okta brand guidelines. Outputs a complete, runnable Google Apps Script that builds the presentation in Google Drive.
argument-hint: [topic, audience, or outline]
---

# Okta Branded Slide Deck Generator

You generate a complete, runnable Google Apps Script that creates a branded Okta Google Slides presentation. The user pastes it into script.google.com and runs it -- no plugins, no manual formatting.

This skill supports 15 slide layouts from the Okta Corp Template v2 and integrates with the presales data ecosystem to auto-populate content from prior research.

---

## Phase 0: Understand Intent

### Presales Data Detection

Before asking questions, check for existing account data:

```
1. Check if $ARGUMENTS contains a company name
2. If company name found, scan output/<company>/ for:
   - research-*.md       -> company overview, industry context
   - okta-discovery-*.md -> pain points, current state, next steps
   - business-case-*.md  -> ROI stats for stat callout slides
   - stakeholders-*.md   -> names for presenter/team slides
   - competitive-*.md    -> Okta vs. competitor for two-column slides
   - executive-briefing-*.md -> full narrative flow for exec decks
   - _inbox/*.txt        -> call quotes, attendee names, action items
3. Report what was found: "Found [N] prior outputs for [company]. Using them to pre-populate slides."
4. If no presales data: "No prior outputs found. I'll build content from what you tell me."
```

### Collect Information (2-3 exchanges)

From `$ARGUMENTS` and conversation, determine:

1. **Topic / title** of the presentation
2. **Audience** (internal team, exec, customer, cross-functional)
3. **Presenter name(s)** -- ask directly. If none provided, use `[Presenter Name]` as placeholder. Never use a hardcoded default.
4. **Deck type** -- classify from the table below, or ask if ambiguous

### Deck Type Classification

| Deck Type | Trigger Words | Typical Slides | Key Layouts |
|-----------|--------------|----------------|-------------|
| Discovery Recap | "discovery", "after call", "recap" | 10-14 | Content, Two-Col, Section+List |
| Executive Briefing | "exec", "CISO", "board", "leadership" | 8-12 | Stat Callout, Quote, Content Dark |
| POC Kickoff | "POC", "proof of concept", "pilot" | 12-16 | Image+Content, Three-Col, Team |
| QBR | "business review", "quarterly", "QBR" | 14-18 | Stat Callout, Two-Col, Section+List |
| Demo Narrative | "demo", "story", "walkthrough" | 8-12 | Content Dark, Quote, Stat Callout |
| Custom | anything else | varies | varies |

### Drive Folder Preflight Note

Remind the user at the end of Phase 0:

> The script uses PNG backgrounds from a shared Google Drive folder. The `checkDriveAccess()` preflight function will verify access before creating slides. If it fails, the error message includes the folder URL and fix steps.

---

## Phase 1: Plan Slide Structure

Generate a slide-by-slide outline as a table before writing any code. Show the user what they're getting.

**Format:**

| # | Layout | Title | Data Source |
|---|--------|-------|-------------|
| 1 | Title | [deck title] | Manual |
| 2 | Agenda | Agenda | Auto-generated from sections |
| 3 | Section Header | [section name] | Manual |
| ... | ... | ... | ... |

### Deck Type Templates

**Discovery Recap (10-14 slides):**
1. Title -- deck title + presenter(s)
2. Safe Harbor -- if any forward-looking content
3. Agenda -- sections list
4. Section Header -- "What We Heard"
5. Content Light -- key pain points (from okta-discovery or manual)
6. Two-Column -- current state vs. desired state
7. Section Header -- "Recommended Approach"
8. Content Light -- proposed solution pillars
9. Section+List -- implementation phases / next steps
10. Stat Callout -- key metric or proof point
11. Closing -- thank you + contact info

**Executive Briefing (8-12 slides):**
1. Title -- deck title + presenter(s)
2. Safe Harbor -- required for exec audiences
3. Stat Callout -- headline metric (breach cost, ROI, etc.)
4. Content Dark -- the challenge / burning platform
5. Quote -- analyst or customer quote
6. Two-Column -- before/after or Okta vs. status quo
7. Stat Callout -- 3-stat row (ROI, time saved, risk reduced)
8. Content Light -- recommended next steps
9. Closing -- thank you + contact info

**POC Kickoff (12-16 slides):**
1. Title -- deck title + presenter(s)
2. Safe Harbor
3. Agenda
4. Section Header -- "POC Objectives"
5. Content Light -- success criteria
6. Three-Column -- use case pillars
7. Section Header -- "Architecture"
8. Image+Content -- architecture placeholder + description
9. Section Header -- "Timeline & Team"
10. Section+List -- phases with dates
11. Team Card -- POC team members
12. Content Light -- logistics / access requirements
13. Closing -- next steps + contact info

**QBR (14-18 slides):**
1. Title -- deck title + presenter(s)
2. Safe Harbor
3. Agenda
4. Section Header -- "Performance Highlights"
5. Stat Callout -- 3-stat row (adoption, tickets reduced, incidents)
6. Content Light -- detailed metrics
7. Two-Column -- before/after comparison
8. Section Header -- "Key Initiatives"
9. Content Light -- completed work
10. Section+List -- upcoming roadmap items
11. Section Header -- "Value Delivered"
12. Stat Callout -- ROI or cost savings
13. Quote -- internal champion quote
14. Content Light -- recommendations for next quarter
15. Closing -- next meeting date + contact info

**Demo Narrative (8-12 slides):**
1. Title -- deck title + presenter(s)
2. Content Dark -- "The Challenge" (set the scene)
3. Quote -- customer pain point or analyst insight
4. Section Header -- "The Solution"
5. Content Light -- what we'll demonstrate
6. Stat Callout -- key differentiator metric
7. Content Dark -- "What This Means For You"
8. Closing -- next steps + contact info

Present the outline to the user. Adjust based on feedback before generating code.

---

## Phase 2: Generate & Refine

Generate the complete Google Apps Script based on the approved outline. Then offer the co-create menu:

```
Here's the complete script. What would you like to do?

A) Add a slide -- which layout and where?
B) Remove a slide -- which number?
C) Change a slide's content -- which one?
D) Switch a background -- which slide, which PNG?
E) Edit presenter info
F) Save as-is
G) Other
```

Each action regenerates the affected portion and loops back to this menu.

### Run Instructions

After the user is satisfied, include these instructions verbatim:

---
**To run:**
1. Go to [script.google.com](https://script.google.com) -> New project
2. Delete any existing code, paste the script
3. Click Run -> `createOktaPresentation`
4. Authorize when prompted (Google will ask for Drive/Slides permissions)
5. Your presentation will appear in Google Drive -- the URL is logged in the Execution log

**Troubleshooting:**
- "No access to folder" -- Open `https://drive.google.com/drive/folders/1EGQnbHwbk4jD0rats7Z_AwYmc15FLeEq` and request access, or copy the PNGs to your own Drive folder and update `FOLDER_ID`
- "Missing: [filename]" -- The PNG background file wasn't found. Check the folder contains the exact filename listed in the error
- "TypeError: Cannot read property" -- Make sure you authorized both Drive and Slides permissions when prompted
---

---

## Phase 3: Save & Learn

After the user approves the final script:

1. Save the script output to `output/<company>/slides-<topic>-<YYYY-MM-DD>.md` (wrapped in a code fence)
2. Update `output/<company>/_state.md` with the skill run
3. Write feedback file to `output/<company>/_feedback/okta-slides-<YYYY-MM-DD>.md`

---

## Okta Brand Specification

### Canvas
- **Dimensions**: 720pt wide x 405pt tall (Google Slides 16:9 default)
- All coordinates below are in points (pt)
- Note: The Okta Corp Template PPTX uses 960x540pt (PowerPoint's 16:9). Google Slides uses 720x405pt. Same aspect ratio, different coordinate space. All layouts in this skill use Google Slides coordinates.

### Typography

**Primary font: DM Sans** -- use throughout, no exceptions.

**Typography Trade-Off:** Okta's official brand font is Aeonik, which requires a Typekit/Adobe Fonts license and cannot be embedded in Google Slides via Apps Script. DM Sans is the closest Google Fonts match -- similar geometric sans-serif proportions, x-height, and character width. This is the standard approximation for any Google Slides workflow.

| Element | Size | Weight | Color (light bg) | Color (dark/blue bg) |
|---------|------|--------|-------------------|---------------------|
| Title slide headline | 48-52pt | Regular | -- | White `#FFFFFF` |
| Title slide tagline | 14-16pt | Regular | -- | Cloud `#B6C9FF` |
| Title slide presenter | 11-12pt | Regular | -- | White `#FFFFFF` |
| Slide titles | 28-36pt | Regular | Carbon `#191919` | White `#FFFFFF` |
| Body / bullets | 15-18pt | Regular | Carbon `#191919` | Snow `#FFFEFA` |
| Agenda numbers | 26-40pt | Regular | Carbon `#191919` | -- |
| Agenda items | 15-18pt | Regular | Carbon `#191919` | -- |
| Stat callout number | 56-72pt | Bold | Sky `#3F59E4` | White `#FFFFFF` |
| Stat callout label | 14-16pt | Regular | Carbon `#191919` | Cloud `#B6C9FF` |
| Quote text | 24-28pt | Regular | Carbon `#191919` | White `#FFFFFF` |
| Quote attribution | 13-14pt | Regular | Slate `#6B665F` | Cloud `#B6C9FF` |
| Footer | 8pt | Regular | Slate `#6B665F` | White `#FFFFFF` |

### Colors

| Name | Hex | Usage |
|------|-----|-------|
| Carbon | `#191919` | Dark backgrounds, body text on light |
| Snow | `#FFFEFA` | Default content slide background |
| Cream | `#F6F1E7` | Agenda slide background, warm neutral |
| Sky | `#3F59E4` | Title slide bg, section headers, key accents |
| Cobalt | `#1A31A9` | Deep blue accent |
| Cloud | `#B6C9FF` | Light blue accent, highlights, subtitles on dark |
| Seafoam | `#4CB7A3` | Teal accent |
| Turquoise | `#B1E4DE` | Light teal accent |
| Slate | `#6B665F` | Secondary text, footer text on light slides |
| Gravel | `#AFABA1` | Tertiary/muted text |
| Sand | `#E8DCC7` | Warm neutral accent |
| Ocean | `#096256` | Deep teal, use sparingly |
| White | `#FFFFFF` | Text/elements on dark backgrounds |

Secondary palette (charts/diagrams only): Oak `#694A01`, Clay `#763101`, Forest `#005429`, Eggplant `#3D10A6`, Papaya `#EF9B05`, Tangerine `#E27133`, Clover `#149750`, Violet `#7549F2`, Goldenrod `#F4D594`, Melon `#F2AC84`, Fern `#8FC88A`, Lilac `#B49BFC`

### PNG Backgrounds

All slides use pre-built PNG backgrounds loaded from Google Drive. These have the Okta logo, aura, and footer **already baked in** -- do not add them in the script.

**Drive folder ID:** `1EGQnbHwbk4jD0rats7Z_AwYmc15FLeEq`

| Filename | Description | Use for |
|---|---|---|
| `Title.png` | Blue, okta logo top-left, aura top-right | Title slide |
| `Blank Snow.png` | Off-white/light | Content slides (light) |
| `Blank Cream.png` | Warm cream/beige | Agenda, warm content |
| `Blank Blue.png` | Flat solid blue | Simple blue content |
| `Blank Blue Circle.png` | Blue with large circle gradient | Concept, closing |
| `Blank Blue Bokeh.png` | Blue abstract light effect | Dramatic content |
| `Blank Dark.png` | Pure black | High-impact dark slides |
| `Blank Dark Circle.png` | Dark with circle gradient | Dark section/content |
| `Statement Dark.png` | Dark soft gradient | Section headers, problem slides |
| `Statement Blue.png` | Blue with horizontal bands | Section dividers |
| `Section Blue Circle.png` | Blue circle variant | Section headers, closing |
| `Cover Blue.png` | Blue with "okta" wordmark centered | Closing (has baked-in text) |
| `Cover Dark.png` | Dark with "okta" wordmark centered | Dark closing (has baked-in text) |
| `Thank You.png` | Blue "Thank you!" pre-baked | Closing thank-you variant |
| `Questions.png` | Blue "Questions?" pre-baked | Q&A |
| `Q&A.png` | Blue "Q&A" pre-baked | Q&A |
| `Blank Blue Gradient.png` | Blue-to-light gradient | Soft content |
| `Blank Blue Bokeh Alt.png` | Blue bokeh variant | Alternate dramatic |
| `Blank Blue Circle Alt.png` | Blue circle variant | Alternate section |

**Text color by background:**
- Light backgrounds (Snow, Cream): Carbon `#191919` for titles, Carbon for body
- Dark backgrounds (Dark, Dark Circle, Statement Dark): White `#FFFFFF` for titles, Snow `#FFFEFA` for body
- Blue backgrounds (Blue, Blue Circle, Statement Blue, Title): White `#FFFFFF` for titles, Cloud `#B6C9FF` for subtitles/accents

### Footer
Already baked into all PNG backgrounds. **Do not add footer text in the script.**

---

## Layout Library (15 Layouts)

### Layout 1: Title Slide

**Background:** `Title.png` (logo, aura, footer baked in)

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| Headline (max 3 lines) | 40 | 120 | 520 | 150 | 48 | `#FFFFFF` | no |
| Tagline/subtitle | 40 | 284 | 520 | 28 | 15 | `#B6C9FF` | no |
| Presenter 1 | 40 | 334 | 200 | 38 | 11 | `#FFFFFF` | no |
| Presenter 2 (if present) | 250 | 334 | 200 | 38 | 11 | `#FFFFFF` | no |
| Presenter 3 (if present) | 460 | 334 | 200 | 38 | 11 | `#FFFFFF` | no |

**Multi-presenter support:** Position up to 3 presenters side-by-side. Each presenter block is `Name\nTitle, Company` format.

**Do NOT add:** logo, aura, "The World's Identity Company", or footer text.

```javascript
// ── SLIDE: Title ─────────────────────────────────────
var s = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(s, 'Title.png');
txt(s, 'Presentation Title Here\nSecond line if needed', 40, 120, 520, 150, 48, '#FFFFFF', false);
txt(s, 'Tagline or subtitle', 40, 284, 520, 28, 15, '#B6C9FF', false);
// Presenter 1
txt(s, 'First Last\nTitle, Company', 40, 334, 200, 38, 11, '#FFFFFF', false);
// Presenter 2 (if applicable)
txt(s, 'First Last\nTitle, Company', 250, 334, 200, 38, 11, '#FFFFFF', false);
```

---

### Layout 2: Agenda

**Background:** `Blank Cream.png`

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| "Agenda" heading | 40 | 24 | 300 | 58 | 48 | `#191919` | no |
| Rule lines | 430 | agY-8 | to 680 | -- | -- | `#191919` | -- |
| Item numbers ("01") | 430 | agY | 50 | 36 | 26 | `#191919` | no |
| Item text | 490 | agY+4 | 200 | 28 | 15 | `#191919` | no |

Starting agY: 110. Increment: 48pt per item. Max 7 items.

```javascript
// ── SLIDE: Agenda ─────────────────────────────────────
var ag = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(ag, 'Blank Cream.png');
txt(ag, 'Agenda', 40, 24, 300, 58, 48, '#191919', false);
var agItems = ['Topic one', 'Topic two', 'Topic three'];
var agY = 110;
for (var i = 0; i < agItems.length; i++) {
  line(ag, 430, agY - 8, 680, agY - 8, '#191919');
  txt(ag, ('0' + (i + 1)).slice(-2), 430, agY, 50, 36, 26, '#191919', false);
  txt(ag, agItems[i], 490, agY + 4, 200, 28, 15, '#191919', false);
  agY += 48;
}
```

---

### Layout 3: Section Header

**Background:** `Statement Dark.png` (default) or `Blank Dark Circle.png` or `Statement Blue.png`

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| Section number (optional) | 40 | 130 | 80 | 40 | 14 | `#B6C9FF` | no |
| Section title | 40 | 175 | 600 | 120 | 44 | `#FFFFFF` | no |
| Subtitle (optional) | 40 | 240 | 600 | 40 | 16 | `#B6C9FF` | no |

```javascript
// ── SLIDE: Section Header ─────────────────────────────
var sh = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(sh, 'Statement Dark.png');
txt(sh, '01', 40, 130, 80, 40, 14, '#B6C9FF', false);
txt(sh, 'Section Title Here', 40, 175, 600, 120, 44, '#FFFFFF', false);
// Optional subtitle:
// txt(sh, 'Supporting context for this section', 40, 240, 600, 40, 16, '#B6C9FF', false);
```

---

### Layout 4: Content Slide (Light)

**Background:** `Blank Snow.png` or `Blank Cream.png`

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| Slide title | 40 | 24 | 640 | 44 | 30 | `#191919` | no |
| Rule line | 40,72 to 680,72 | -- | -- | -- | -- | `#191919` | -- |
| Body (bullets) | 40 | 84 | 640 | 260 | 16 | `#191919` | no |

Max 6 bullets. Split into multiple slides if more. Use `\u2022` prefix for bullets.

```javascript
// ── SLIDE: Content (light) ────────────────────────────
var cs = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(cs, 'Blank Snow.png');
txt(cs, 'Slide Title', 40, 24, 640, 44, 30, '#191919', false);
line(cs, 40, 72, 680, 72, '#191919');
var bullets = [
  '\u2022 Key point one',
  '\u2022 Key point two',
  '\u2022 Key point three'
];
txt(cs, bullets.join('\n\n'), 40, 84, 640, 260, 16, '#191919', false);
```

---

### Layout 5: Content Slide (Dark)

**Background:** `Blank Dark.png` or `Statement Dark.png`

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| Slide title | 40 | 24 | 640 | 44 | 30 | `#FFFFFF` | no |
| Rule line | 40,72 to 680,72 | -- | -- | -- | -- | `#3F59E4` | -- |
| Body (bullets) | 40 | 84 | 640 | 260 | 16 | `#FFFEFA` | no |

```javascript
// ── SLIDE: Content (dark) ─────────────────────────────
var cd = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(cd, 'Blank Dark.png');
txt(cd, 'Slide Title', 40, 24, 640, 44, 30, '#FFFFFF', false);
line(cd, 40, 72, 680, 72, '#3F59E4');
var bullets = [
  '\u2022 Key point one',
  '\u2022 Key point two',
  '\u2022 Key point three'
];
txt(cd, bullets.join('\n\n'), 40, 84, 640, 260, 16, '#FFFEFA', false);
```

---

### Layout 6: Two-Column Content

**Background:** `Blank Snow.png` or `Blank Cream.png`

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| Slide title | 40 | 24 | 640 | 40 | 28 | `#191919` | no |
| Left rule line | 40,68 to 330,68 | -- | -- | -- | -- | `#3F59E4` | -- |
| Left heading | 40 | 78 | 278 | 24 | 15 | `#191919` | yes |
| Left body | 40 | 106 | 278 | 240 | 13 | `#191919` | no |
| Right rule line | 370,68 to 660,68 | -- | -- | -- | -- | `#3F59E4` | -- |
| Right heading | 370 | 78 | 278 | 24 | 15 | `#191919` | yes |
| Right body | 370 | 106 | 278 | 240 | 13 | `#191919` | no |

```javascript
// ── SLIDE: Two-Column Content ─────────────────────────
var tc = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(tc, 'Blank Cream.png');
txt(tc, 'Slide Title', 40, 24, 640, 40, 28, '#191919', false);
line(tc, 40, 68, 330, 68, '#3F59E4');
txt(tc, 'Left Heading', 40, 78, 278, 24, 15, '#191919', true);
txt(tc, 'Body text here.\n\n\u2022 Supporting bullet\n\u2022 Supporting bullet', 40, 106, 278, 240, 13, '#191919', false);
line(tc, 370, 68, 660, 68, '#3F59E4');
txt(tc, 'Right Heading', 370, 78, 278, 24, 15, '#191919', true);
txt(tc, 'Body text here.\n\n\u2022 Supporting bullet\n\u2022 Supporting bullet', 370, 106, 278, 240, 13, '#191919', false);
```

---

### Layout 7: Closing

**Background:** `Blank Blue Circle.png` (default), `Section Blue Circle.png`, `Thank You.png`, `Questions.png`, `Cover Blue.png`, or `Cover Dark.png`

**Variants:**
- **Thank You** -- use `Thank You.png` (text baked in, add contact info only)
- **Questions** -- use `Questions.png` (text baked in, add contact info only)
- **Cover** -- use `Cover Blue.png` or `Cover Dark.png` (wordmark baked in, minimal text)
- **Custom** -- use `Blank Blue Circle.png` with custom closing message

| Element (Custom variant) | x | y | w | h | Size | Color | Bold |
|--------------------------|---|---|---|---|------|-------|------|
| Closing message | 40 | 140 | 500 | 120 | 50 | `#FFFFFF` | no |
| Contact / next step | 40 | 280 | 400 | 24 | 13 | `#B6C9FF` | no |

| Element (Thank You / Questions variant) | x | y | w | h | Size | Color | Bold |
|-----------------------------------------|---|---|---|---|------|-------|------|
| Contact / next step only | 40 | 310 | 400 | 24 | 13 | `#B6C9FF` | no |

```javascript
// ── SLIDE: Closing (custom variant) ───────────────────
var cl = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(cl, 'Blank Blue Circle.png');
txt(cl, 'Thank you', 40, 140, 500, 120, 50, '#FFFFFF', false);
txt(cl, 'name@okta.com', 40, 280, 400, 24, 13, '#B6C9FF', false);

// ── SLIDE: Closing (Thank You variant) ────────────────
// var cl = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
// bg(cl, 'Thank You.png');
// txt(cl, 'name@okta.com', 40, 310, 400, 24, 13, '#B6C9FF', false);
```

---

### Layout 8: Stat / Metric Callout

**Background:** `Blank Snow.png` (light) or `Blank Dark.png` (dark)

Use for ROI figures, Forrester proof points, customer metrics. Two sub-layouts:

**Single big number:**

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| Stat number | 40 | 100 | 640 | 100 | 72 | `#3F59E4` (light) / `#FFFFFF` (dark) | yes |
| Stat label | 40 | 210 | 640 | 40 | 18 | `#191919` (light) / `#B6C9FF` (dark) | no |
| Source citation | 40 | 260 | 640 | 24 | 12 | `#6B665F` (light) / `#AFABA1` (dark) | no |

**Three-stat row:**

| Element | Col 1 x | Col 2 x | Col 3 x | y (number) | y (label) | w each | Size (num) | Size (label) |
|---------|---------|---------|---------|------------|-----------|--------|------------|--------------|
| Stat number | 40 | 260 | 480 | 120 | -- | 200 | 56 | -- |
| Stat label | 40 | 260 | 480 | -- | 195 | 200 | -- | 14 |

Colors follow same light/dark rules as single. Source citation at y:280.

```javascript
// ── SLIDE: Stat Callout (single) ──────────────────────
var st = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(st, 'Blank Snow.png');
var numBox = txt(st, '211%', 40, 100, 640, 100, 72, '#3F59E4', true);
setCenter(numBox);
var labBox = txt(st, 'ROI with Okta Identity Governance', 40, 210, 640, 40, 18, '#191919', false);
setCenter(labBox);
txt(st, 'Source: Forrester TEI for OIG, June 2025', 40, 260, 640, 24, 12, '#6B665F', false);

// ── SLIDE: Stat Callout (three-stat row) ──────────────
var st3 = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(st3, 'Blank Snow.png');
var n1 = txt(st3, '211%', 40, 120, 200, 70, 56, '#3F59E4', true);
setCenter(n1);
var l1 = txt(st3, 'ROI', 40, 195, 200, 30, 14, '#191919', false);
setCenter(l1);
var n2 = txt(st3, '<6 mo', 260, 120, 200, 70, 56, '#3F59E4', true);
setCenter(n2);
var l2 = txt(st3, 'Payback period', 260, 195, 200, 30, 14, '#191919', false);
setCenter(l2);
var n3 = txt(st3, '$1.8M', 480, 120, 200, 70, 56, '#3F59E4', true);
setCenter(n3);
var l3 = txt(st3, '3-year NPV', 480, 195, 200, 30, 14, '#191919', false);
setCenter(l3);
txt(st3, 'Source: Forrester TEI for OIG, June 2025', 40, 280, 640, 24, 12, '#6B665F', false);
```

---

### Layout 9: Image + Content Split

**Background:** `Blank Snow.png` or `Blank Cream.png`

Use for architecture diagrams, screenshots, product visuals paired with explanatory text.

**Left-image variant:**

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| Image placeholder | 40 | 24 | 320 | 340 | -- | -- | -- |
| Content title | 380 | 24 | 300 | 40 | 24 | `#191919` | no |
| Rule line | 380,68 to 680,68 | -- | -- | -- | -- | `#3F59E4` | -- |
| Content body | 380 | 80 | 300 | 280 | 14 | `#191919` | no |

**Right-image variant:** Mirror the x positions (content at x:40 w:300, image at x:360 w:320).

```javascript
// ── SLIDE: Image + Content (left image) ───────────────
var ic = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(ic, 'Blank Snow.png');
imgPlaceholder(ic, 40, 24, 320, 340, 'Architecture Diagram', SlidesApp.ShapeType.RECTANGLE);
txt(ic, 'Content Title', 380, 24, 300, 40, 24, '#191919', false);
line(ic, 380, 68, 680, 68, '#3F59E4');
txt(ic, 'Description text goes here.\n\n\u2022 Key point one\n\u2022 Key point two', 380, 80, 300, 280, 14, '#191919', false);
```

---

### Layout 10: Quote / Statement

**Background:** `Blank Cream.png` (light) or `Statement Dark.png` (dark)

Use for customer testimonials, analyst quotes, bold statements.

| Element | x | y | w | h | Size | Color (light) | Color (dark) | Bold |
|---------|---|---|---|---|------|---------------|-------------|------|
| Quote mark (\u201C) | 40 | 80 | 40 | 60 | 72 | `#3F59E4` | `#B6C9FF` | no |
| Quote text | 80 | 110 | 560 | 160 | 24 | `#191919` | `#FFFFFF` | no |
| Attribution | 80 | 290 | 560 | 24 | 14 | `#6B665F` | `#B6C9FF` | no |

```javascript
// ── SLIDE: Quote (light) ──────────────────────────────
var qt = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(qt, 'Blank Cream.png');
txt(qt, '\u201C', 40, 80, 40, 60, 72, '#3F59E4', false);
txt(qt, 'The labor savings justify the cost overall.', 80, 110, 560, 160, 24, '#191919', false);
txt(qt, '\u2014 CIO, Financial Services (Forrester TEI, June 2025)', 80, 290, 560, 24, 14, '#6B665F', false);
```

---

### Layout 11: Three-Column Grid

**Background:** `Blank Snow.png` or `Blank Cream.png`

Use for value pillars, capability comparison, three-part frameworks.

| Element | Col 1 x | Col 2 x | Col 3 x | y | w each | h | Size | Color | Bold |
|---------|---------|---------|---------|---|--------|---|------|-------|------|
| Slide title | 40 | -- | -- | 24 | 640 | 40 | 28 | `#191919` | no |
| Rule line | 40-680 | -- | -- | 68 | -- | -- | -- | `#191919` | -- |
| Column heading | 40 | 260 | 480 | 80 | 200 | 28 | 16 | `#3F59E4` | yes |
| Column body | 40 | 260 | 480 | 114 | 200 | 240 | 13 | `#191919` | no |

```javascript
// ── SLIDE: Three-Column Grid ──────────────────────────
var g3 = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(g3, 'Blank Snow.png');
txt(g3, 'Slide Title', 40, 24, 640, 40, 28, '#191919', false);
line(g3, 40, 68, 680, 68, '#191919');
// Column 1
txt(g3, 'Column One', 40, 80, 200, 28, 16, '#3F59E4', true);
txt(g3, '\u2022 Point one\n\u2022 Point two\n\u2022 Point three', 40, 114, 200, 240, 13, '#191919', false);
// Column 2
txt(g3, 'Column Two', 260, 80, 200, 28, 16, '#3F59E4', true);
txt(g3, '\u2022 Point one\n\u2022 Point two\n\u2022 Point three', 260, 114, 200, 240, 13, '#191919', false);
// Column 3
txt(g3, 'Column Three', 480, 80, 200, 28, 16, '#3F59E4', true);
txt(g3, '\u2022 Point one\n\u2022 Point two\n\u2022 Point three', 480, 114, 200, 240, 13, '#191919', false);
```

---

### Layout 12: Four-Column Grid

**Background:** `Blank Snow.png` or `Blank Cream.png`

Use for process steps, feature grids, comparison matrices.

| Element | Col 1 x | Col 2 x | Col 3 x | Col 4 x | y | w each | h |
|---------|---------|---------|---------|---------|---|--------|---|
| Slide title | 40 | -- | -- | -- | 24 | 640 | 40 |
| Rule line | 40-680 | -- | -- | -- | 68 | -- | -- |
| Step number circle | 40 | 200 | 370 | 540 | 80 | 40 | 40 |
| Column heading | 40 | 200 | 370 | 540 | 130 | 150 | 24 |
| Column body | 40 | 200 | 370 | 540 | 160 | 150 | 200 |

| Element | Size | Color | Bold |
|---------|------|-------|------|
| Slide title | 28 | `#191919` | no |
| Step number | 18 | `#3F59E4` | yes |
| Column heading | 14 | `#191919` | yes |
| Column body | 12 | `#191919` | no |

```javascript
// ── SLIDE: Four-Column Grid ───────────────────────────
var g4 = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(g4, 'Blank Snow.png');
txt(g4, 'Slide Title', 40, 24, 640, 40, 28, '#191919', false);
line(g4, 40, 68, 680, 68, '#191919');
var colX = [40, 200, 370, 540];
var colHeads = ['Step 1', 'Step 2', 'Step 3', 'Step 4'];
var colBodies = ['Description', 'Description', 'Description', 'Description'];
for (var c = 0; c < 4; c++) {
  txt(g4, String(c + 1), colX[c], 80, 40, 40, 18, '#3F59E4', true);
  txt(g4, colHeads[c], colX[c], 130, 150, 24, 14, '#191919', true);
  txt(g4, colBodies[c], colX[c], 160, 150, 200, 12, '#191919', false);
}
```

---

### Layout 13: Team / Presenter Card

**Background:** `Blank Snow.png` or `Blank Cream.png`

Use for POC team introductions, presenter bios.

**Variants:**
- 1-person: centered at x:260
- 2-person: positioned at x:120 and x:400
- 3-person: positioned at x:40, x:260, x:480

Each person block:

| Element | x (relative) | y | w | h | Size | Color | Bold |
|---------|-------------|---|---|---|------|-------|------|
| Headshot placeholder | +20 | 80 | 120 | 120 | -- | -- | -- |
| Name | +0 | 215 | 160 | 24 | 16 | `#191919` | yes |
| Title | +0 | 243 | 160 | 20 | 12 | `#6B665F` | no |
| Company | +0 | 267 | 160 | 20 | 12 | `#6B665F` | no |

Slide title at standard position (40, 24, 640, 40, 28).

```javascript
// ── SLIDE: Team Card (3-person) ───────────────────────
var tm = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(tm, 'Blank Snow.png');
txt(tm, 'Your Team', 40, 24, 640, 40, 28, '#191919', false);
line(tm, 40, 68, 680, 68, '#191919');
var teamX = [40, 260, 480];
var teamNames = ['First Last', 'First Last', 'First Last'];
var teamTitles = ['Solutions Engineer', 'Account Executive', 'Solution Architect'];
for (var t = 0; t < teamNames.length; t++) {
  imgPlaceholder(tm, teamX[t] + 20, 80, 120, 120, teamNames[t], SlidesApp.ShapeType.ELLIPSE);
  txt(tm, teamNames[t], teamX[t], 215, 160, 24, 16, '#191919', true);
  txt(tm, teamTitles[t], teamX[t], 243, 160, 20, 12, '#6B665F', false);
  txt(tm, 'Okta', teamX[t], 267, 160, 20, 12, '#6B665F', false);
}
```

---

### Layout 14: Safe Harbor

**Background:** `Blank Snow.png`

Required before any forward-looking content. Standard legal boilerplate.

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| "Safe Harbor" heading | 40 | 24 | 640 | 40 | 28 | `#191919` | no |
| Rule line | 40,68 to 680,68 | -- | -- | -- | -- | `#191919` | -- |
| Disclaimer text | 40 | 84 | 640 | 200 | 11 | `#6B665F` | no |
| Verification note | 40 | 310 | 640 | 40 | 10 | `#AFABA1` | no |

**Standard boilerplate text:**

```
This presentation may contain forward-looking statements including, but not
limited to, statements regarding Okta's plans, objectives, expectations,
strategies, and prospects. These forward-looking statements are based on
current expectations and are subject to risks, uncertainties, and assumptions.
Actual results may differ materially from those expressed or implied.

Okta undertakes no obligation to update any forward-looking statements to
reflect events or circumstances after the date of this presentation.

Any unreleased features or functionality referenced herein are not currently
available and may not be delivered on time or at all. Product roadmap
information does not represent a commitment, obligation, or promise to
deliver any material, code, or functionality.
```

```javascript
// ── SLIDE: Safe Harbor ────────────────────────────────
var sh = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(sh, 'Blank Snow.png');
txt(sh, 'Safe Harbor', 40, 24, 640, 40, 28, '#191919', false);
line(sh, 40, 68, 680, 68, '#191919');
var disclaimer = 'This presentation may contain forward-looking statements including, but not '
  + 'limited to, statements regarding Okta\u2019s plans, objectives, expectations, strategies, '
  + 'and prospects. These forward-looking statements are based on current expectations and are '
  + 'subject to risks, uncertainties, and assumptions. Actual results may differ materially from '
  + 'those expressed or implied.\n\n'
  + 'Okta undertakes no obligation to update any forward-looking statements to reflect events or '
  + 'circumstances after the date of this presentation.\n\n'
  + 'Any unreleased features or functionality referenced herein are not currently available and '
  + 'may not be delivered on time or at all. Product roadmap information does not represent a '
  + 'commitment, obligation, or promise to deliver any material, code, or functionality.';
txt(sh, disclaimer, 40, 84, 640, 200, 11, '#6B665F', false);
txt(sh, 'Verify current safe harbor language with Legal before external use.', 40, 310, 640, 40, 10, '#AFABA1', false);
```

---

### Layout 15: Section + Numbered List

**Background:** `Blank Snow.png` or `Blank Cream.png`

Use for process flows, next steps, phased timelines.

| Element | x | y | w | h | Size | Color | Bold |
|---------|---|---|---|---|------|-------|------|
| Section heading | 40 | 24 | 640 | 40 | 28 | `#191919` | no |
| Rule line | 40,68 to 680,68 | -- | -- | -- | -- | `#191919` | -- |
| Step number | 40 | stepY | 30 | 30 | 18 | `#3F59E4` | yes |
| Step text | 80 | stepY | 580 | 30 | 15 | `#191919` | no |

Starting stepY: 84. Increment: 42pt per step. Max 7 steps.

```javascript
// ── SLIDE: Section + Numbered List ────────────────────
var nl = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
bg(nl, 'Blank Snow.png');
txt(nl, 'Next Steps', 40, 24, 640, 40, 28, '#191919', false);
line(nl, 40, 68, 680, 68, '#191919');
var steps = [
  'Schedule technical deep-dive with architecture team',
  'Complete ISPM scan of current environment',
  'Review integration requirements for top 10 apps',
  'Build POC success criteria document'
];
var stepY = 84;
for (var n = 0; n < steps.length; n++) {
  txt(nl, String(n + 1), 40, stepY, 30, 30, 18, '#3F59E4', true);
  txt(nl, steps[n], 80, stepY, 580, 30, 15, '#191919', false);
  stepY += 42;
}
```

---

## Google Apps Script Patterns

Use these exact patterns. Do NOT invent methods.

### Preflight Function

Call `checkDriveAccess()` at the top of `createOktaPresentation()` before creating any slides.

```javascript
function checkDriveAccess() {
  var FOLDER_ID = '1EGQnbHwbk4jD0rats7Z_AwYmc15FLeEq';
  try {
    var folder = DriveApp.getFolderById(FOLDER_ID);
    var name = folder.getName();
    Logger.log('Drive folder accessible: ' + name);
    return true;
  } catch (e) {
    throw new Error(
      'Cannot access the Okta brand assets folder.\n\n'
      + 'Fix: Open this link and request access (or ask your team lead):\n'
      + 'https://drive.google.com/drive/folders/' + FOLDER_ID + '\n\n'
      + 'Alternatively, copy the PNG files to your own Drive folder and update FOLDER_ID in the script.\n\n'
      + 'Original error: ' + e.message
    );
  }
}
```

### Helper Functions

```javascript
function createOktaPresentation() {
  var FOLDER_ID = '1EGQnbHwbk4jD0rats7Z_AwYmc15FLeEq';

  // ── Preflight ────────────────────────────────────────
  checkDriveAccess();

  var pres = SlidesApp.create('Presentation Title');
  pres.getSlides()[0].remove();

  // ── Helpers ──────────────────────────────────────────

  function bg(slide, filename) {
    var folder = DriveApp.getFolderById(FOLDER_ID);
    var files = folder.getFilesByName(filename);
    if (!files.hasNext()) {
      Logger.log(
        'ERROR: Missing background "' + filename + '" in folder.\n'
        + 'Folder: https://drive.google.com/drive/folders/' + FOLDER_ID + '\n'
        + 'Fix: Verify the file exists with the exact name (case-sensitive).\n'
        + 'Slide will have a blank background.'
      );
      return;
    }
    try {
      var img = slide.insertImage(files.next().getBlob(), 0, 0, 720, 405);
      img.sendToBack();
    } catch (e) {
      Logger.log(
        'ERROR: Failed to insert "' + filename + '": ' + e.message + '\n'
        + 'The file may be corrupted or too large. Try re-uploading it.'
      );
    }
  }

  function txt(slide, text, left, top, width, height, size, color, bold) {
    var box = slide.insertTextBox(text, left, top, width, height);
    box.getFill().setTransparent();
    box.getBorder().setTransparent();
    var style = box.getText().getTextStyle();
    style.setFontFamily('DM Sans');
    style.setFontSize(size);
    style.setBold(bold || false);
    style.setForegroundColor(color);
    return box;
  }

  function line(slide, x1, y1, x2, y2, color) {
    var l = slide.insertLine(SlidesApp.LineCategory.STRAIGHT, x1, y1, x2, y2);
    l.getLineFill().setSolidFill(color || '#191919');
    l.setWeight(0.75);
    return l;
  }

  function imgPlaceholder(slide, x, y, w, h, label, shape) {
    var ph = slide.insertShape(shape || SlidesApp.ShapeType.RECTANGLE, x, y, w, h);
    ph.getFill().setSolidFill('#E8DCC7');
    ph.getBorder().getLineFill().setSolidFill('#AFABA1');
    ph.getBorder().setWeight(1);
    var phText = ph.getText();
    phText.setText(label || 'Image');
    var phStyle = phText.getTextStyle();
    phStyle.setFontFamily('DM Sans');
    phStyle.setFontSize(11);
    phStyle.setForegroundColor('#6B665F');
    phText.getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
    return ph;
  }

  function setCenter(textBox) {
    textBox.getText().getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
    return textBox;
  }

  // ── SLIDES GO HERE ───────────────────────────────────
  // (Generate slide code based on the approved outline)

  // ── Done ─────────────────────────────────────────────
  Logger.log('Presentation created: ' + pres.getUrl());
}
```

---

## Quality Rules

Enforce these in every script you generate:

### Mandatory
- **DM Sans only** -- no Arial, no Roboto, no fallbacks
- **Only Okta palette colors** -- no off-brand hex values (see Colors table above)
- **Always call `checkDriveAccess()` before creating slides** -- preflight is not optional
- **Always use `bg()` for every slide** -- never `setBg()` or solid color fills
- **No footer text in scripts** -- footers are baked into all PNG backgrounds
- **No logo or aura on title/closing** -- `Title.png` already has them
- **Unicode escapes for all special characters** -- never embed literal unicode. Use: `\u2014` (em-dash), `\u2022` (bullet), `\u2192` (arrow), `\u201C` / `\u201D` (quotes), `\u2019` (apostrophe)
- **No placeholder text in final output** -- all slide content must be real, written from the user's topic
- **Script must be complete and runnable** -- no `// TODO` or `// add content here`
- **No hardcoded presenter names** -- use actual names from Phase 0 or `[Presenter Name]` placeholder

### Content Rules
- **Title slide**: max 3 lines for the headline
- **Content slides**: max 6 bullets, split into multiple slides if more
- **Stat callout numbers must have source citations** -- no unsourced metrics
- **Safe Harbor required before forward-looking content** -- if the deck references roadmap, EA/beta features, or future plans, insert Layout 14 as slide 2
- **Image placeholders must have descriptive labels** -- "Architecture Diagram", not "Image"
- **Skip empty slides** -- if a slide has no content to fill, omit it rather than generating a blank layout
- **Max 3 stats per stat-callout slide** -- use single stat for high impact, three-stat row for supporting data

### Script Structure
- Always define `checkDriveAccess()` as a top-level function (outside `createOktaPresentation`)
- Helper functions (`bg`, `txt`, `line`, `imgPlaceholder`, `setCenter`) are defined inside `createOktaPresentation`
- Comment each slide section with `// \u2500\u2500 SLIDE: [Layout Name] \u2500\u2500\u2500...`

---

## Presales Integration Reference

When `output/<company>/` contains prior skill outputs, auto-populate slide content:

| Data Source File | Content Extracted | Slide Layout |
|-----------------|-------------------|--------------|
| `research-*.md` | Company overview, industry, employee count | Content Light (context slides) |
| `okta-discovery-*.md` | Pain points, current state gaps, desired state | Two-Column (before/after), Content Light |
| `business-case-*.md` | ROI %, NPV, payback period, cost savings | Stat Callout (single or 3-stat) |
| `stakeholders-*.md` | Stakeholder names, titles, priorities | Team Card, Title slide presenters |
| `competitive-*.md` | Okta vs. competitor strengths/weaknesses | Two-Column, Content Dark |
| `executive-briefing-*.md` | Strategic narrative, key themes, proof points | Quote, Content Dark, Stat Callout |
| `_inbox/*.txt` | Call quotes, attendee names, action items | Quote, Section+List (next steps) |

### Content Extraction Patterns

- **For stat callouts**: Scan for patterns like `NNN%`, `$N.NM`, `NNN hours`, `N days` followed by context
- **For quotes**: Look for direct quotes in `"..."` with attribution
- **For before/after**: Look for "current state" / "desired state" or "before" / "after" sections
- **For next steps**: Look for numbered lists, action items, or "next steps" sections

If presales data is available but thin, fill what you can and flag gaps:
```
"Pre-populated 6 of 12 slides from prior outputs. Slides 4, 7, 9, 10, 11, 12 need manual content."
```

If no presales data exists, generate all content from the user's manual input. This is the graceful degradation path -- the skill works fully without the presales ecosystem.
