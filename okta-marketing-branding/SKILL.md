---
name: okta-marketing-branding
description: |
  Okta marketing design system for building UIs that match okta.com's current visual identity.
  Use this skill when building any customer-facing web page, dashboard, landing page, demo site,
  or marketing collateral that should look like it belongs on okta.com. Trigger on "Okta branded",
  "match Okta's website", "Okta marketing style", "okta.com look", "Okta design system",
  "branded page for Okta", or when any /frontend-design or /account-dashboard-build output
  needs to carry Okta's visual identity. Also use when the user mentions "Okta UI", "Okta theme",
  or wants a page that looks professional and on-brand for Okta sales materials.
---

# Okta Marketing Branding -- Design System

Source: okta.com/solutions/secure-ai/ (scraped April 2026)

This skill provides the exact design tokens, component patterns, and CSS extracted from Okta's
current production marketing site. Use it as the ground-truth reference when building any UI
that should carry Okta's visual identity.

**How to use this skill:**
1. Read `references/design-tokens.css` -- copy it into your project as the base stylesheet
2. Use the component patterns below as HTML/CSS templates for each section type
3. Adapt content but preserve the typographic hierarchy, color system, and spacing rhythm

---

## Design Tokens (Quick Reference)

Read `references/design-tokens.css` for the full CSS custom properties file. Here are the key values:

### Typography

| Role | Font | Weight | Notes |
|------|------|--------|-------|
| Headings (h1-h3, hero, stats, CTA titles) | `"playfair-display", serif` | 400 | `font-variant-numeric: lining-nums proportional-nums; font-feature-settings: "liga" 1` |
| Body, UI, buttons, overlines | `Aeonik, "Helvetica Neue", sans-serif` | 400-500 | Okta's custom sans-serif. Fall back to Helvetica Neue or system sans. |

Font source: `https://use.typekit.net/zer8olz.css` (Adobe Fonts / Typekit).

**Responsive heading scale:**
- Hero h1: 52px (mobile) / 72px (tablet 769px+) / 92px (desktop 1201px+)
- Section h2: Use the `--heading-m` size class (roughly 36-48px)
- Subsection h3: Use `--heading-s` size class (roughly 24-32px)

### Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--okta-black` | `#000000` | Hero backgrounds, dark sections |
| `--okta-dark` | `#191919` | Text, primary button bg, dark UI elements |
| `--okta-cream` | `#fffefa` | Primary text on dark, button fills, page bg |
| `--okta-blue` | `#3f59e4` | Accent, hover states, interactive elements |
| `--okta-glass-bg` | `rgba(255, 255, 255, 0.2)` | Glass morphism card/banner backgrounds |
| `--okta-glass-shadow` | `0px 0px 8px rgba(1, 3, 62, 0.1)` | Glass morphism box-shadow |
| `--okta-gray-900` | `var(--theme-ui-colors-gray900)` | Disclaimer/footnote sections |

### Spacing & Layout

- Grid: 12-column, `max-width: 84rem` (1344px) with `3rem` horizontal padding on desktop
- Breakpoints: `768px` (tablet), `1200px` (desktop)
- Section spacing classes: `xs`, `s`, `m`, `xxl` (vertical padding tiers)
- Component gap: `grid-2-items--wide-gap` for 2-column layouts

### Buttons

**Primary:**
```css
background-color: #191919;
color: #fffefa;
fill: #fffefa;
font-size: 1rem;
font-weight: 500;
letter-spacing: 0.02rem;
line-height: 150%;
/* Hover: */
background-color: #3f59e4;
```

**Secondary:**
```css
background-color: transparent;
border: 0.09375rem solid #191919;
color: #191919;
padding: 10.5px 2rem;
/* Hover: */
border-color: #3f59e4;
color: #3f59e4;
```

**On dark backgrounds:**
```css
/* Primary inverts: cream bg, dark text */
/* Secondary: cream border, cream text */
/* Hover for both: bg #000000 or #3f59e4 */
```

---

## Component Patterns

Each pattern below shows the semantic structure. Apply the design tokens above for styling.

### 1. Hero Section (Dark, Full-Width Background Image)

```
[Dark background image, responsive: mobile/tablet/desktop variants]
  [Breadcrumb kicker: "Solutions > AI" -- small text, chevron separator]
  [h1: Playfair Display, 52-92px responsive]
  [Subtitle paragraph: Aeonik, font-weight 500]
  [CTA row: Primary button + Secondary button, side by side]
  [Optional: Video thumbnail with circular play button overlay]
```

Key CSS patterns:
- Background image covers the section, swapped per breakpoint via media queries
- Content centered with `max-width` container
- Kicker uses a `<nav>` with `<ul>` breadcrumb, chevron SVG separators
- Play button: circular with backdrop blur, `#191919` at 30% opacity, `#FFFEFA` stroke

### 2. Stats Section (2-Column: Narrative + Grid)

```
[Left column (50%): Playfair h2 + body paragraph]
[Right column (50%): 2x2 grid of stat cards]
  [Each stat: large percentage (data-countup animation) + small description]
```

