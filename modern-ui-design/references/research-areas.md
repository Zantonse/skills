# Research Areas

Use these as search targets when dispatching subagents. Each area maps to a dedicated research subagent.

Each area includes:
- **Search queries** for `firecrawl_search` (use limit: 5 per query)
- **Extraction schema** for `firecrawl_scrape` with JSON format on the best result URLs
- **Extract targets** describing what to pull from pages

## Area 1: Visual Design Trends

Search queries for `firecrawl_search`:
- "UI design trends 2025 2026"
- "modern web design color palettes 2026"
- "typography trends web design 2025"
- "modern CSS animation techniques"
- "glassmorphism neubrutalism design trends current"

Extraction schema for `firecrawl_scrape` (use with `formats: [{ type: "json", prompt: "...", schema: ... }]`):
```json
{
  "type": "object",
  "properties": {
    "trends": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" },
          "category": { "type": "string", "enum": ["color", "typography", "animation", "texture", "spacing", "other"] },
          "examples": { "type": "array", "items": { "type": "string" } },
          "production_ready": { "type": "boolean" }
        }
      }
    }
  }
}
```
Prompt for extraction: "Extract current UI/web design trends from this page. Focus on color strategies, typography pairings, animation techniques, texture/depth approaches, and spacing patterns. Only include trends from 2024-2026."

Extract targets:
- Dominant color strategies (dark mode defaults, accent approaches, gradients vs flat)
- Typography pairings gaining traction (variable fonts, display + body combos)
- Spacing and density patterns (content-dense vs breathing layouts)
- Animation/motion conventions (scroll-driven animations, view transitions API, spring physics)
- Texture and depth techniques (noise, grain, mesh gradients, layered glass)

## Area 2: Component Architecture Patterns

Search queries for `firecrawl_search`:
- "modern UI component patterns 2025 2026"
- "design system trends 2026"
- "micro-interactions web design best practices"
- "modern navigation patterns web apps"
- "responsive layout strategies beyond media queries"

Extraction schema for `firecrawl_scrape`:
```json
{
  "type": "object",
  "properties": {
    "patterns": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" },
          "category": { "type": "string", "enum": ["layout", "navigation", "cards", "forms", "data-viz", "interaction", "other"] },
          "css_features_used": { "type": "array", "items": { "type": "string" } },
          "use_case": { "type": "string" }
        }
      }
    }
  }
}
```
Prompt for extraction: "Extract modern UI component patterns and design system trends from this page. Focus on layout innovations, navigation paradigms, card patterns, form design, data visualization, and micro-interactions."

Extract targets:
- Layout innovations (container queries, subgrid, dynamic islands, bento grids)
- Navigation paradigms (command palettes, radial menus, contextual nav)
- Card and surface patterns (stacked, overlapping, expandable)
- Form design evolution (inline validation, progressive disclosure, conversational forms)
- Data visualization approaches (sparklines, inline charts, ambient data)

## Area 3: AI-Generated UI Anti-Patterns

Search queries for `firecrawl_search`:
- "AI generated UI looks generic how to fix"
- "claude AI code generation UI design quality"
- "AI vibe coding design problems"
- "why AI generated websites look the same"
- "LLM generated frontend anti-patterns"

Extraction schema for `firecrawl_scrape`:
```json
{
  "type": "object",
  "properties": {
    "anti_patterns": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "pattern": { "type": "string" },
          "why_it_looks_generic": { "type": "string" },
          "remedy": { "type": "string" },
          "category": { "type": "string", "enum": ["typography", "color", "layout", "spacing", "components", "other"] }
        }
      }
    },
    "design_fixes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "before": { "type": "string" },
          "after": { "type": "string" },
          "improvement": { "type": "string" }
        }
      }
    }
  }
}
```
Prompt for extraction: "Extract common problems with AI-generated UIs and how to fix them. Focus on visual fingerprints that make UIs look AI-generated (generic fonts, predictable layouts, cookie-cutter patterns) and specific remedies human designers use."

Extract targets:
- Common visual fingerprints of AI-generated UIs (Inter font, purple gradients, identical card grids)
- Structural anti-patterns (over-reliance on Tailwind defaults, identical padding everywhere)
- What makes AI output look "templated" vs "designed"
- Specific remedies: what human designers do differently
- Before/after examples of AI UI improved by design thinking

## Area 4: Cutting-Edge CSS and Web Platform

Search queries for `firecrawl_search`:
- "new CSS features 2025 2026 web design"
- "CSS anchor positioning scroll-driven animations"
- "view transitions API web apps"
- "modern CSS techniques designers should know"
- "CSS container queries subgrid production examples"

Extraction schema for `firecrawl_scrape`:
```json
{
  "type": "object",
  "properties": {
    "features": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" },
          "browser_support": { "type": "string" },
          "code_example": { "type": "string" },
          "use_case": { "type": "string" },
          "production_ready": { "type": "boolean" }
        }
      }
    }
  }
}
```
Prompt for extraction: "Extract modern CSS features and web platform capabilities from this page. Focus on features that are production-ready or nearly so, including browser support status, code examples, and practical use cases for UI design."

Extract targets:
- New CSS capabilities ready for production (anchor positioning, scroll-driven animations, view transitions)
- Performance-friendly animation techniques
- Variable font strategies for dynamic typography
- Color spaces beyond sRGB (oklch, display-p3)
- Modern gradient and blend techniques
