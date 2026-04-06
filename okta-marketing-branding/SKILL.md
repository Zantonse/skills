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

Source: okta.com (6 production pages: homepage, products, pricing, customers,
company/blog, industry/solutions -- scraped April 2026)

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
| Hero / section titles | `"playfair-display", serif` | 400 | `font-variant-numeric: lining-nums proportional-nums; font-feature-settings: "liga" 1` -- applied via `.okta-heading--display` |
| Base headings (h1-h3) | `Aeonik, "Helvetica Neue", sans-serif` | 400-500 | Default heading stack from clientlib-site CSS |
| Body, UI, buttons, overlines | `Aeonik, "Helvetica Neue", sans-serif` | 400-500 | Okta's custom sans-serif. Fall back to Helvetica Neue or system sans. |

Font source: `https://use.typekit.net/zer8olz.css` (Adobe Fonts / Typekit).

**Responsive heading scale (base -- Aeonik):**
- h1: `2rem` mobile / `2.5rem` tablet / `3.5rem` desktop, weight 400, letter-spacing `-0.02rem`, line-height 114-136%
- h2: `1.5rem` mobile / `1.75rem` tablet / `2rem` desktop, weight 400, letter-spacing `-0.01rem`, line-height 125-133%
- h3: `1.25rem` mobile / `1.5rem` tablet+, weight 500, letter-spacing `0` to `-0.005rem`, line-height 135-140%

**Hero Playfair override (`.okta-heading--display`):**
- 52px mobile / 72px tablet / 92px desktop

**Font size scale (production):** `.625rem` `.75rem` `.875rem` `1rem` `1.25rem` `1.5rem` `1.75rem` `2rem` `2.5rem` `2.75rem` `3rem` `3.5rem` `4rem` `4.5rem` `5rem` `6rem` `7rem` `8rem`

### Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--theme-ui-colors-primary` | `#3f59e4` | Blue accent, hover states, interactive elements |
| `--theme-ui-colors-secondary` | `#4cb7a3` | Teal accent |
| `--theme-ui-colors-tertiary` | `#4016a0` | Purple accent |
| `--theme-ui-colors-gray900` | `#191919` | Text, primary button bg, dark UI |
| `--theme-ui-colors-gray000` | `#fffefa` | Page background, text on dark |
| `--okta-glass-bg` | `rgba(255, 255, 255, 0.2)` | Glass morphism backgrounds |
| `--okta-glass-shadow` | `0px 0px 8px rgba(1, 3, 62, 0.1)` | Glass morphism box-shadow |
| `--okta-shadow-heavy` | `0 20px 40px rgba(0, 0, 0, 0.5)` | Hero overlay shadows |

Full color token set (including all gray steps, button states, link colors, content-type tags)
is in `references/design-tokens.css` under `/* theme-ui-colors */`.

### Spacing & Layout

- Grid container: `padding: 0 1rem` (mobile) / `0 4rem` (tablet) / `margin: 0 auto` `max-width: 90rem` (1440px desktop)
- **Note:** max-width is `90rem` (1440px), not 84rem as originally extracted
- Blue accent line: `.grid-container:before { border-top: 4px solid #3f59e4 }` -- used as section separators
- Breakpoints: `768px` (tablet), `1200px` (desktop)
- Section spacing classes: `xs` `s` `m` `xxl` (vertical padding tiers)
- CSS class naming: BEM with `cmp-` prefix (`cmp-hero`, `cmp-button`, `cmp-cards`)
  - Style system modifiers: `cmp-*-ss--` (e.g., `cmp-hero-ss--centered`, `cmp-cards-ss--snow`)
  - Theme classes: `dark-theme`, `alternate-theme`, `none-theme`
  - Section containers: `sectioncontent`, `sectionContainerEnhanced`
  - Size modifiers: `--title-1` through `--title-3`, `--body-1` through `--body-3`

### Buttons

**Primary:**
```css
background-color: #191919;
color: #fff;
font-size: 1rem; font-weight: 500; letter-spacing: .02rem; line-height: 150%;
/* Hover: background-color #3f59e4 */
/* Active: background-color #1a31a9 */
/* Transition: background-color 0.3s ease-out, border-color 0.3s ease-out, color 0.3s ease-out */
```

**Secondary:**
```css
background-color: transparent; border: 0.09375rem solid #191919; color: #191919;
/* Hover: border-color #3f59e4; color #3f59e4 */
```

---

## Component Patterns

Each pattern shows the semantic structure. CSS classes are in `references/design-tokens.css`.

### 1. Hero Section (Dark, Full-Width Background Image)

