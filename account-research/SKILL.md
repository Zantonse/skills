---
name: account-research
description: "Structured account research for Sales Engineering prep. Scrapes 10 public data sources in parallel, synthesizes with Claude Sonnet (extended thinking) into an SE-ready brief, and writes to the Obsidian vault. Derives business goals from signals, detects identity/security stack, and generates discovery questions and talk tracks. Use when the user asks to research a company, prep for a call, build an account overview, or do prospect research. Triggers on: 'account research', 'research [company]', 'prep for [company]', 'account overview', 'prospect research', 'who is [company]', 'what does [company] do', 'research account', or any request combining a company name with sales, SE, or account prep intent. Also trigger when the user mentions preparing for a customer call or needs a company brief."
---

# Account Research

Perform structured account research for Sales Engineering and write SE-ready briefs to the Obsidian vault.

## How It Works

The skill uses `scripts/research_account.py` to:
1. Resolve the company name to a domain
2. Scrape 5-10 public data sources concurrently (company website, news, funding, job postings, tech stack, reviews, SEC filings, Glassdoor, industry news, competitor references)
3. Send all scraped context to Claude Sonnet with extended thinking (via LiteLLM) for deep synthesis
4. Format the output with Obsidian YAML frontmatter and wiki-links
5. Save to `~/Documents/ObsidianNotes/Claude-Research/accounts/`

All scrapers run in parallel via ThreadPoolExecutor.

## Usage

```bash
python3 <skill-path>/scripts/research_account.py "Snowflake"
python3 <skill-path>/scripts/research_account.py "Snowflake" --angle "evaluating workforce identity"
python3 <skill-path>/scripts/research_account.py "Snowflake" --depth quick
python3 <skill-path>/scripts/research_account.py "Collibra" --depth full --angle "competitive displacement from Ping"
```

Replace `<skill-path>` with: `/Users/craigverzosa/.claude/skills/account-research`

## Depth Levels

| Depth | Purpose | Sources | Output |
|-------|---------|---------|--------|
| `quick` | First call prep | 5 core | ~1-2 pages |
| `deep` (default) | Full SE prep | 8 sources | ~3-5 pages |
| `full` | Proposal/RFP | All 10 | ~5-8 pages |

## Invocation

Parse the user's request to extract:
1. **Company name** (required)
2. **Angle** (optional — any context about the opportunity, e.g., "competitive displacement", "evaluating workforce identity")
3. **Depth** (optional — quick/deep/full, default deep)

Then dispatch:

```
Task tool (Bash subagent, model: "sonnet"):
  prompt: |
    Run: python3 /Users/craigverzosa/.claude/skills/account-research/scripts/research_account.py "{COMPANY}" --angle "{ANGLE}" --depth {DEPTH}
    Report the output path from stdout and any source failures from stderr.
```

## Multi-Company: Parallel Dispatch

When the user asks to research multiple companies, dispatch one subagent per company using the Task tool. All subagents run concurrently.

Example: user says "research Snowflake, Collibra, and Datadog" -> dispatch 3 Bash subagents simultaneously.

## Evolving Briefs

If a previous brief exists for the company, the script automatically reads it and deepens the analysis rather than regenerating from scratch. Manual notes in a `## My Notes` section are preserved.

## After Running

1. Report the output file path(s) to the user
2. Summarize key findings conversationally: company snapshot, top business goals, main pain point hypotheses, and recommended discovery questions
3. Mention any data sources that failed (from stderr)
4. For multi-company runs, provide a brief comparison
5. The user can open the report(s) in Obsidian for the full detailed view

## Output Location

`~/Documents/ObsidianNotes/Claude-Research/accounts/{company-slug}-{YYYY-MM}.md`

## Data Sources (10 total, all scraped concurrently)

| Source | Data | Depth |
|--------|------|-------|
| Company Website | About page, careers/hiring signals | all |
| Google News RSS | Recent headlines, M&A, funding | all |
| Crunchbase (via Google) | Funding, investors, leadership, employees | all |
| Job Postings (via Google) | Tech stack from requirements (identity/security keywords) | all |
| BuiltWith / HackerTarget | HTTP headers, tech stack detection | all |
| G2 / TrustRadius (via Google) | Identity/security tool reviews and usage | deep+ |
| SEC EDGAR | 10-K filings, risk factors | deep+ |
| Glassdoor (via Google) | Engineering culture, team size, tech signals | deep+ |
| Industry News (Google News) | Regulatory/compliance/security pressures | full |
| Competitor References (via Google) | Public case studies with identity vendors | full |

## Dependencies

- Python 3 with `requests`, `beautifulsoup4`, `openai` (auto-installed if missing)
- LiteLLM credentials in `~/.claude-litellm.env`
- Obsidian vault at `~/Documents/ObsidianNotes/`
