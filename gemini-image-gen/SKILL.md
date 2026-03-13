---
name: gemini-image-gen
description: "Generate and edit images using Google Gemini's native image generation (Nano Banana) via LiteLLM proxy or direct google-genai SDK. Use when the user asks to: (1) generate images, icons, backgrounds, illustrations, or visual assets, (2) create branded visuals or design assets for a project, (3) edit or modify existing images with AI, (4) batch-generate multiple assets from prompts. Triggers on: 'generate image', 'create icon', 'make a background', 'design visual', 'AI image', 'Gemini image', or any request to produce visual assets with AI."
---

# Gemini Image Generation

Generate images, icons, backgrounds, and visual assets using Google Gemini's native image generation.

## Prerequisites — Two Modes

**Option A: LiteLLM Proxy (recommended if available)**
```bash
export LITELLM_API_KEY="sk-..."
export LITELLM_BASE_URL="https://llm.atko.ai"
```
Uses the OpenAI-compatible `/v1/images/generations` endpoint. Default model: `gemini-3-pro-image-preview`.

**Option B: Direct Gemini API**
```bash
export GEMINI_API_KEY="..."
```
Uses `google-genai` SDK directly. Get a key at https://aistudio.google.com/apikey

The scripts auto-detect which mode to use based on which env vars are set. LiteLLM takes priority if both are set.

## Quick Start

### Single image
```bash
python3 scripts/generate_image.py \
  --prompt "Luxury hotel lobby with golden lighting" \
  --output hero.png
```

### With model/size options (direct API)
```bash
python3 scripts/generate_image.py \
  --prompt "Abstract gold gradient background" \
  --output bg.png \
  --model gemini-3.1-flash-image-preview \
  --aspect 16:9 \
  --size 2K
```

### Edit an existing image (direct API only)
```bash
python3 scripts/generate_image.py \
  --prompt "Add warm golden hour lighting, keep everything else" \
  --input original.png \
  --output edited.png
```

### Batch generate from manifest
```bash
python3 scripts/batch_generate.py \
  --manifest assets.json \
  --outdir ./public/images
```

## Models

| Model | Best For | Via LiteLLM | Via Direct API |
|---|---|---|---|
| `gemini-3-pro-image-preview` | Highest quality. Default for LiteLLM. | Yes | Yes |
| `gemini-3.1-flash-image-preview` | Best quality/cost. Aspect + size control (512px–4K). | Check proxy config | Yes |
| `gemini-2.5-flash-image` | Fast, cost-efficient. Fixed 1024px. Default for direct. | Check proxy config | Yes |

## Workflow

1. **Identify assets needed** — List all images with purpose, dimensions, and style
2. **Write prompts** — See [references/prompt-guide.md](references/prompt-guide.md) for patterns
3. **Create manifest** — JSON array for batch generation
4. **Generate** — Run `batch_generate.py` or individual `generate_image.py` calls
5. **Review and iterate** — Use `--input` flag to refine (direct API only)
6. **Place in project** — Copy outputs to the project's `public/` or `assets/` directory

## Manifest Format

```json
[
  {
    "prompt": "Abstract luxury background, soft gold gradients, subtle geometric patterns",
    "filename": "hero-bg.png",
    "aspect": "16:9",
    "size": "2K"
  },
  {
    "prompt": "Minimalist shield icon, flat gold on white, clean lines",
    "filename": "icon-security.png",
    "aspect": "1:1",
    "size": "1K"
  }
]
```

Fields: `prompt` (required), `filename` (required), `aspect` (optional), `size` (optional), `input` (optional, editing via direct API only).

## Prompt Crafting — The Key Principles

**Write natural language, not keyword lists.** Gemini rewards creative direction over tag soup.

- BAD: `"dog, park, sunset, 4k, realistic, cinematic"`
- GOOD: `"A golden retriever bounding through a sun-dappled park at golden hour, shot from a low angle with shallow depth of field"`

**Be specific.** Add materiality, texture, and context:
- Instead of "a cup": `"a handmade ceramic coffee cup with an uneven clay glaze, steam curling upward"`

**Use camera language.** The model understands: shallow depth of field, Rembrandt lighting, wide establishing shot, 35mm film grain, macro photography.

**Mention the purpose.** "Create a hero image for a premium coffee brand's website" helps the model infer appropriate composition and lighting.

**Edit, don't re-roll.** When an image is mostly right, request conversational changes: "Make the lighting warmer" or "Remove the background person." The model adjusts physics automatically.

### Reference Images & Consistency
- Up to **5 consistent characters** and **14 consistent objects** per workflow
- Use: "Keep facial features exactly the same as the reference"
- For storyboarding: "Identity and attire must stay consistent throughout"

