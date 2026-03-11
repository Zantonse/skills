# Research Areas

Each area maps to one parallel subagent. Includes search queries for `firecrawl_search` and extract targets describing what to pull from scraped pages.

The JSON schemas below are **reference schemas** — they describe the structure of findings each agent should return. Agents should scrape pages as markdown (`formats: ["markdown"], onlyMainContent: true`) and extract these fields themselves, rather than passing schemas to firecrawl_scrape's JSON extraction (design articles are narrative, not structured data).

## Area 1: Visual Design Trends

Search queries (`firecrawl_search`, limit: 5 per query):
- "UI design trends 2025 2026"
- "modern web design color palettes 2026"
- "typography trends web design 2025"

Pick 2-3 best URLs from results, scrape with `firecrawl_scrape` (markdown format).

Extract these fields from each trend found:
- **name**: trend name
- **description**: what it is and why it's gaining traction
- **category**: color | typography | animation | texture | spacing
- **examples**: specific values (hex codes, font names, CSS properties)
- **production_ready**: boolean

Focus areas:
- Dominant color strategies (dark mode + neon, earthy minimalism, saturated Y2K)
- Typography pairings (variable fonts, display + body combos, specific font names)
- Spacing patterns (content-dense vs breathing, base grid units)
- Animation conventions (scroll-driven, view transitions, spring physics easing curves)
- Texture and depth (noise/grain overlays, mesh gradients, glassmorphism maturation)

## Area 2: Component Architecture Patterns

Search queries (`firecrawl_search`, limit: 5 per query):
- "modern UI component patterns 2025 2026"
- "design system trends 2026"
- "micro-interactions web design best practices"

Pick 2-3 best URLs, scrape as markdown.

Extract these fields from each pattern found:
- **name**: pattern name
- **description**: what it is and how it works
- **category**: layout | navigation | cards | forms | data-viz | interaction
- **css_features_used**: list of CSS properties/features involved
- **use_case**: where this pattern fits best

Focus areas:
- Layout innovations (container queries, subgrid, bento grids, maximalist layering)
- Navigation paradigms (command palettes, contextual nav, experimental/radial)
- Card patterns (stacked/expandable, neumorphic, hierarchy through size not uniformity)
- Form design (real-time inline validation, progressive disclosure, emotionally aware timing)
- Micro-interactions (skeleton screens, celebratory confirmations, hover feedback with 3 properties)

## Area 3: AI-Generated UI Anti-Patterns

Search queries (`firecrawl_search`, limit: 5 per query):
- "AI generated UI looks generic how to fix"
- "AI vibe coding design problems"
- "why AI generated websites look the same"

Pick 2-3 best URLs, scrape as markdown.

Extract these fields:
- **anti_patterns**: list of { pattern, why_it_looks_generic, remedy, category }
- **design_fixes**: list of { before, after, improvement }

Focus areas:
- Visual fingerprints (Inter font, purple gradients, identical card grids, floating 3D blobs)
- Structural anti-patterns (Tailwind defaults as finished design, uniform padding, predictable section ordering)
- The "templated vs designed" distinction
- Specific remedies: token override, hierarchy injection, voice as design material
- Before/after examples

## Area 4: Cutting-Edge CSS and Web Platform

Search queries (`firecrawl_search`, limit: 5 per query):
- "new CSS features 2025 2026 web design"
- "CSS anchor positioning scroll-driven animations"
- "CSS container queries subgrid production examples"

Pick 2-3 best URLs, scrape as markdown.

Extract these fields from each feature found:
- **name**: CSS feature name
- **description**: what it does
- **browser_support**: which browsers and versions
- **code_example**: working CSS snippet
- **use_case**: practical design application
- **production_ready**: boolean

Focus areas:
- Anchor positioning (replaces Popper.js)
- Scroll-driven animations (replaces GSAP ScrollTrigger)
- View Transitions API (SPA-quality page transitions in MPAs)
- `@starting-style` (entry animations without JS)
- OKLCH color space + relative color syntax
- Container queries + container query units
- `@scope`, `:has()`, native nesting, cascade layers
- `text-wrap: balance` and `text-wrap: pretty`
