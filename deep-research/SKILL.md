---
name: deep-research
description: "Parallel specialist agent teams for comprehensive research with Gemini synthesis. Always uses the full agent team pipeline (4-6 parallel research agents + coverage gap check + Gemini cross-domain synthesis). Use when: (1) the user asks a deep, complex, or multi-faceted question requiring thorough analysis, (2) researching a company for a sales account overview or prospect briefing, (3) any request containing 'deep research', 'research this', 'deep dive', 'thorough analysis', or 'account overview', (4) comparing technologies, architectures, or approaches in depth, (5) market research, competitive analysis, or industry landscape questions, (6) when a subagent needs deep analytical capability beyond web search. Triggers on: 'deep research', 'research', 'account overview', 'company research', 'deep dive', 'analyze thoroughly', 'competitive analysis', 'market research', or any question that requires synthesis across many data points."
---

# Deep Research

Parallel specialist agent teams for comprehensive research, with Gemini synthesis. Every research request uses the full agent team pipeline — there is no "simple" mode.

**Architecture:** Decompose the question into 4-6 research domains → dispatch parallel specialist agents (each scrapes the web independently) → check coverage gaps → synthesize all findings through Gemini's large context window → save to Obsidian vault.

## Gemini Synthesis Script

The `scripts/research.py` script sends gathered context to Claude Sonnet with extended thinking (8K token budget) for synthesis. Routes through LiteLLM proxy using `LITELLM_API_KEY` and `LITELLM_BASE_URL` from `~/.claude-litellm.env`.

**This script is used ONLY in Step 4 (synthesis) — never as the primary research method.** All research is done by parallel specialist agents first.

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

## How It Works

**Every research request follows this pipeline. There is no lightweight mode — the agent team approach is always used.**

### Step 0: Generate Research Plan (show before dispatching)

Before dispatching agents, decompose the question and present the plan to the user. This is inspired by how Gemini Deep Research works — showing the plan before executing lets the user redirect strategy before expensive retrieval operations begin.

Break the user's question into 4-6 research sub-questions. Each sub-question becomes a specialist agent's focus area. The key is making sub-questions independent enough to research in parallel while collectively covering the full scope of the user's question. For example, "best AI video creation tools for realistic 15-minute videos" decomposes into:
1. What AI avatar / talking head platforms exist and how do they compare?
2. What AI voice synthesis tools produce the most natural-sounding speech?
3. What AI video generation tools work best for B-roll and scene creation?
4. What lip sync and face animation solutions integrate with the above?
5. How do you orchestrate a pipeline combining these tools end-to-end?
6. What are the realistic costs and throughput for a 15-minute video?

Present the plan to the user:
```
Researching across 6 sub-questions:
1. AI avatar / talking head platforms
2. AI voice synthesis tools
3. AI video generation for B-roll
4. Lip sync & face animation
5. Workflow orchestration & pipeline tools
6. Cost & throughput analysis

Dispatching specialist agents now. (Reply to adjust before results come in.)
```

Then proceed immediately — don't block on user confirmation. If the user responds with adjustments before agents finish, incorporate them in a second-pass round.

### Step 1: Dispatch Specialist Agents in Parallel

For each domain, dispatch a `general-purpose` subagent with `model: "sonnet"`:

