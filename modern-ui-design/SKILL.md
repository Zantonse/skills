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

1. Determine context (project-specific or general research)
2. Read [references/research-areas.md](references/research-areas.md) for search queries per area
3. Dispatch 4 parallel subagents using the Task tool
4. Synthesize findings into a design brief
5. Save to Obsidian vault (if configured in CLAUDE.md) AND project, then summarize in conversation

### Step 1: Determine Context

Two modes:
- **Project-specific:** Tailor search queries to the project type. A fintech dashboard needs different trends than a creative portfolio.
- **General research:** Run all four areas broadly to build a reusable knowledge base.

If the user hasn't specified a project, ask briefly or default to general research.

### Step 2: Dispatch Research Subagents

Launch 4 parallel Task subagents (subagent_type: "general-purpose", model: "sonnet").

Each agent prompt should include:
1. The search queries from references/research-areas.md for their research area
2. Explicit instruction to use `firecrawl_search` with `limit: 5` per query
3. Instruction to pick the 2-3 best URLs from results and scrape them with `firecrawl_scrape` using `formats: ["markdown"]` and `onlyMainContent: true`
4. The specific extract targets from references/research-areas.md (what data to pull from pages)
5. Project context (if any)
6. Current year for relevance filtering
7. Instruction to return structured markdown with actionable findings and source URLs

**Why markdown scraping instead of JSON extraction:** In practice, subagents get richer results scraping full articles as markdown and extracting findings themselves than trying to use firecrawl_scrape's JSON schema extraction — design articles are narrative, not structured data. The JSON schemas in references/research-areas.md serve as a reference for what fields to extract, not as literal firecrawl parameters.

**Fallback chain:** If scrape returns empty, retry with `waitFor: 5000`. If still empty, use `firecrawl_map` to find the correct subpage.

**The 4 agents:**
1. **Visual Trends** — color, typography, spacing, animation, texture
2. **Component Patterns** — layouts, navigation, cards, forms, data viz
3. **AI Anti-Patterns** — what makes AI-generated UIs look generic and how to avoid it
4. **CSS & Web Platform** — new CSS features, performance techniques, modern capabilities

### Step 3: Synthesize Design Brief

Combine all 4 agents' findings into a single design brief using this structure:

```markdown
---
date: [today]
tags: [design, ui-trends, css, typography, color, research]
source: claude-code
project: [project name or "general"]
---

# UI Design Research Brief
Generated: [date]
Project context: [what is being built, or "general research"]

## Executive Summary
[3-5 bullet points: the most impactful findings]

## Visual Direction
### Color Strategy
[Specific palettes in OKLCH where possible, NOT generic advice]
### Typography
[Specific font pairings with rationale]
### Motion & Animation
[Specific CSS techniques with code snippets]

## Component Strategy
### Layout
[Specific patterns with CSS examples]
### Key Components
[Patterns that elevate the project]
### Interaction Patterns
[Micro-interactions with implementation notes]

## Anti-Pattern Checklist
[Checkbox list of AI-generated UI markers to avoid]

## CSS Techniques to Use
[Table: feature | replaces | example code]

## Sources
[URLs referenced]
```

Include YAML frontmatter so the brief works as an Obsidian note (with date, tags, source fields).

### Step 4: Save and Summarize

Save the design brief to **all applicable locations:**
1. **Obsidian vault** (if configured in CLAUDE.md): write to the vault's Claude-Research/Design/ folder
2. **Project**: `.planning/design-brief.md` (if using GSD) or `design-brief.md` (project root)
3. **Conversation**: Summarize the top 5-8 actionable findings so the next skill can use them immediately

## Notes

- Always use `model: "sonnet"` for subagents
- Research should focus on what is **current and production-ready**, not experimental
- Prefer findings with concrete examples (code snippets, font names, hex/oklch values) over abstract trend descriptions
- If a research area returns thin results, broaden search queries rather than padding with generic advice
- A full run takes 2-4 minutes with all 4 agents in parallel
