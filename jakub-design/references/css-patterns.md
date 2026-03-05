# CSS Patterns Reference

## Gradient Layering with Blend Modes

Layer multiple gradients with `background-blend-mode` for rich, unique effects:

```css
.layered-gradient {
  background:
    linear-gradient(in oklch 135deg,
      oklch(0.75 0.18 280),
      oklch(0.8 0.15 80),
      oklch(0.75 0.18 320)),
    conic-gradient(in oklch from 180deg,
      oklch(0.7 0.12 200 / 0.3),
      oklch(0.7 0.12 340 / 0.3),
      oklch(0.7 0.12 200 / 0.3));
  background-blend-mode: overlay, color-dodge;
}
```

## Diamond Gradient (4 layered linear gradients)

Figma-style diamond gradient, not natively available in CSS:

```css
.diamond-gradient {
  background:
    linear-gradient(to bottom right, #fff 0%, #999 50%) bottom right / 50% 50% no-repeat,
    linear-gradient(to bottom left, #fff 0%, #999 50%) bottom left / 50% 50% no-repeat,
    linear-gradient(to top left, #fff 0%, #999 50%) top left / 50% 50% no-repeat,
    linear-gradient(to top right, #fff 0%, #999 50%) top right / 50% 50% no-repeat;
}
```

## Color Hints for Gradient Midpoint Control

Shift the blend midpoint without adding new color stops:

```css
/* Default: midpoint at 50% */
background: linear-gradient(to right, red, blue);

/* Shifted: midpoint at 30% — red transitions faster */
background: linear-gradient(to right, red, 30%, blue);

/* Multiple hints */
background: linear-gradient(to right, red, 30%, blue, 70%, green);
```

## Repeating Gradient Textures

```css
/* Striped pattern */
background: repeating-linear-gradient(
  45deg,
  #000 0 10px,
  #fff 10px 20px
);

/* Radial repeating pattern */
background: repeating-conic-gradient(
  from 0deg,
  #000 0deg 20deg,
  #fff 20deg 40deg
);
```

## Gradient Animation (Animate Position, Not Stops)

```css
.animated-gradient {
  background: linear-gradient(135deg, oklch(0.7 0.15 250), oklch(0.7 0.15 30));
  background-size: 200% 200%;
  animation: gradientShift 3s ease infinite;
}
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

## Shadow-Border Variants

```css
/* Subtle (default) */
--shadow-subtle: 0px 0px 0px 1px rgba(0,0,0,0.06),
                 0px 1px 2px -1px rgba(0,0,0,0.06),
                 0px 2px 4px 0px rgba(0,0,0,0.04);

/* Medium (focused/active states) */
--shadow-medium: 0px 0px 0px 1px rgba(0,0,0,0.08),
                 0px 2px 4px -1px rgba(0,0,0,0.08),
                 0px 4px 8px 0px rgba(0,0,0,0.06);

/* Elevated (popovers, dropdowns) */
--shadow-elevated: 0px 0px 0px 1px rgba(0,0,0,0.08),
                   0px 4px 8px -2px rgba(0,0,0,0.1),
                   0px 8px 16px 0px rgba(0,0,0,0.08);
```

## OKLCH Fallback Pattern

```css
@layer base {
  :root {
    --color-gray-100: #fcfcfc;
    --color-gray-200: #fafafa;
    --color-gray-300: #f4f4f4;

    @supports (color: oklch(0 0 0)) {
      --color-gray-100: oklch(0.991 0 0);
      --color-gray-200: oklch(0.982 0 0);
      --color-gray-300: oklch(0.955 0 0);
    }
  }
}
```

## Tailwind 4 OKLCH Gradients

```html
<div class="bg-linear-to-r/oklch from-red-500 to-blue-500" />
```

## Clip-Path Button Hold Effect

Use `clip-path` to reveal/hide button states on interaction:

```css
.clip-btn {
  position: relative;
  overflow: hidden;
}
.clip-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: oklch(0.3 0.1 250);
  clip-path: circle(0% at var(--x, 50%) var(--y, 50%));
  transition: clip-path 300ms ease;
}
.clip-btn:active::after {
  clip-path: circle(150% at var(--x, 50%) var(--y, 50%));
}
```

## will-change Best Practice

```css
/* Only add before animation starts */
.will-animate {
  will-change: transform, opacity;
}
/* Remove after animation completes via JS */
element.addEventListener('transitionend', () => {
  element.style.willChange = 'auto';
});
```
