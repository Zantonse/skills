# Gemini Image Generation — Prompt Engineering Guide

## The #1 Rule: Natural Language Over Tag Soup

Gemini's image models understand intent, physics, and composition. They reward clear creative direction over keyword lists.

**BAD (tag soup):** `"dog, park, sunset, 4k, realistic, cinematic"`

**GOOD (creative direction):** `"A golden retriever bounding through a sun-dappled park at golden hour, shot from a low angle with shallow depth of field"`

Write as if briefing a human photographer or artist. Describe what the camera sees.

## Prompt Structure

Build prompts from these elements (not all required — use what's relevant):

```
[Style/medium] of [specific subject with details] in [setting/environment],
[action or pose], [lighting description], [mood/atmosphere],
[camera angle/composition], [additional details: texture, color palette, materiality].
[Purpose context if relevant.]
```

## Key Vocabularies

### Camera Language
Use cinematic terms the model understands:
- **Framing:** wide establishing shot, medium close-up, extreme close-up, over-the-shoulder, bird's eye view, worm's eye view, Dutch angle
- **Lens:** shallow depth of field, bokeh, macro, telephoto compression, fisheye distortion, tilt-shift
- **Film:** 35mm film grain, Kodak Portra tones, Fuji Velvia saturation, cross-processed

### Lighting
Be specific about how light behaves:
- **Direction:** backlit with rim light, soft window light from the left, dramatic side-lighting
- **Named techniques:** Rembrandt lighting, butterfly lighting, chiaroscuro, clamshell lighting
- **Quality:** soft diffused, harsh directional, golden hour warmth, cool blue hour, neon-lit
- **Atmospheric:** volumetric fog with light rays, dappled light through leaves, studio strobes with softbox

### Materials and Texture
The model produces better results when you name physical materials:
- **Metals:** brushed aluminum, polished brass, hammered copper, matte black anodized
- **Fabrics:** hand-knit wool, soft velvet, crisp linen, weathered leather, raw silk
- **Surfaces:** cracked clay, translucent glass, wet stone, oxidized patina, frosted acrylic
- **Natural:** sun-bleached driftwood, moss-covered bark, volcanic rock, sea-polished pebbles

### Color Direction
Guide the palette rather than specifying hex codes (for hex, see Web UI section):
- **Palettes:** muted earth tones, high-contrast complementary, monochromatic blue, warm terracotta and sage
- **Techniques:** desaturated pastels, rich jewel tones, black and white with selective color
- **Mood through color:** warm amber candlelight glow, cool steel-blue twilight, vibrant tropical sunset

## Specificity Matters

Vague subjects produce generic images. Add materiality, context, and detail:

| Vague | Specific |
|-------|---------|
| "a woman" | "a sophisticated elderly woman wearing a vintage Chanel-style tweed suit" |
| "a building" | "a brutalist concrete apartment block with laundry lines strung between balconies" |
| "a coffee cup" | "a handmade ceramic coffee cup with an uneven clay glaze, steam curling upward" |

## Context About Purpose

Mentioning the use case helps the model infer appropriate composition, lighting, and quality:
- "Create a hero image for a premium coffee brand's website" — infers professional lighting, editorial framing
- "Design a poster for a jazz concert" — infers bold typography, moody atmosphere
- "Make a social media thumbnail for a cooking channel" — infers bright, appetizing, centered composition

## Edit, Don't Re-Roll

When a generated image is mostly correct, request specific conversational changes rather than starting over:
- "Change the sunny day to a rainy night"
- "Remove the person in the background and add a potted plant"
- "Make the lighting warmer and add more shadow on the left"

The model adjusts lighting, reflections, and physics automatically when editing.

## Reference Images & Consistency

Gemini supports multi-image context for visual consistency:
- **Up to 5 consistent characters** per workflow
- **Up to 14 consistent objects** per workflow
- Instruct with: "Use the uploaded image as a strict style reference"
- For character consistency: "Keep facial features exactly the same as the reference"
- For storyboarding: "The identity and attire of all characters must stay consistent throughout"

## Text in Images

Gemini has strong text rendering. Always put exact text in quotation marks:
- `with the text "MIDNIGHT REVERIE" in bold art deco typography`
- Specify style: "bold sans-serif," "handwritten script," "retro neon sign"
- For localization: "Translate the text in this image to Japanese"

Note: exact text rendering is improved but not pixel-perfect. For production text, use SVG/CSS.

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Tag soup | `"dog, park, sunset, 4k"` — keyword lists lack creative direction | Write natural sentences describing the scene |
| Vague subjects | "a person" or "a building" — too generic | Add specific details, materials, context |
| Missing mood/lighting | Dramatically affects output quality | Always include lighting and atmosphere |
| No purpose context | Model can't infer appropriate style | Mention the use case when relevant |
| Over-prompting | Contradictory or excessive details confuse the model | Keep prompts coherent and focused |
| Abstract adjectives alone | "elegant" or "luxurious" without a noun | Pair with specifics: "elegant serif calligraphy" |

## Example Prompts

### Product Photography
> A flat lay of artisanal coffee beans spilling from a matte black ceramic cup onto a weathered oak table, soft directional window light from the upper left, warm earth tones with deep shadows, shot from directly above, styled for a premium coffee brand's Instagram feed.

### Portrait
> A cinematic medium close-up portrait of a jazz musician mid-performance, eyes closed, sweat glistening under warm amber stage lighting, shallow depth of field with bokeh from string lights in the background, shot on what looks like 35mm film with natural grain.

### Text-Heavy Design
> A vintage-style concert poster with the text "MIDNIGHT REVERIE" in bold art deco typography at the top, a silhouette of a saxophone player against a deep indigo night sky with a full moon, "Live at The Blue Note — March 15, 2026" in smaller elegant serif type at the bottom, gold and navy color palette.

### Fantasy Illustration
> A lush watercolor illustration of a hidden forest library, towering bookshelves made from living trees with glowing mushrooms as reading lamps, a cozy armchair draped in moss-green velvet, shafts of golden sunlight filtering through the canopy above, whimsical and enchanting atmosphere.

### Icon/UI Asset
> A minimalist 3D-rendered shield icon, polished gold surface with subtle reflections, clean geometric form, soft gradient shadow on white background, product photography lighting, centered composition.

---

## Web UI Asset Presets

For generating consistent assets for Vercel/Next.js sites.

### Workflow
1. **Define your color palette** — Pick 2-5 accent colors with hex codes
2. **Choose a visual material** — One material family for consistency (crystal, glass, marble, light refractions)
3. **Write a base style prefix** — Share across all prompts
4. **Generate by category** — Use presets below, substituting your colors and material

### Hero Backgrounds (16:9, 2K)
```
A premium SaaS hero background with soft light refractions through layered
translucent [PRIMARY_COLOR] surfaces, clean modern abstract composition,
wide horizontal format, light background fading to white at edges, macro
photography style, no text, no icons
```

### Section Backgrounds (16:9, 1K)
```
An extremely subtle abstract texture, very faint [COLOR] geometric pattern
dissolving into white, premium SaaS style, barely visible, clean modern,
horizontal format, macro photography of frosted glass surface, no text
```

### Card Headers (2:1, 1K)
```
An abstract premium card illustration with flowing [COLOR] light refractions
and [METAPHOR] forms, soft gradients, clean modern SaaS style, horizontal
card composition, light background, macro photography of [MATERIAL], no text
```

### Wide Banners (4:1, 2K)
```
A wide panoramic abstract premium banner with [COLOR] [PATTERN_DESCRIPTION],
soft gradients, clean modern SaaS style, ultra-wide horizontal composition,
light background, no text, no icons
```

### Icons (1:1, 512px)
```
A tiny minimalist abstract icon, soft [COLOR] gradient forming a simple
geometric [SHAPE], clean modern premium style, centered on white background,
product photography lighting, no text
```

### Manifest Example
```json
[
  {"prompt": "A premium SaaS hero background...", "filename": "hero-bg.png", "aspect": "16:9", "size": "2K"},
  {"prompt": "A minimalist shield icon...", "filename": "icon-security.png", "aspect": "1:1", "size": "1K"}
]
```

---

## Avoiding Safety Filter Rejections

Gemini's safety classifier blocks prompts it considers ambiguous. **Concrete, photographic descriptions succeed; abstract conceptual ones fail.**

### Rules
1. **Describe what the camera sees** — "Close-up photograph of paper" not "paper texture"
2. **Name physical materials** — "handmade paper", "brass surface", "ink on paper"
3. **Add photographic context** — "macro photography", "product photography", "close-up"
4. **Use specific color names** — "cream colored", "dark charcoal" not just "warm" or "dark"
5. **Pair adjectives with nouns** — "elegant serif calligraphy" not just "elegant"

### Before/After
```
BLOCKED: "seamless tileable vellum texture"
WORKS:   "Close-up photograph of cream colored handmade paper with visible fiber texture, warm ivory tones, soft natural light"

BLOCKED: "gold metallic circle button"
WORKS:   "Brushed gold metallic circle on white background, warm polished brass surface, subtle radial polish marks, clean product photography"
```

---

## Programmatic Fallback (Auto-Detected)

These prompt types are auto-generated with Pillow instead of calling the API:

| Need | Keywords to Include | What Generates |
|------|-------------------|----------------|
| Noise/grain overlay | "noise texture", "film grain", "digital noise" | Random RGBA noise |
| Solid color fill | "solid color", "solid background" + hex code | Single-color image |
| Simple gradient | "simple gradient", "linear gradient" + 2 hex codes | Two-color vertical gradient |

---

## Known Limitations

1. **Transparent backgrounds** — Gemini always generates opaque. Use "on white background" then remove in post.
2. **Pixel-perfect text** — Improved but not production-ready. Use SVG/CSS for final text.
3. **Seamless tileable patterns** — Hit-or-miss. Use CSS patterns for reliability.
4. **UI mockups with precise layouts** — Better to code in HTML/CSS.
5. **Very abstract concepts** — "the feeling of growth" fails; "golden crystalline prisms ascending" works.
