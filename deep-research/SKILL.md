---
name: deep-research
description: "Parallel specialist agent teams for comprehensive research with Gemini synthesis. Always uses the full agent team pipeline (4-6 parallel research agents + coverage gap check + Gemini cross-domain synthesis). Use when: (1) the user asks a deep, complex, or multi-faceted question requiring thorough analysis, (2) researching a company for a sales account overview or prospect briefing, (3) any request containing 'deep research', 'research this', 'deep dive', 'thorough analysis', or 'account overview', (4) comparing technologies, architectures, or approaches in depth, (5) market research, competitive analysis, or industry landscape questions, (6) when a subagent needs deep analytical capability beyond web search. Triggers on: 'deep research', 'research', 'account overview', 'company research', 'deep dive', 'analyze thoroughly', 'competitive analysis', 'market research', or any question that requires synthesis across many data points. NOT for SE-specific account research with Okta sales context (use account-research). NOT for IAM vendor battlecards (use competitive-intel). NOT for stock/crypto analysis (use stock-research or crypto-research). Use deep-research for general knowledge questions, technology comparisons, and broad research that doesn't fit a specialized skill."
---

# Deep Research

Parallel specialist agent teams for comprehensive research, with Gemini synthesis. Every research request uses the full agent team pipeline — there is no "simple" mode.

**Architecture:** Decompose the question into 4-6 research domains → dispatch parallel specialist agents (each scrapes the web independently) → content-aware gap check with LLM evaluation → cross-agent reasoning to find blind spots → optional targeted follow-up agents → synthesize all findings through Gemini's large context window → save to Obsidian vault. Optional `--depth 2` mode adds a post-synthesis refinement pass.

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

**Check for depth flag.** If the user included `--depth 2` (or said "go deeper", "be thorough", "iterative"), note that a post-synthesis refinement pass will run after the initial report. Default is depth 1 (single pass).

Present the plan to the user:
```
Researching across 6 sub-questions:
1. AI avatar / talking head platforms
2. AI voice synthesis tools
3. AI video generation for B-roll
4. Lip sync & face animation
5. Workflow orchestration & pipeline tools
6. Cost & throughput analysis

Depth: {1 or 2} ({"single pass" or "with post-synthesis refinement"})
Dispatching specialist agents now. (Reply to adjust before results come in.)
```

Then proceed immediately — don't block on user confirmation. If the user responds with adjustments before agents finish, incorporate them in a second-pass round.

### Step 1: Dispatch Specialist Agents in Parallel

For each domain, dispatch a `general-purpose` subagent with `model: "sonnet"` and `max_turns: 25`:

```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  max_turns=25,
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
single query phrasing. Mix general and news-focused search terms.

## What to Research

Find current, specific data: product names, pricing, capabilities, limitations,
comparisons, and real user experiences. Prefer sources from the last 12 months.
Prioritize: academic and institutional sources (.gov, .edu, peer-reviewed journals)
> industry reports and official docs > reputable news outlets > blogs > forums.

## Source Citation Rules

- Every major claim must cite a specific source: "[Source Name](URL), date"
- If only ONE source supports a claim, flag it: "(single source — unverified)"
- Cross-reference key findings: when 3+ sources agree, note the convergence
- Clearly separate established facts from inferences
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
Flag the disagreement explicitly.

## Saturation

Stop searching when you have 3+ corroborating sources for a claim, new searches return
information you've already captured, and you've covered the core dimensions.

## Length Constraint

Keep total output under 12,000 characters. Be specific and data-rich, not verbose.

Today's date: {TODAY_DATE}
"""
)
```

All agents run concurrently. **Dispatch them all in a single message.**

#### Agent Progress Monitoring

After dispatching all background agents, **poll their status every 20 seconds** using `TaskOutput(task_id=AGENT_ID, block=false, timeout=1000)`. Print one-line status updates:

```
"Progress: 2/6 agents complete | domain3 still searching | domain5 extracting..."
"✓ Domain 2 (AI voice synthesis) complete — 4,200 chars, 11 sources found"
```

**8-minute wall-clock timeout:** If agents haven't returned within 8 minutes, collect whatever output exists from completed agents and proceed. Print: `"Pipeline timeout: 4/6 agents completed. Proceeding with available data."`

### Step 2: Extract Specialist Outputs from JSONL

After all agents complete (or timeout fires), extract research text from JSONL transcripts. Agents may hit the 32K output token limit and restart — the extraction must capture ALL text blocks, not just the longest one.