```
[Dark background image, responsive: mobile/tablet/desktop variants]
  [Breadcrumb kicker: "Solutions > AI" -- small text, chevron separator]
  [h1 (.okta-heading--display): Playfair Display, 52-92px responsive]
  [Subtitle paragraph: Aeonik, font-weight 500]
  [CTA row: Primary button + Secondary button, side by side]
  [Optional: Video thumbnail with circular play button overlay]
```

- Background image covers section, swapped per breakpoint via media queries
- Kicker uses `<nav>` with `<ul>` breadcrumb, chevron SVG separators
- Play button: `.okta-play-btn` -- circular, `#191919` at 30% opacity, `#FFFEFA` border + triangle

### 2. Stats Section (2-Column: Narrative + Grid)

```
[Left column (50%): Playfair h2 + body paragraph]
[Right column (50%): 2x2 grid of stat cards]
  [Each stat: large number (data-countup animation) + small description]
```

- Stats use `data-countup` attribute for scroll-triggered animation
- Superscript footnote markers (`<sup>*</sup>`) link to disclaimer section

### 3. Title + Subtitle Block (Section Openers)

```
[Overline: uppercase small text, e.g. "THE UNIFIED IDENTITY PLATFORM"]
[2-column row:]
  [Left: Playfair h2]
  [Right: Body paragraph with optional link]
```

- Overline: `<p class="cmp-title__overline">`, uppercase, 0.75rem
- This pattern introduces every major page section

### 4. Vertical Tabs (Feature Showcase)

```
[Section title block (pattern #3)]
[2-column layout:]
  [Left: Image/animation swaps per active tab]
  [Right: Vertical tab list]
    [Each tab: Progress bar (animated fill) + title + body text]
```

- Tabs auto-advance with progress bar indicating time remaining (8s transition)
- Image area supports static images, `<video>` webm+mp4, or Lottie
- Variant: `image-left` or `image-right`

### 5. Cards -- Bento Box Layout

```
[Featured card (large): full image + content overlay + overline tag + heading + body]
[Card list (right/bottom, paginated): 3 cards visible at a time]
  [Each card: image + overline tag + heading + body]
  [Pagination: step bars + pause button (desktop), dot nav + arrows (mobile)]
```

- Themes: `snow` (dark) or `cream` (warm toned)
- Overline tags: `OVERVIEW` `PART 1-7` `EBOOK` `BLOG` `WHITEPAPER` `WEBINAR` `VIDEO` `CHECKLIST`
- Cards are fully clickable (`<a>` wrapping entire card)

### 6. Tabbed Resource Section

```
[Section heading: Playfair h2]
[Horizontal tab bar: justified, e.g. "AI security concepts | Navigating risk | ..."]
[Tab panel: 3-column card grid]
  [Each card: image + overline + heading + "Read more" link]
```

### 7. FAQ Section (Sticky Left + Accordion Right)

```
[33% left column (sticky): Playfair h2 "Frequently asked questions"]
[66% right column: Accordion items]
  [Question header + answer panel (first item expanded by default)]
```

- Layout class: `cmp-faq-ss--layout-33-66`
- Single-expansion mode: opening one closes others

### 8. CTA Banner (Glass Morphism)

```
[Glass morphism container: rgba(255,255,255,0.2) bg + gradient border]
  [Playfair h2]
  [Body paragraph]
  [Primary button (large)]
```

See `references/design-tokens.css` `.okta-glass-banner` for full CSS including gradient border pseudo-element.

### 9. Disclaimer / Footnote Area

```
[Divider line above]
[Small text with source citations and links]
[Forward-looking statements disclaimer]
```

- Font: 0.875rem, line-height 1.5, opacity 0.7

### 10. Logo Bar

```
[Small social proof heading: "We help secure workforces worldwide" + "View all" link]
[Horizontal row of partner/customer logos]
```

- Class: `cmp-logo-bar` with `--carbon` theme (grayscale/monochrome logos via `filter: grayscale(100%)`)
- Logos are lazy-loaded SVGs

### 11. Product Showcase Tabs (Horizontal + Video)

```
[Horizontal ol[role=tablist]: 5-7 tabs]
[Each tab panel: Vidyard video thumbnail + play button overlay + title + body + CTA link]
[Mobile: collapses to <select> dropdown]
```