```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  run_in_background=true,
  prompt="""
You are a specialist researcher investigating: {DOMAIN_DESCRIPTION}

Research question context: {USER_QUERY}

## Search Strategy (use firecrawl CLI via Bash tool)

Your PRIMARY search tool is the firecrawl CLI, run via the Bash tool. It returns clean
markdown and handles JS-rendered pages. Use this escalation pattern:

1. **Search + scrape** (start here for any new topic):
   ```
   firecrawl search "your search query" --scrape --limit 3 -o /tmp/deep-research/{DOMAIN_SLUG}-search.json --json
   ```
   This searches AND fetches full page content in one call. Parse results with:
   ```
   jq -r '.data.web[] | "## " + .title + "\nURL: " + .url + "\n" + .description' /tmp/deep-research/{DOMAIN_SLUG}-search.json
   ```

2. **Scrape a specific URL** (when you find a promising page):
   ```
   firecrawl scrape "https://exact-url.com/page" -o /tmp/deep-research/{DOMAIN_SLUG}-page.md
   ```
   Then read the output file to extract findings.

3. **Parallel scrapes** (when you have multiple URLs to check):
   ```
   firecrawl scrape "url1" -o /tmp/deep-research/page1.md &
   firecrawl scrape "url2" -o /tmp/deep-research/page2.md &
   wait
   ```

**Fallbacks** (if firecrawl is unavailable or fails):
- Use `litellm_web_search` (WebSearch tool) for discovery — returns snippets, not full pages
- Use `WebFetch` only for specific known URLs (not for guessed URLs)
- If WebFetch fails (401, 404), do NOT retry — move on or use training knowledge

Create the output directory first: `mkdir -p /tmp/deep-research`

## Search Strategy

Use 2-3 different keyword variations per sub-topic to avoid blind spots from any
single query phrasing. Mix general and news-focused search terms. For instance,
searching "AI video generation tools 2026" AND "best text-to-video platforms
comparison" AND "Runway vs Kling vs Sora" will surface different source pools.

## What to Research

Find current, specific data: product names, pricing, capabilities, limitations,
comparisons, and real user experiences. Prefer sources from the last 12 months.
Prioritize: academic and institutional sources (.gov, .edu, peer-reviewed journals)
> industry reports and official docs > reputable news outlets > blogs > forums.

## Source Citation Rules

These are critical — the quality of the final report depends on traceable sourcing:
- Every major claim must cite a specific source: "[Source Name](URL), date"
- If only ONE source supports a claim, flag it: "(single source — unverified)"
- Cross-reference key findings: when 3+ sources agree, note the convergence
- Clearly separate established facts from inferences — use "Based on data from..."
  vs "It appears that..." or "This suggests..."
- When citing statistics, always include the year/quarter they refer to
- Aim for 8-15 unique sources per domain

## Output Requirements

Produce a structured markdown section titled "## {DOMAIN_NAME}" with:
- Key findings with inline source citations and publication dates
- Comparison tables where applicable
- Current limitations and workarounds
- Confidence rating per finding: High (3+ corroborating sources), Medium (2 sources),
  Low (single source or inference)
- Recommendations within this domain
- A source list at the end: numbered, with URL and one-line summary each

## Conflict Handling

When sources disagree, report BOTH views with attribution rather than picking a winner.
Flag the disagreement explicitly: "Source A (date) states X, while Source B (date) states Y."
Weight peer-reviewed or institutional sources over blogs and opinion pieces, but still
surface the dissenting view. Flag temporal conflicts — if an older source says X but a
newer source says Y, note the timeline and lean toward the newer source unless the older
one is more authoritative.

## Saturation

Stop searching for a sub-topic when:
- You have 3+ corroborating sources for a claim
- New searches return information you've already captured
- You've covered the core dimensions (what, who, how much, limitations)

## Length Constraint

Keep total output under 12,000 characters. Be specific and data-rich, not verbose.
Truncate background context in favor of concrete findings.

Today's date: {TODAY_DATE}
"""
)
```

All agents run concurrently. Dispatch them all in a single message.

### Step 2: Extract Specialist Outputs from JSONL

After all agents complete, extract their research text from the JSONL transcript files. Agents may hit the 32K output token limit and restart, producing multiple text blocks — the extraction must capture ALL of them, not just the longest one.

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
    all_texts = []
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
                                    if len(text) > 200:
                                        all_texts.append(text)
                except: pass
        # Concatenate all qualifying text blocks, separated by dividers
        combined = '\n\n---\n\n'.join(all_texts)
        outpath = f'/tmp/deep-extracts/{name}.md'
        with open(outpath, 'w') as f:
            f.write(combined)
        print(f'{name}: {len(combined)} chars from {len(all_texts)} blocks')
    except Exception as e:
        print(f'{name}: ERROR - {e}')