### Text in Images
Gemini has strong text rendering. Always put exact text in **quotation marks**:
- `with the text "MIDNIGHT REVERIE" in bold art deco typography`
- Specify style: "handwritten script", "retro neon sign", "bold sans-serif"

See [references/prompt-guide.md](references/prompt-guide.md) for the full prompt engineering guide with camera/lighting/material vocabularies, example prompts, web UI presets, and anti-patterns to avoid.

## Reliability Features

### Auto-Retry
`generate_image.py` retries rate-limited (429) and transient server errors up to 3 times with exponential backoff + jitter. No action needed — this happens automatically.

### Failed Manifest
When `batch_generate.py` encounters failures, it writes a `*-failed.json` manifest. Retry with the same command:
```bash
python3 scripts/batch_generate.py -f manifest-failed.json -d ./public/images
```

### Skip Existing
`batch_generate.py` skips images that already exist in the output directory. Use `--force` to regenerate all.

### Smarter Defaults
- Default delay: **4s** for LiteLLM proxy (stricter rate limits), **2s** for direct API
- Default model auto-detects based on env vars

## Avoiding Safety Filter Rejections

Gemini's safety classifier blocks prompts it considers ambiguous or potentially problematic. **Concrete, photographic descriptions work; abstract/conceptual ones fail.**

| Fails | Works |
|-------|-------|
| "seamless tileable vellum texture" | "Close-up photograph of cream colored handmade paper with visible fiber texture" |
| "abstract dark moody surface" | "Close-up photograph of dark charcoal paper with subtle grain, macro photography" |
| "gold metallic effect" | "Brushed gold metallic circle, warm polished brass surface, clean product photography" |

**Rules:**
1. **Describe what the camera sees**, not the concept — "photograph of paper" not "paper texture"
2. **Add physical materials** — "handmade paper", "brass surface", "ink on paper"
3. **Include photographic terms** — "macro photography", "product photography", "close-up"
4. **Name specific colors** — "cream colored", "dark charcoal" not just "warm" or "dark"
5. **Avoid abstract adjectives alone** — always pair with a noun ("elegant serif calligraphy" not just "elegant")

## Programmatic Fallback

Certain image types consistently fail on Gemini because they're procedural/mathematical rather than photographic. The scripts automatically detect these prompts and generate them with Pillow instead:

| Prompt Type | Detection Keywords | What It Generates |
|---|---|---|
| **Noise/grain textures** | "noise texture", "grain texture", "film grain", "grainy", "digital noise" | Random RGBA noise at configurable opacity |
| **Solid color fills** | "solid color", "solid background", "plain background", "uniform background" | Single-color image (parses hex from prompt) |
| **Simple gradients** | "simple gradient", "linear gradient background", "color gradient", "vertical gradient" | Two-color vertical gradient (parses hex from prompt) |

This happens automatically — no flags needed. If the prompt contains these keywords, Pillow generates the image without calling the API.

## Known Limitations — What Gemini Cannot Generate

These prompt categories reliably fail or produce poor results. Use the programmatic fallback or manual creation:

1. **Pure noise/grain textures** — Auto-handled by programmatic fallback
2. **Solid color images** — Auto-handled by programmatic fallback
3. **Exact text rendering** — Improved (state-of-the-art for AI), but not pixel-perfect for production. Use SVG/CSS for final text.
4. **Transparent backgrounds** — Gemini always generates opaque images (use Pillow to remove backgrounds post-generation)
5. **Pixel-perfect patterns** — Seamless tileable patterns are hit-or-miss; use CSS patterns instead
6. **UI mockups with precise layouts** — Better to code these directly in HTML/CSS
7. **Very abstract conceptual requests** — "the feeling of growth" fails; "golden crystalline prisms ascending" works

## Gotchas

- **LiteLLM proxy**: image editing (`--input`) is not supported — use direct API for that
- **LiteLLM proxy**: `--size` maps to OpenAI format (`1024x1024`); `--aspect` is appended as a prompt hint
- **LiteLLM proxy rate limits**: are stricter than direct Gemini API — use `--delay 6` for large batches (>15 images). Never run multiple batch processes in parallel against the same proxy.
- **Direct API**: `image_size` must use **uppercase K** — `"2K"` not `"2k"`
- **Direct API**: `gemini-2.5-flash-image` ignores aspect/size params (fixed 1024px)
- **Model access**: LiteLLM proxy virtual keys may only authorize specific models. If you get auth errors, check which models your key allows and pass `--model` explicitly.
- Safety filters may return text instead of an image — see "Avoiding Safety Filter Rejections" above
- All generated images include an invisible SynthID watermark (does not affect visual quality)
- Auto-installs `openai` or `google-genai` + `Pillow` on first run as needed