- Different from vertical tabs (pattern #4): this is a horizontal `ol` tab bar
- Play button uses `.okta-play-btn` with `#FFFEFA` triangle fill

### 12. Customer Carousel (Full-Width Testimonial Slider)

```
[Full-bleed background image per slide (height: 520px desktop)]
[Content: customer logo + blockquote quote + name + title + "Read their story" link]
[Navigation: arrow characters + dot wayfinding buttons]
```

### 13. Pricing Cards

```
[4-tier horizontal row: Starter / Essentials / Professional / Enterprise]
[Each card: tier name + price ($/user/month) OR "Inquire for pricing"]
[Feature list: "Everything in [tier], plus:" inheritance pattern]
[Comparison table: section headers + Add-on labels + footnote symbols *, **, †, ‡]
```

- "Most Popular" badge on Essentials tier
- "Early Access" inline badge on AI add-ons
- Annual pricing only (no monthly/annual toggle)

### 14. Customer Story Cards

```
[Filter sidebar: Products / Industries / Product Features (multi-select)]
[Grid: 3 columns, 12 cards per page, numbered pagination]
[Each card (full anchor): company name + one-line outcome headline]
[Card image: 624x270px (2.31:1 very wide landscape)]
```

- Sort options: Featured / Company / Latest

### 15. Leadership Cards

```
[H2: "Executive Team" (14 people) / "Board of Directors" (10 people)]
[Each card: headshot photo + bold name + full title + "Learn more" link]
[Grid: 4 columns desktop, 3 tablet, 2 mobile]
```

### 16. Blog Cards

```
[Featured: category + date + title + excerpt + full author block (photo + name + role + bio)]
[Listing: category + date + bold title + "Learn more" link (no author, no excerpt)]
[Date format: "16 Mar 2026" listing / "16 March 2026" detail page]
[Reading time: "~ N Minutes" (tilde prefix)]
[Category pills: 7 horizontal tabs (AI, Product Innovation, Identity Security, etc.)]
```

### 17. Solution Category Cards (Text-Only)

```
[H2 section headers: Identity type (6 cards) / Industry (9 cards) / Goals (3 cards)]
[Each card (full link): bold title + 1-2 sentence description + "Explore [title] solutions" CTA]
```

- No images, no icons in body cards

### 18. Industry Page Section Rhythm

Standard section ordering on industry/solutions pages:
1. Dark hero (navy/blue gradient, white text)
2. Stats bar (3 metrics, dark background)
3. Tabbed value prop (3 accordion tabs)
4. Sub-industry tabs (e.g. Banking/FinTech with customer logos)
5. Product carousel (numbered tabs + screenshots)
6. New release grid (3-up text cards)
7. Two-tab feature split
8. Pull quote testimonial
9. Platform two-up (Okta + Auth0 cards)
10. Resource cards (4-up with category tags)
11. Final dark CTA

---

## Additional CSS Patterns

### Transitions
```css
/* Standard visibility */
transition: opacity 0.3s, visibility 0.3s;

/* Buttons */
transition: background-color 0.3s ease-out, border-color 0.3s ease-out, color 0.3s ease-out;
```

### Box Shadows
```css
/* Glass morphism */
box-shadow: 0px 0px 8px rgba(1, 3, 62, 0.1);

/* Heavy (hero overlays) */
box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
```

### Content-Type Color Coding

Resource category tags use these colors (also in `references/design-tokens.css`):
| Type | Color |
|------|-------|
| Whitepaper | `#cfb1c1` |
| Datasheet | `#8d6e97` |
| Analyst Research | `#fad28c` |
| Infographic | `#f0bf87` |
| Video | `#abd5d6` |
| Demo | `#a0dcc3` |
| Webinar | `#2d8c9e` |

---

## Implementation Checklist

When building a page with this design system:

- [ ] Load Playfair Display from Typekit (`https://use.typekit.net/zer8olz.css`)
- [ ] Apply `references/design-tokens.css` as the base stylesheet
- [ ] Use dark hero section with responsive background images
- [ ] Hero titles use `.okta-heading--display` (Playfair), not base h1 (Aeonik)
- [ ] Max-width container is `90rem` (1440px), not 84rem
- [ ] Every major section opens with the Title + Subtitle block (overline + 2-column h2/body)
- [ ] Buttons follow primary/secondary patterns with `0.3s ease-out` transitions
- [ ] Stats use countup animation on scroll
- [ ] Cards carry overline category tags
- [ ] CTA banner uses glass morphism with gradient border pseudo-element
- [ ] Test at 3 breakpoints: < 768px, 768-1200px, > 1200px
- [ ] Footer matches Okta's 3-column layout with social icons

---

## When NOT to Use This Skill

- Internal-only tools where brand alignment doesn't matter
- Auth0-branded pages (Auth0 has its own distinct design system)
- Okta Admin Console UI (that uses a different component library)
- Quick prototypes where speed matters more than brand fidelity

## Last Updated
- Date: 2026-04-06
- Source: okta.com (6 pages: homepage, products, pricing, customers, company/blog, industry/solutions)
- Previous source was single page (okta.com/solutions/secure-ai/). Max-width corrected from 84rem to 90rem.
