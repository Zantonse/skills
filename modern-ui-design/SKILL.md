---
name: modern-ui-design
description: Research current modern UI design trends, patterns, and strategies to inform frontend implementation. Use BEFORE building any UI — dispatches parallel subagents to search the web for current visual design trends, component patterns, AI-generated UI anti-patterns, and cutting-edge CSS techniques. Produces a design research brief (markdown file + conversation summary) that feeds into /frontend-design or direct implementation. Triggers on "research UI trends", "modern design", "design research", "UI inspiration", or when starting a new frontend project that needs design direction. This is a research skill, NOT an implementation skill — use /frontend-design for actual code generation.
---

Research current UI design trends via parallel Firecrawl-powered subagents. Produce a design brief that informs subsequent frontend implementation.

## Relationship to /frontend-design

This skill is the **research phase** — run it before `/frontend-design`:
- `/modern-ui-design` → discovers WHAT modern design looks like right now
- `/frontend-design` → implements HOW to build it in code

## Workflow

1. Read [references/research-areas.md](references/research-areas.md) for search targets and extraction schemas
2. Dispatch 4 parallel subagents (one per research area) using the Task tool
3. Synthesize findings into a design brief
4. Save brief to project AND summarize in conversation

### Step 1: Determine Context

Before researching, understand the project:
- What is being built? (app type, audience, purpose)
- Any existing design direction or constraints?
- Specific areas of interest? (default: all four areas)

Use this context to tailor search queries — a fintech dashboard needs different trends than a creative portfolio.

### Step 2: Dispatch Research Subagents

Launch 4 parallel Task subagents (subagent_type: "general-purpose", model: "sonnet"). Each agent uses Firecrawl tools for research.

**Agent research strategy (each agent follows this):**
1. **Search** with `firecrawl_search` using queries from references/research-areas.md (limit: 5 results per query, no scrapeOptions — search first, scrape after)
2. **Identify** the 2-3 most relevant result URLs from search
3. **Scrape** those URLs with `firecrawl_scrape` using JSON format + the extraction schema from references/research-areas.md to pull structured data
4. **Fallback**: If scrape returns empty (JS-rendered), retry with `waitFor: 5000`. If still empty, use `firecrawl_map` to find the correct subpage, then scrape that.

**Agent prompts must include:**
- The specific research area, search queries, AND JSON extraction schema from references/research-areas.md
- The project context (what is being built)
- Instruction to use `firecrawl_search` for discovery, then `firecrawl_scrape` with JSON schema for extraction
- Instruction to return findings as structured markdown with specific, actionable items
- Instruction to include source URLs for key findings
- Current year context (for relevance filtering)

**The 4 agents:**
1. **Visual Trends** — color, typography, spacing, animation, texture
2. **Component Patterns** — layouts, navigation, cards, forms, data viz
3. **AI Anti-Patterns** — what makes AI-generated UIs look generic and how to avoid it
4. **CSS & Web Platform** — new CSS features, performance techniques, modern capabilities

### Step 3: Synthesize Design Brief

Combine all 4 agents' findings into a single design brief. Use this structure:

```markdown
# UI Design Research Brief
Generated: [date]
Project context: [what is being built]

## Executive Summary
[3-5 bullet points: the most impactful findings for THIS project]

## Visual Direction
### Recommended Approach
[Specific recommendations tailored to the project, drawing from visual trends research]
### Color Strategy
[Specific palettes or approaches, NOT generic advice]
### Typography
[Specific font recommendations or pairing strategies]
### Motion & Animation
[Specific techniques appropriate for the project]

## Component Strategy
### Layout
[Specific layout patterns suited to this project]
### Key Components
[Component patterns that would elevate this project]
### Interaction Patterns
[Micro-interactions and UX patterns to consider]

## Anti-Pattern Checklist
[Specific things to AVOID — the "AI slop" markers to watch for]
- [ ] Generic font (Inter, Roboto, system default)
- [ ] Purple gradient on white
- [ ] Identical card grids with uniform padding
- [ ] [additional items from research]

## CSS Techniques to Use
[Modern CSS features that are production-ready and relevant]

## Sources
[Key URLs referenced during research]
```

### Step 4: Save and Summarize

1. Save the design brief to the project: `.planning/design-brief.md` (if using GSD) or `design-brief.md` (project root)
2. Summarize the top 5-8 actionable findings in conversation so the next skill (/frontend-design) or implementation step can use them immediately

## Notes

- Always use `model: "sonnet"` for subagents
- Research should focus on what is **current and production-ready**, not experimental
- Prefer findings with concrete examples over abstract trend descriptions
- If a research area returns thin results, broaden search queries rather than padding with generic advice