```bash
mkdir -p /tmp/deep-extracts && python3 -c "
import json, os

agents = {
    'domain1': '{AGENT1_ID}',
    'domain2': '{AGENT2_ID}',
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
        combined = '\n\n---\n\n'.join(all_texts)
        outpath = f'/tmp/deep-extracts/{name}.md'
        with open(outpath, 'w') as f:
            f.write(combined)
        print(f'{name}: {len(combined)} chars from {len(all_texts)} blocks')
    except Exception as e:
        print(f'{name}: ERROR - {e}')
"
```

### Step 3: Content-Aware Coverage Gap Check

Evaluate each domain's output for **substantive quality**, not just character count.

#### Phase 3a: Quick Size Pre-screen

Domains with `< 100 chars` are agent failures — go directly to second-pass. Domains with `< 500 chars` are flagged as thin.

#### Phase 3b: LLM Quality Evaluation

Dispatch a **single evaluation agent** (`model: "sonnet"`, `max_turns: 5`) that reads ALL domain outputs and rates each one against its research sub-question:

- **Coverage score (1-5):** 1=empty/irrelevant, 2=tangential, 3=partial, 4=solid with minor gaps, 5=comprehensive
- **Gap description:** What specific aspect is missing or weak?
- **Suggested follow-up search:** If score < 4, what specific query would fill the gap?

#### Phase 3c: Context-Enriched Second-Pass

For any domain scored < 4 (or < 100 chars from pre-screen), dispatch a **second-pass agent** that receives:

1. The **first-pass output** (even if thin) — so it doesn't re-search what was already found
2. The **evaluator's specific gap description** — so it targets what's missing
3. **URLs discovered by other domain agents** — so it can drill into cross-domain leads
4. The **evaluator's suggested follow-up search query** — as a starting point

Second-pass agents use `max_turns: 20` and target gaps rather than re-researching the whole domain. After completion, merge outputs with originals.

### Step 3.5: Cross-Agent Reasoning (Blind Spot Detection)

**Runs AFTER gap-filling, BEFORE synthesis.** This is the key intelligence layer that turns independent parallel research into a coherent whole.

Dispatch a single reasoning agent (`model: "sonnet"`, `max_turns: 8`) that reads ALL domain outputs together:

1. **Contradiction Detection:** Where do two specialists make conflicting claims?
2. **Blind Spot Analysis:** What important angle did ALL specialists miss?
3. **Single Most Valuable Follow-Up:** One specific search query that would most improve the report.
4. **Source Quality Audit:** Scan for potentially hallucinated citations.
5. **Synthesis Guidance:** 2-3 sentences for the synthesis model about what to watch for.

Output saved to `/tmp/deep-extracts/_cross_agent_reasoning.md`.

**If a critical blind spot is identified with a specific follow-up search**, dispatch one final targeted agent (`max_turns: 15`) to fill it. Save to `/tmp/deep-extracts/_blindspot_fill.md`.

### Step 4: Synthesize with Gemini via LiteLLM

Concatenate all specialist outputs **plus the cross-agent reasoning analysis**, then send to Gemini:

```bash
cat /tmp/deep-extracts/*.md > /tmp/deep-extracts/all_specialist_outputs.md

python3 /Users/craigverzosa/.claude/skills/deep-research/scripts/research.py \
  -q "Synthesize the following specialist research into a comprehensive, actionable report.

SYNTHESIS INSTRUCTIONS:
1. Cross-reference findings across domains — identify where specialists AGREE and CONTRADICT
2. IMPORTANT: A cross-agent reasoning analysis is included (section '_cross_agent_reasoning').
   Address contradictions it found, acknowledge unfilled blind spots, omit suspicious citations.
3. Present both perspectives when sources disagree. Do not silently pick a winner.
4. Flag temporal conflicts and single-source claims.
5. Assign confidence ratings (High/Medium/Low) to major conclusions.
6. Produce sections: (a) Executive summary, (b) Detailed findings by theme, (c) Comparison matrix,
   (d) Recommended approach, (e) Limitations and open questions, (f) Sources cited, (g) Methodology

Original question: {USER_QUERY}" \
  -c /tmp/deep-extracts/all_specialist_outputs.md \
  -o ~/Documents/ObsidianNotes/Claude-Research/{OUTPUT_FILENAME}.md \
  --max-tokens 16000
```

### Step 5: Enhance and Write to Obsidian

After Gemini returns the synthesis:
1. Read the output file
2. Prepend YAML frontmatter with `deep_mode: true` tag
3. Add wiki-links for cross-referencing
4. Report key findings to the user conversationally

**Fallback:** If Gemini synthesis fails, synthesize directly in the main conversation window.

### Step 5.5: Post-Synthesis Refinement (Depth 2 Only)

**ONLY runs if user requested `--depth 2` or said "go deeper".** Skip for depth 1 (default).

