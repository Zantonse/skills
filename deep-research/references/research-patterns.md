# Deep Research Patterns

## Multi-Source Research Workflow

For thorough research, gather context from multiple sources before sending to Gemini:

### Step 1: Web Search (gather raw data)
```bash
# Use firecrawl_search or web search to find relevant pages
# Scrape key pages for full content
# Save scraped content to temp files
```

### Step 2: Compile Context
```bash
# Combine all gathered data into context files
# Include: web pages, internal docs, previous research, user notes
```

### Step 3: Deep Analysis
```bash
python3 scripts/research.py \
  --query "Your research question" \
  --context gathered-data.md internal-notes.md \
  --mode general \
  --output findings.md
```

## Sales Account Research Workflow

### Quick Account Overview
```bash
python3 scripts/research.py \
  --query "Build a comprehensive account overview for [Company Name]" \
  --mode account \
  --output accounts/company-overview.md
```

### With Pre-gathered Intel
```bash
# First: scrape company website, recent news, SEC filings, job postings
# Then: feed as context
python3 scripts/research.py \
  --query "Build account overview for [Company Name]" \
  --context website-scrape.md news-articles.md job-postings.md \
  --mode account \
  --output accounts/company-overview.md
```

## Subagent Integration

When called from a Claude Code subagent (Task tool), use the `--json` flag for structured output:

```bash
python3 scripts/research.py \
  --query "Research question" \
  --json
```

This returns JSON with `query`, `model`, `mode`, and `result` fields for easy parsing.

## Prompt Patterns for Better Results

### Company Research
- "What is [Company]'s current technology stack and infrastructure?"
- "Analyze [Company]'s recent earnings calls for technical priorities"
- "Compare [Company]'s approach to [topic] vs their competitors"

### Technical Deep Dives
- "Explain [technology] architecture patterns with trade-offs"
- "What are the current best practices for [approach] in 2026?"
- "Compare [option A] vs [option B] for [use case] with specific criteria"

### Market Research
- "What is the current competitive landscape for [category]?"
- "What trends are driving adoption of [technology] in [industry]?"
- "Size the market opportunity for [product] in [vertical]"
