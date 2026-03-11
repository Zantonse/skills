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

## Deep Mode (`--deep`)

### When to Trigger

Deep mode activates when the user's message contains:
- "deep dive on [topic]"
- "deep research [topic]"
- "research [topic] --deep"
- "thorough deep dive [topic]"
- "comprehensive research [topic]"

Deep mode uses **parallel specialist agents** for web research, then **Gemini for synthesis** — combining Claude's web scraping capabilities with Gemini's large context window for cross-referencing.

### How It Works

#### Step 1: Decompose the Question into Research Domains

Break the user's question into 4-6 independent research domains. Each domain becomes a specialist agent. For example, "best AI video creation tools for realistic 15-minute videos" decomposes into:
- Domain 1: AI avatar / talking head platforms
- Domain 2: AI voice synthesis tools
- Domain 3: AI video generation for B-roll
- Domain 4: Lip sync & face animation
- Domain 5: Workflow orchestration & pipeline tools
- Domain 6: Cost & throughput analysis

Present the domains to the user briefly before dispatching: "Researching across 5 domains: [list]. Dispatching agents now."

#### Step 2: Dispatch Specialist Agents in Parallel

For each domain, dispatch a `general-purpose` subagent with `model: "sonnet"`:

```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  run_in_background=true,
  prompt="""
You are a specialist researcher investigating: {DOMAIN_DESCRIPTION}

Research question context: {USER_QUERY}

Use WebSearch, firecrawl_search, and firecrawl_scrape to find current, specific data.
Focus on: product names, pricing, capabilities, limitations, comparisons, and real user experiences.
Cite sources with dates. Prefer 2025-2026 data.

Produce a structured markdown section titled "## {DOMAIN_NAME}" with:
- Key findings (specific products, features, pricing)
- Comparison tables where applicable
- Current limitations and workarounds
- Recommendations within this domain

Today's date: {TODAY_DATE}
"""
)
```

All agents run concurrently. Dispatch them all in a single message.

#### Step 3: Extract Specialist Outputs from JSONL

After all agents complete, extract their research text from the JSONL transcript files:

```bash
mkdir -p /tmp/deep-extracts && python3 -c "
import json, os

agents = {
    'domain1': '{AGENT1_ID}',
    'domain2': '{AGENT2_ID}',
    'domain3': '{AGENT3_ID}',
    'domain4': '{AGENT4_ID}',
    # ... add more as needed
}

base_path = # use the actual task output directory from agent notifications

for name, agent_id in agents.items():
    filepath = f'{base_path}/{agent_id}.output'
    best_text = ''
    try:
        with open(filepath, 'r', errors='replace') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    obj = json.loads(line)
                    msg = obj.get('message', {})
                    if msg.get('role') == 'assistant':
                        content = msg.get('content', [])
                        if isinstance(content, list):
                            for block in content:
                                if isinstance(block, dict) and block.get('type') == 'text':
                                    text = block.get('text', '')
                                    if len(text) > len(best_text):
                                        best_text = text
                except: pass
        outpath = f'/tmp/deep-extracts/{name}.md'
        with open(outpath, 'w') as f:
            f.write(best_text)
        print(f'{name}: {len(best_text)} chars')
    except Exception as e:
        print(f'{name}: ERROR - {e}')
"
```

#### Step 4: Synthesize with Gemini via LiteLLM

Concatenate all extracted specialist outputs into a single context file, then send to Gemini for synthesis:

```bash
# Concatenate all specialist outputs
cat /tmp/deep-extracts/domain*.md > /tmp/deep-extracts/all_specialist_outputs.md

# Send to Gemini for synthesis
python3 /Users/craigverzosa/.claude/skills/deep-research/scripts/research.py \
  -q "Synthesize the following specialist research into a comprehensive, actionable report. Cross-reference findings across domains for agreements and contradictions. Produce: (1) an executive summary with the top recommendation, (2) a detailed comparison matrix, (3) a recommended workflow/pipeline, (4) cost analysis, (5) current limitations and workarounds. Original question: {USER_QUERY}" \
  -c /tmp/deep-extracts/all_specialist_outputs.md \
  -o ~/Documents/ObsidianNotes/Claude-Research/{OUTPUT_FILENAME}.md \
  --max-tokens 16000
```

Gemini's large context window handles all specialist outputs in a single call — no timeout risk, no subagent turn limits.

#### Step 5: Enhance and Write to Obsidian

After Gemini returns the synthesis:
1. Read the output file
2. Prepend YAML frontmatter with `deep_mode: true` tag
3. Add wiki-links for cross-referencing
4. Report key findings to the user conversationally

#### Fallback

If Gemini synthesis fails (API error, rate limit), fall back to synthesizing directly in the main conversation window by reading all extracted specialist files and writing the report manually.

---

## Research Patterns

See [references/research-patterns.md](references/research-patterns.md) for detailed prompt patterns and multi-source workflows.