"
```

### Step 3: Coverage Gap Check (adaptive second pass)

Before synthesis, verify each domain produced substantive results. This is inspired by how Gemini checks coverage against its research plan — if a sub-topic is under-covered, it runs additional searches before synthesizing.

```bash
# Check which domains have thin or failed results
python3 -c "
import os
thin = []
for f in sorted(os.listdir('/tmp/deep-extracts')):
    if not f.endswith('.md'): continue
    path = os.path.join('/tmp/deep-extracts', f)
    size = os.path.getsize(path)
    domain = f.replace('.md','')
    if size < 1000:
        thin.append(domain)
        print(f'THIN: {domain} ({size} chars)')
    else:
        print(f'OK:   {domain} ({size} chars)')
if thin:
    print(f'\nDomains needing second pass: {thin}')
else:
    print(f'\nAll domains have sufficient coverage.')
"
```

If any domains returned thin results (<1000 chars), dispatch a **second-pass agent** for each, using different search terms and a more focused prompt. These second-pass agents should:
- Use broader/alternative search terms
- Try different angles on the same topic
- Fall back to training knowledge if web search continues to fail
- Target the specific gaps rather than re-researching the whole domain

After second-pass agents complete, re-extract and merge their outputs into the existing domain files.

### Step 4: Synthesize with Gemini via LiteLLM

Concatenate all extracted specialist outputs into a single context file, then send to Gemini for synthesis:

```bash
# Concatenate all specialist outputs
cat /tmp/deep-extracts/*.md > /tmp/deep-extracts/all_specialist_outputs.md

# Send to Gemini for synthesis
python3 /Users/craigverzosa/.claude/skills/deep-research/scripts/research.py \
  -q "Synthesize the following specialist research into a comprehensive, actionable report.

SYNTHESIS INSTRUCTIONS:
1. Cross-reference findings across domains — identify where specialists AGREE and where they CONTRADICT each other
2. When sources disagree, present both perspectives with source attribution. Do not silently pick a winner
3. Weight peer-reviewed and institutional sources over blogs and opinion pieces
4. Flag temporal conflicts — if an older source says X but a newer source says Y, note the timeline
5. If a claim is supported by only one source, mark it '(single source — treat with caution)'
6. Separate established facts from inferences — label estimates, projections, and opinions clearly
7. Assign confidence ratings (High/Medium/Low) to major conclusions based on source convergence
8. Produce the following sections:
   (a) Executive summary with the top 3-5 findings
   (b) Detailed findings organized by theme (not by domain — reorganize around insights)
   (c) Comparison matrix where applicable
   (d) Recommended approach / workflow / pipeline
   (e) Current limitations and open questions
   (f) Sources cited with dates — format: numbered list with [Title](URL) and one-line summary
   (g) Methodology — how many domains researched, approximate number of sources analyzed,
       sub-questions investigated, and any domains where coverage was thin

Original question: {USER_QUERY}" \
  -c /tmp/deep-extracts/all_specialist_outputs.md \
  -o ~/Documents/ObsidianNotes/Claude-Research/{OUTPUT_FILENAME}.md \
  --max-tokens 16000
```

Gemini's large context window handles all specialist outputs in a single call — no timeout risk, no subagent turn limits.

### Step 5: Enhance and Write to Obsidian

After Gemini returns the synthesis:
1. Read the output file
2. Prepend YAML frontmatter with `deep_mode: true` tag
3. Add wiki-links for cross-referencing
4. Report key findings to the user conversationally

#### Fallback

If Gemini synthesis fails (API error, rate limit), fall back to synthesizing directly in the main conversation window by reading all extracted specialist files and writing the report manually.

---

## Design Rationale

This skill uses a hybrid multi-agent architecture informed by how the major AI platforms implement deep research. Understanding these design choices helps explain why the skill works the way it does.

### How the Platforms Do It

| Dimension | OpenAI Deep Research | Gemini Deep Research | Perplexity Deep Research | Claude Research |
|---|---|---|---|---|
| **Model** | o3 (reasoning model) | Gemini 2.5 Pro / 3.1 Pro | Internal models | Claude Opus/Sonnet |
| **Architecture** | Single-agent, inline reasoning | Hierarchical agent, plan-first | Fully reactive loop | Tool-calling loop |
| **Query approach** | CoT decomposes inline | Explicit plan shown to user | No plan, iterative passes | Context-driven tool calls |
| **Search backend** | Bing + web browsing | Google Search | Proprietary index | Bing / third-party |
| **Breadth vs depth** | Depth-adaptive | Breadth-first (plan-driven) | Depth-first by default | Context-window managed |
| **Conflict handling** | Surfaces contradictions | Synthesis-dominant | Explicit when stark | Synthesis-dominant |
| **Stopping criteria** | Time/compute budget (5-30 min) | Plan completion | Search budget (dozens of queries) | Tool-call budget |
| **RAG pattern** | Iterative self-RAG | Hierarchical RAG | Fusion + iterative RAG | Iterative RAG |
| **Plan visibility** | Internal (reasoning trace) | External (user approval) | None | None |

### Why This Skill Uses a Hybrid Approach

**Multi-agent parallel decomposition** (like Anthropic's own multi-agent research system) gives breadth — each domain gets its own specialist agent that can search independently without competing for context window space.

**Research plan display** (borrowed from Gemini) gives the user control over the decomposition before expensive agent work begins.

**Adaptive coverage detection** (inspired by Gemini's plan-completion stopping and Perplexity's multi-pass approach) catches domains where agents failed or returned thin results, triggering a focused second pass.

**Gemini synthesis** (our unique addition) uses Gemini's massive context window to cross-reference all specialist outputs in a single pass — something no single Claude agent could do within its context limits. This is the "fusion RAG" step that Perplexity does internally.

**Conflict-aware synthesis prompts** (inspired by OpenAI's explicit contradiction surfacing) ensure the final report doesn't silently pick winners when sources disagree.

### Quality Rules (applies to all outputs)

These are the non-negotiable quality standards for every research report this skill produces. They are inspired by the best practices across deep research implementations and reflect what makes a report trustworthy vs. hand-wavy.

1. **Every claim needs a source.** No unsourced assertions in the final report. If the synthesis model can't trace a claim to a specialist's cited source, it gets cut or flagged as inference.
2. **Cross-reference findings.** If only one source says it, flag it as "(single source — unverified)." Convergence across 3+ independent sources = high confidence.
3. **Recency matters.** Prefer sources from the last 12 months. When using older sources, note the date explicitly.
4. **Acknowledge gaps.** If a sub-question couldn't be answered well, say so explicitly in the report rather than glossing over it. Thin coverage is better disclosed than hidden.
5. **Separate fact from inference.** Label estimates, projections, and opinions clearly. "Gartner reports 18% growth" (fact) vs. "This suggests the market will..." (inference).
6. **No hallucinated citations.** Specialist agents sometimes fabricate URLs or source names. The synthesis step should only cite sources that appear in the specialist outputs with real URLs.

### Key Lessons from the Architecture

1. **Firecrawl CLI as primary search tool**: Agents use `firecrawl search --scrape` via Bash for source discovery — it returns clean LLM-optimized markdown and handles JS-rendered pages, bypassing the WebFetch haiku dependency entirely. `litellm_web_search` is the fallback if firecrawl is unavailable. WebFetch is last resort for specific known URLs only.
2. **Extraction must handle token-limit restarts**: Agents that hit the 32K output limit restart and produce multiple text blocks. The extraction script must concatenate all blocks (>200 chars), not just take the longest one.
3. **Budget-based stopping is fragile**: Systems that stop based on a compute budget may halt while under-informed. The coverage gap check (Step 3) compensates by detecting thin results and triggering second-pass agents.
4. **No system truly solves contradiction handling**: All platforms struggle with conflicting sources. Explicitly instructing the synthesis model to surface disagreements (rather than silently resolving them) produces more trustworthy output.
5. **Multiple keyword variations per sub-topic**: A single search query creates a blind spot. Using 2-3 different phrasings (general + specific + comparative) per sub-question surfaces different source pools and reduces the chance of missing key data.

---

## Research Patterns

See [references/research-patterns.md](references/research-patterns.md) for detailed prompt patterns and multi-source workflows.