- Stats use `data-countup` attribute for scroll-triggered animation
- Superscript footnote markers (`<sup>*</sup>`) link to disclaimer section
- Layout: `col-12 col-lg-6` for the two-column split

### 3. Title + Subtitle Block (Section Openers)

```
[Overline: uppercase small text, e.g. "THE UNIFIED IDENTITY PLATFORM"]
[2-column row:]
  [Left: Playfair h2]
  [Right: Body paragraph with optional link]
```

- Overline is `<p class="cmp-title__overline">`, uppercase, small font
- The 2-column layout uses `grid-2-items--wide-gap`
- This pattern introduces every major page section

### 4. Vertical Tabs (Feature Showcase)

```
[Section title block (pattern #3)]
[2-column layout:]
  [Left: Image/animation that swaps per active tab]
  [Right: Vertical tab list]
    [Each tab:]
      [Progress bar (animated fill)]
      [Tab title with expand icon]
      [Tab content: paragraph text]
```

- Tabs auto-advance with a progress bar indicating time remaining
- Image/animation area supports static images, `<video>` with webm+mp4 sources, or Lottie
- Variant: `image-left` or `image-right` layout (the page uses both)
- Background images change per section (developer section vs. security/IT section)

### 5. Cards -- Bento Box Layout

```
[Featured card (large, left/top):]
  [Full image + content overlay]
  [Overline tag: "OVERVIEW"]
  [Playfair heading]
  [Body text]

[Card list (right/bottom, paginated):]
  [3 cards visible at a time]
  [Each card: image + overline tag + heading + body]
  [Pagination: step bars + pause button (desktop), dot nav + arrows (mobile)]
```

- Themes: `snow` (dark cards on light bg) or `cream` (warm toned)
- Overline tags: `OVERVIEW`, `PART 1-7`, `EBOOK`, `BLOG`, `WHITEPAPER`, `WEBINAR`, `VIDEO`, `CHECKLIST`
- Cards are fully clickable (`<a>` wrapping the entire card)
- Desktop pagination auto-rotates; mobile uses swipe/arrows

### 6. Tabbed Resource Section

```
[Section heading: Playfair h2 "Resources"]
[Horizontal tab bar: justified, e.g. "AI security concepts | Navigating risk | ..."]
[Tab panel: 3-column card grid (pattern similar to #5 but without bento)]
  [Each card: image + overline + heading + "Read more" link]
```

- Tab bar uses `cmp-tabs--alignment-justify` for equal-width tabs
- Cards within tabs use the `cream` theme
- Card link style: plain text "Read more" with arrow/underline on hover

### 7. FAQ Section (Sticky Left + Accordion Right)

```
[33% left column (sticky on scroll):]
  [Playfair h2: "Frequently asked questions"]

[66% right column:]
  [Accordion items:]
    [Question header with expand/collapse icon]
    [Answer panel (hidden by default, first item expanded)]
```

- Left heading sticks to viewport on scroll (`position: sticky`)
- Single-expansion mode: opening one accordion closes others
- Layout class: `cmp-faq-ss--layout-33-66`

### 8. CTA Banner (Glass Morphism)

```
[Glass morphism container:]
  [Playfair h2: large, bold question/statement]
  [Body paragraph]
  [Primary button (large)]
```

Glass morphism CSS:
```css
background: rgba(255, 255, 255, 0.2);
border-radius: 16px;
box-shadow: 0px 0px 8px rgba(1, 3, 62, 0.1);
/* Gradient border via pseudo-element: */
&::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 18px;
  padding: 2px;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.1), white);
  mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  mask-composite: exclude;
  opacity: 0.5;
  pointer-events: none;
}
```

- Responsive padding: `2rem` mobile / `3rem` tablet / `4rem` desktop
- Placed over a dark background image for contrast

### 9. Disclaimer / Footnote Area

```
[Divider line above]
[Small text with source citations and links]
[Forward-looking statements disclaimer]
```

- Uses a separate background color (`gray-900`)
- Text is `1rem`, `#fffefa`, `font-weight: 400`, `line-height: 140%`
- Bottom divider line: `0.0625rem` solid `#afaba1`

---

## Implementation Checklist

When building a page with this design system:

- [ ] Load Playfair Display from Typekit (`https://use.typekit.net/zer8olz.css`)
- [ ] Apply `references/design-tokens.css` as the base stylesheet
- [ ] Use dark hero section with responsive background images
- [ ] Every major section opens with the Title + Subtitle block (overline + 2-column h2/body)
- [ ] Buttons follow primary/secondary patterns exactly
- [ ] Stats use countup animation on scroll
- [ ] Cards carry overline category tags
- [ ] CTA banner uses glass morphism with gradient border
- [ ] Test at 3 breakpoints: < 768px, 768-1200px, > 1200px
- [ ] Footer matches Okta's 3-column layout with social icons

---

## When NOT to Use This Skill

- Internal-only tools where brand alignment doesn't matter
- Auth0-branded pages (Auth0 has its own distinct design system)
- Okta Admin Console UI (that uses a different component library)
- Quick prototypes where speed matters more than brand fidelity

## Last Updated
- Date: 2026-04-05
- Source: okta.com/solutions/secure-ai/ (production page, last modified 2026-04-01)
