# Gemini Image Generation — Prompt Engineering Guide

## Prompt Structure

Effective prompts follow this pattern:

```
[Subject] + [Style/Medium] + [Composition] + [Lighting/Mood] + [Color Palette] + [Quality Modifiers]
```

## Style Keywords

| Category | Keywords |
|----------|----------|
| **Photorealistic** | photorealistic, DSLR photo, professional photography, 8K, sharp focus |
| **Illustration** | vector illustration, flat design, hand-drawn, watercolor, ink sketch |
| **Corporate/UI** | clean, minimal, professional, corporate, modern UI, flat icon |
| **Luxury/Premium** | elegant, refined, luxury, premium, sophisticated, haute couture |
| **Abstract** | abstract, geometric, gradient mesh, fluid shapes, generative art |
| **SaaS/Editorial** | premium SaaS, clean modern, soft gradients, light background, editorial |

## Web UI Asset Presets

### Hero Backgrounds (Full-width banner images)
```
Prompt: "Premium SaaS hero background, soft light refractions through layered
translucent [PRIMARY_COLOR] surfaces, clean modern abstract, horizontal wide
format, light background fading to white at edges, no text, no icons, macro
photography style"
Aspect: 16:9
Size: 2K
```

### Section Backgrounds (Subtle textures behind content sections)
```
Prompt: "Extremely subtle abstract texture, very faint [COLOR] geometric
pattern dissolving into white, premium SaaS style, barely visible, clean
modern, no text, horizontal format, macro photography of frosted glass"
Aspect: 16:9
Size: 1K
```

### Card Header Images (Module/feature cards)
```
Prompt: "Abstract premium card illustration, flowing [COLOR] light refractions
with [METAPHOR] forms, soft gradients, clean modern SaaS style, horizontal
card composition, no text, no icons, light background, macro photography
of [MATERIAL]"
Aspect: 2:1
Size: 1K
```

### Wide Banners (Page headers, module index banners)
```
Prompt: "Wide panoramic abstract premium banner, [COLOR] [PATTERN_DESCRIPTION],
soft gradients, clean modern SaaS style, no text, no icons, light background,
ultra-wide horizontal composition"
Aspect: 4:1
Size: 2K
```

### Small Icons (Sidebar, navigation, features)
```
Prompt: "Tiny minimalist abstract icon, soft [COLOR] gradient, simple geometric
[SHAPE] form, clean modern premium, no text, centered on white background,
product photography"
Aspect: 1:1
Size: 512px
```

### Lesson/Page Header Strips (Thin atmospheric banners)
```
Prompt: "Thin atmospheric horizontal banner, soft [COLOR] [VISUAL_ELEMENT],
abstract, premium SaaS style, no text, macro photography of [MATERIAL]"
Aspect: 8:1
Size: 1K
```

### Navigation Thumbnails (Small preview images)
```
Prompt: "Small thumbnail, soft [COLOR] [VISUAL], clean modern, no text,
product photography of [MATERIAL], square crop"
Aspect: 1:1
Size: 512px
```

### Value Proposition Icons (Feature/benefit icons)
```
Prompt: "Premium abstract icon, [VISUAL_METAPHOR], soft [COLOR] gradient
background fading to white, 3D glass morphism style, clean modern, no text,
centered composition, product photography"
Aspect: 1:1
Size: 1K
```

### Reference Card Headers (Documentation/resource cards)
```
Prompt: "Premium card header illustration, abstract [CONCEPTUAL_FORM],
soft neutral gradient, clean modern SaaS style, no text, horizontal composition,
macro photography of [MATERIAL]"
Aspect: 2:1
Size: 1K
```

### Interactive Exercise Textures (Subtle card backgrounds)
```
Prompt: "Extremely subtle abstract texture strip, barely visible soft [COLOR]
gradient pattern, premium SaaS background texture, very faint, no text,
horizontal thin band, macro photography of frosted [COLOR] glass surface"
Aspect: 8:1
Size: 1K
```

## Building a Consistent Vercel Site Manifest

When generating assets for a full website, follow this workflow:

1. **Define your color palette** — Pick 2-5 accent colors with hex codes
2. **Choose a visual material** — Pick one material family for consistency (e.g., "crystal", "glass", "marble", "light refractions")
3. **Write a base style prefix** — Share across all prompts: `"premium SaaS, clean, abstract, soft gradients, light background, no text"`
4. **Generate by category** — Use the presets above, substituting your colors and material
5. **Module/section colors** — Give each section its own accent color for visual hierarchy
6. **Dark mode consideration** — Use CSS `filter: brightness(0.7) saturate(0.9)` for dark mode instead of generating separate images

