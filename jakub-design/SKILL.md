---
name: jakub-design
description: Build interfaces following the design engineering philosophy of Jakub Krehel (jakub.kr). Use when building any frontend UI, web component, page, or application where the user wants a polished, minimalist, craft-focused design. Triggers on "jakub design", "jakub style", "clean UI", "minimalist interface", "design engineer style", "polished UI", or when the user invokes /jakub-design. Produces interfaces that feel alive through shadows, motion, OKLCH color, concentric radius, and optical precision. For custom icon generation, invoke /nano-banana-art.
---

# Jakub Design System

Inspired by [jakub.kr](https://jakub.kr/) — a design engineer who cares deeply about craft, quality, and making people feel something through interfaces.

## Philosophy

1. **Shadows over borders** — Never use hard borders in light mode. Use layered box-shadows for depth.
2. **Concentric border radius** — Nested elements must have mathematically correct radius: `outer = inner + padding`.
3. **OKLCH colors** — Use `oklch()` for perceptually uniform palettes. Vary hue, keep lightness/chroma constant.
4. **Motion is meaning** — Animate elements in AND out. Use shared layout animations. Make gestures feel alive.
5. **Optical alignment** — Adjust visually, not just geometrically. Icons in buttons often need ~1px offset.
6. **Radical minimalism** — Near-white bg (#FCFCFC), near-black text (#202020), sparse accent colors.

## Design Tokens

```css
--bg: #FCFCFC;
--text: #202020;
--text-muted: oklch(0.55 0 0);
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 16px;
--spacing-unit: 8px;
--font: 'Inter', system-ui, sans-serif;
--shadow-border: 0px 0px 0px 1px rgba(0,0,0,0.06), 0px 1px 2px -1px rgba(0,0,0,0.06), 0px 2px 4px 0px rgba(0,0,0,0.04);
--shadow-border-hover: 0px 0px 0px 1px rgba(0,0,0,0.08), 0px 1px 2px -1px rgba(0,0,0,0.08), 0px 2px 4px 0px rgba(0,0,0,0.06);
```

## Shadow-Border Pattern

Replace all `border` with layered `box-shadow`. Transition on hover:

```css
.card {
  box-shadow: var(--shadow-border);
  transition: box-shadow 150ms ease;
}
.card:hover {
  box-shadow: var(--shadow-border-hover);
}
```

## Concentric Border Radius

**Rule:** `outerRadius = innerRadius + padding`

```
Container padding 8px, child radius 12px → container radius = 20px
```

## OKLCH Color System

Uniform palettes: fix lightness + chroma, vary hue:

```css
--btn-red:    oklch(0.50 0.16 30);
--btn-green:  oklch(0.50 0.16 150);
--btn-blue:   oklch(0.50 0.16 250);
```

Shade generation — vary lightness only:

```css
--blue-100: oklch(0.95 0.03 250);
--blue-500: oklch(0.60 0.16 250);
--blue-900: oklch(0.25 0.12 250);
```

Gradients: prefer `in oklab` for safe interpolation, `in oklch` for vibrant.

## Buttons

```css
/* Primary: dark, solid */
.btn-primary { background: #202020; color: #FCFCFC; border-radius: 8px; border: none; }

/* Secondary: white, shadow-border */
.btn-secondary { background: #FFF; color: #202020; border-radius: 12px; border: none; box-shadow: var(--shadow-border); }
```

## Motion Guidelines

Use Motion (formerly Framer Motion) for React:
- Wrap conditional elements in `<AnimatePresence>` with `exit` props
- Use `layoutId` for elements transitioning between states
- Prefer `type: "spring"` with `stiffness: 300, damping: 25`
- Animate `pathLength` for SVG drawing effects
- Use `will-change` sparingly — add before animation, remove after

## Icon Generation

When custom icons are needed, invoke `/nano-banana-art`:
- Request minimalist, monochrome line icons
- 1.5px-2px stroke weight, rounded line caps
- 24x24 or 32x32 resolution
- SVG-compatible output

## Detailed References

- **CSS patterns**: See [references/css-patterns.md](references/css-patterns.md) for gradient layering, diamond gradients, clip-path, repeating patterns, animation techniques
- **Component patterns**: See [references/component-patterns.md](references/component-patterns.md) for card stacks, shared layout dialogs, animated inputs, carousels, tab indicators

## Anti-Patterns

- Hard 1px borders in light mode → use shadow-border
- Mismatched radius on nested elements → use concentric formula
- HSL for palettes → use OKLCH
- Animating gradient color stops → animate position/opacity instead
- `will-change` on every element → use sparingly
- Geometric centering without optical adjustment → adjust icons ~1px
- Entry animations without exit animations → always add `exit` prop
- Overly saturated accents → keep chroma restrained

## Tailwind v4 Safety (MANDATORY)

When writing CSS for Tailwind v4 projects:

1. **All CSS resets inside `@layer base { }`** — bare `* { margin: 0 }` kills ALL spacing utilities
2. **Custom component classes inside `@layer components { }`** — `.card`, `.badge`, etc.
3. **Hardcoded values in custom classes** — `var()` refs to `@theme` may not resolve in build
4. **Inline styles for layout-critical fixed values** — `ml-[240px]` can fail silently, use `style={{ marginLeft: 240 }}`
5. **Correct structure:** `@import "tailwindcss"` → `@theme {}` → `@layer base {}` → `@layer components {}`
