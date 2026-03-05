---
name: full-design
description: End-to-end autonomous design pipeline that chains research, asset generation, and UI implementation into a single command. Runs /modern-ui-design (trend research), /gemini-image-gen (visual assets), then /frontend-design (code) sequentially without pausing. Use when building a new UI from scratch and you want the full design workflow automated. Triggers on "full design", "design pipeline", "build UI end to end", "complete design workflow", or when the user wants research + assets + implementation in one shot. Do NOT use for partial workflows — use the individual skills instead.
---

Autonomous design pipeline: research → assets → implementation. Run all three stages without pausing.

## Pipeline

### Stage 1: Design Research — invoke /modern-ui-design

Gather the project context from the user's request, then invoke the `/modern-ui-design` skill:
- Dispatch 4 parallel research subagents (visual trends, component patterns, AI anti-patterns, CSS techniques)
- Produce a design brief file and conversation summary
- Extract: recommended color strategy, typography, layout patterns, anti-pattern checklist

**Carry forward to Stage 2:** The design brief's visual direction, color palette, and aesthetic recommendations.

### Stage 2: Asset Generation — invoke /gemini-image-gen

Using the design brief from Stage 1, determine what visual assets the UI needs. Common assets:
- App icon or logo matching the chosen aesthetic
- Hero illustration or background texture
- Custom icons for key UI elements
- Decorative elements (patterns, gradients, textures)

Invoke `/gemini-image-gen` with prompts derived from the design brief's visual direction. Generate 2-4 assets that the UI will reference.

**Carry forward to Stage 3:** File paths of generated assets + the full design brief.

### Stage 3: UI Implementation — invoke /frontend-design

Invoke `/frontend-design` with the combined context:
- Design brief findings (color, typography, layout, motion)
- Generated asset file paths (reference them in the code)
- The user's original requirements

Build production-grade, working code that incorporates the researched trends and generated assets.

## Context Threading

Each stage's output feeds the next. Maintain these through the pipeline:

```
Stage 1 output → design-brief.md + conversation summary
                    ↓
Stage 2 input  → "Generate assets matching [brief's visual direction]"
Stage 2 output → asset file paths + descriptions
                    ↓
Stage 3 input  → brief + asset paths + user requirements
Stage 3 output → working frontend code
```

## Usage

When invoked, immediately ask the user one question:

> "What are you building? Describe the app/page/component, its audience, and any constraints."

Then run all three stages autonomously using that context. Do not pause between stages.

## Notes

- Always use `model: "sonnet"` for any subagents dispatched
- If `/gemini-image-gen` is unavailable or fails, skip to Stage 3 — the pipeline should not break due to asset generation issues
- If the project already has a design brief from a prior `/modern-ui-design` run, skip Stage 1 and start from Stage 2