### Example Manifest Structure for a Vercel Site

```json
[
  {"prompt": "BASE_STYLE + hero-specific details", "filename": "hero/hero-bg.png"},
  {"prompt": "BASE_STYLE + section bg details", "filename": "hero/section-bg.png"},
  {"prompt": "BASE_STYLE + module1 card with MODULE1_COLOR", "filename": "modules/module1-card.png"},
  {"prompt": "BASE_STYLE + module2 card with MODULE2_COLOR", "filename": "modules/module2-card.png"},
  {"prompt": "BASE_STYLE + page banner for MODULE1_COLOR", "filename": "banners/module1-banner.png"},
  {"prompt": "BASE_STYLE + icon for sidebar", "filename": "sidebar/module1.png"},
  {"prompt": "BASE_STYLE + nav thumbnail", "filename": "nav/page1.png"}
]
```

## Avoiding Safety Filter Rejections

Gemini's safety classifier blocks prompts it flags as ambiguous or potentially problematic. The pattern: **concrete photographic descriptions succeed; abstract conceptual ones fail.**

### What Gets Blocked

- Vague texture descriptions: "moody dark surface", "abstract texture"
- Conceptual-only prompts: "gold metallic effect", "luxury feel"
- Ambiguous subjects without physical grounding

### How to Fix Blocked Prompts

1. **Describe what the camera sees** — "Close-up photograph of dark charcoal paper" not "dark texture"
2. **Name physical materials** — "handmade paper", "polished brass surface", "ink on paper"
3. **Add photographic context** — "macro photography", "product photography", "DSLR close-up"
4. **Use specific color names** — "cream colored", "dark charcoal" not just "warm" or "dark"
5. **Always pair adjectives with nouns** — "elegant serif calligraphy style" not just "elegant"

### Before/After Examples

```
BLOCKED: "seamless tileable vellum texture, warm cream undertones"
WORKS:   "Close-up photograph of high quality cream colored handmade paper with visible subtle fiber texture, warm ivory tones, soft natural light"

BLOCKED: "abstract dark moody surface texture"
WORKS:   "Close-up photograph of dark charcoal colored handmade paper texture, near-black surface with visible subtle fiber grain, macro photography"

BLOCKED: "gold metallic circle button"
WORKS:   "Brushed gold metallic circle on white background, warm polished brass surface texture, subtle radial polish marks, clean product photography"
```

## Don't Use Gemini For These — Use Programmatic Fallback

The script auto-detects these keywords and generates with Pillow instead of calling the API:

| Need | Include This in Your Prompt | What Happens |
|---|---|---|
| Noise/grain overlay | "noise texture", "grain texture", "film grain", "grainy", "digital noise" | Generates random RGBA noise at appropriate opacity |
| Solid color fill | "solid color", "solid background", "plain background", "uniform background" + hex code | Generates single-color image |
| Simple gradient | "simple gradient", "linear gradient background", "color gradient", "vertical gradient" + 2 hex codes | Generates two-color vertical gradient |

If you need these, just include the keywords naturally in your prompt and the scripts handle it automatically.

**For anything else Gemini can't do well** (exact text, transparent backgrounds, pixel-perfect patterns), generate a placeholder with Gemini and post-process with Pillow, or create the asset directly in code (SVG, CSS gradients, Canvas).

**Important:** Gemini always generates opaque images. Do NOT specify "transparent background" in prompts — it won't work. Use "on white background" or "on [color] background" instead. If you need transparency, remove the background in post-processing with Pillow.

## Tips

1. **Be specific about colors** — Gemini responds well to hex codes and named colors
2. **Specify negative space** — "with ample white space", "isolated on white background"
3. **Include technical specs** — "sharp edges", "no blur", "high contrast"
4. **For icons** — always specify "on white background" (NOT transparent — Gemini can't do transparent)
5. **For patterns** — specify "seamless", "tileable", "repeating pattern"
6. **For UI elements** — reference specific design systems: "Material Design", "Apple HIG"
7. **Iterate** — Use the `--input` flag to edit/refine generated images
8. **For textures/backgrounds** — always frame as "photograph of [physical material]" not abstract descriptions
9. **For Vercel sites** — use the Web UI Asset Presets section above for consistent, high-quality results