1. Dispatch an evaluation agent to read the synthesis and identify 1-2 most significant remaining gaps (weakest evidence, missing critical comparisons).
2. If gaps found, dispatch 1-2 targeted agents (`max_turns: 15`, background) for each.
3. Re-run synthesis with original context plus refinement outputs.
4. Add "Refinement Notes" subsection to Methodology explaining what was added.

If evaluation returns "NO REFINEMENT NEEDED", skip re-synthesis.

---

## Pipeline Summary

```
Step 0:  Decompose → 4-6 sub-questions, show plan, check depth flag
Step 1:  Dispatch parallel agents (max_turns=25, 8-min wall-clock timeout)
         ↳ Poll progress every 20s, report to user
Step 2:  Extract outputs from JSONL transcripts
Step 3:  Content-aware gap check:
         3a: Size pre-screen (catch crashes)
         3b: LLM quality evaluation (rate 1-5 per domain)
         3c: Context-enriched second-pass for weak domains
Step 3.5: Cross-agent reasoning:
         - Contradiction detection
         - Blind spot analysis
         - Source quality audit
         ↳ Optional: one targeted blind-spot fill agent
Step 4:  Gemini synthesis (all outputs + reasoning analysis)
Step 5:  Obsidian frontmatter + wiki-links + report to user
Step 5.5: [Depth 2 only] Post-synthesis refinement:
         - Evaluate report for remaining gaps
         - Dispatch 1-2 targeted agents
         - Re-synthesize with new data
```

---

## Design Rationale

This skill uses a hybrid multi-agent architecture informed by how the major AI platforms implement deep research.

### How the Platforms Do It

| Dimension | OpenAI Deep Research | Gemini Deep Research | Perplexity | **This Skill** |
|---|---|---|---|---|
| **Architecture** | Single-agent, inline reasoning | Hierarchical, plan-first | Reactive loop | Parallel agents + cross-agent reasoning + synthesis |
| **Breadth vs depth** | Depth-adaptive | Breadth-first | Depth-first | Breadth-first + iterative depth (reasoning + optional depth 2) |
| **Conflict handling** | Surfaces contradictions | Synthesis-dominant | Explicit when stark | Explicit: cross-agent reasoning detects before synthesis |
| **Stopping criteria** | Time/compute budget | Plan completion | Search budget | Content-aware LLM eval + time budget (8 min + max_turns) |
| **Gap detection** | Implicit (model decides) | Plan completion | Multi-pass saturation | LLM quality eval + cross-agent blind spot detection |

### Why This Skill Uses a Hybrid Approach

- **Multi-agent parallel decomposition** gives breadth — each domain gets its own context window.
- **Research plan display** (from Gemini) gives user control before expensive work begins.
- **Content-aware gap detection** uses an LLM to evaluate quality, catching "long but irrelevant" outputs.
- **Context-enriched second passes** give retry agents the first-pass output, gap descriptions, and cross-domain URLs.
- **Cross-agent reasoning** reads all outputs together to find contradictions, blind spots, and suspicious citations.
- **Gemini synthesis** handles all outputs in a single large-context pass with reasoning guidance.
- **Iterative refinement** (depth 2) evaluates the final report and fills remaining weak spots.
- **Agent progress reporting** provides visibility through periodic status polling.
- **Time budgets** (`max_turns: 25` + 8-min wall-clock) prevent runaway agents.

### Quality Rules

1. **Every claim needs a source.** No unsourced assertions in the final report.
2. **Cross-reference findings.** Single-source = "(single source — unverified)." 3+ sources = high confidence.
3. **Recency matters.** Prefer last 12 months. Note dates on older sources.
4. **Acknowledge gaps.** Thin coverage is better disclosed than hidden.
5. **Separate fact from inference.** Label estimates, projections, and opinions clearly.
6. **No hallucinated citations.** Cross-agent reasoning audits for suspicious sources.

### Key Lessons

1. **Firecrawl CLI as primary search tool** — clean markdown, handles JS-rendered pages.
2. **Extraction must handle token-limit restarts** — concatenate all blocks >200 chars.
3. **Content-aware stopping beats character counting** — a 2K output of noise is worse than 500 chars of solid findings.
4. **Cross-agent reasoning catches what parallel agents can't** — contradictions and cross-domain blind spots.
5. **Context-enriched second passes outperform blind retries** — targeted gap-filling vs. redundant re-searching.
6. **Time budgets prevent pipeline stalls** — `max_turns` + wall-clock timeout force progress.

---

## Research Patterns

See [references/research-patterns.md](references/research-patterns.md) for detailed prompt patterns and multi-source workflows.
