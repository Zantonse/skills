---
name: deep-research
description: "Deep research and analysis using Gemini 3.1 Pro Preview's large context window via LiteLLM proxy. Use when: (1) the user asks a deep, complex, or multi-faceted question requiring thorough analysis, (2) researching a company for a sales account overview or prospect briefing, (3) any request containing 'deep research', 'research this', 'deep dive', 'thorough analysis', or 'account overview', (4) comparing technologies, architectures, or approaches in depth, (5) market research, competitive analysis, or industry landscape questions, (6) when a subagent needs deep analytical capability beyond web search. Triggers on: 'deep research', 'research', 'account overview', 'company research', 'deep dive', 'analyze thoroughly', 'competitive analysis', 'market research', or any question that requires synthesis across many data points."
---

# Deep Research

Send complex queries to Gemini 3.1 Pro Preview for thorough analysis via `scripts/research.py`. Uses `LITELLM_API_KEY` and `LITELLM_BASE_URL` from the environment (set in `~/.claude-litellm.env`).

## Two Research Modes

### General Research (`--mode general`)
Deep analysis on any topic — technology, architecture, markets, trends. Returns structured markdown with findings, analysis, and recommendations.

### Sales Account Overview (`--mode account`)
Structured company research for SE prep — company overview, tech landscape, pain points, opportunity analysis, competitive positioning, and discovery questions.

## Workflow

### Simple: Direct Query
```bash
python3 scripts/research.py -q "Your research question" -o output.md
```

### With Context: Gather Then Analyze
1. **Gather** — Use web search, firecrawl scraping, file reads to collect raw data
2. **Analyze** — Feed gathered data as context to Gemini for synthesis:
```bash
python3 scripts/research.py \
  -q "Synthesize findings on [topic]" \
  -c scraped-page.md notes.md data.txt \
  -o findings.md
```

### Account Overview
```bash
python3 scripts/research.py \
  -q "Build account overview for Snowflake" \
  --mode account \
  -o accounts/snowflake.md
```

### Piped Input (from other tools)
```bash
curl -s https://example.com/about | python3 scripts/research.py -q "Analyze this company" --stdin
```

## Best Results Pattern

For the deepest research, **gather context first** before calling the script:

1. Use `WebSearch` or `firecrawl_search` to find relevant pages
2. Use `firecrawl_scrape` or `WebFetch` to get full page content
3. Save scraped content to temp files
4. Pass all context files with `-c` flag
5. The more context Gemini has, the better the synthesis

Gemini 3.1 Pro has a massive context window — feed it everything relevant.

## Subagent Usage

Dispatch as a Task tool subagent for parallel research:
```
Task tool (general-purpose):
  prompt: |
    Run deep research:
    python3 /path/to/scripts/research.py \
      -q "Research question" \
      --mode account \
      --json

    Parse the JSON result and summarize findings.
```

Use `--json` flag for structured output when parsing programmatically.

## Script Reference

```
python3 scripts/research.py [options]

Required:
  -q, --query      Research query or question

Optional:
  -c, --context    Context files to include (one or more paths)
  --stdin          Read additional context from stdin
  -m, --mode       Research mode: general (default), account
  -s, --system     Custom system prompt (overrides mode defaults)
  -o, --output     Save to file instead of stdout
  --model          Model name (default: gemini-3.1-pro-preview)
  --max-tokens     Max response length (default: 16000)
  --json           Output as JSON with metadata
```

## Obsidian Integration

All research output should be saved to the user's Obsidian vault by default.

**Default output path:** `~/Documents/ObsidianNotes/Claude-Research/`

**After writing the research output file, always prepend YAML frontmatter:**
```yaml
---
date: YYYY-MM-DD
tags:
  - research
  - [topic-specific tags]
source: claude-code
project: [current project name or 'general-research']
---
```

**Add wiki-links** for cross-referencing related notes:
```markdown
> Related: [[related-topic-1]] [[related-topic-2]]
```

**File naming convention:** `topic-slug-YYYY-MM.md` (e.g., `tech-layoffs-march-2026.md`, `deel-account-overview.md`)

**Account research** goes to: `~/Documents/ObsidianNotes/Claude-Research/accounts/`
**General research** goes to: `~/Documents/ObsidianNotes/Claude-Research/`

If the `-o` flag is not provided, default to the Obsidian path with an auto-generated filename based on the query.

## Research Patterns

See [references/research-patterns.md](references/research-patterns.md) for detailed prompt patterns and multi-source workflows.
