---
name: competitive-intel
description: "Living competitive intelligence tracker for IAM vendors. Maintains evergreen battlecard docs and periodic landscape summaries in Obsidian. Two modes: (1) landscape — refreshes all tracked vendors with feature matrix, battlecards, and 'what changed' digest, (2) quick — single-vendor call-prep brief with landmines and differentiation points. Scrapes 10 sources per vendor in parallel, synthesizes with Gemini. Default vendors: Ping, ForgeRock, Entra, CyberArk, SailPoint, Lumos, ConductorOne. Use when the user asks about competitors, wants competitive updates, needs call prep for a competitive deal, asks 'what's new with [vendor]', wants battlecard updates, or requests a landscape refresh. Triggers on: 'competitive intel', 'competitor update', 'battlecard', 'landscape update', 'what's new with [vendor]', 'prep for competitive deal', 'competitive brief on [vendor]', or any request combining a competitor name with competitive or battlecard intent. For IAM vendor battlecards only — use deep-research for competitive analysis outside the IAM space. NOT for general company research (use account-research or deep-research)."
---

# Competitive Intelligence

Maintain living competitive battlecards and landscape summaries for IAM vendors.

## How It Works

The skill uses `scripts/research_competitive.py` to:
1. Scrape 10 data sources per vendor in parallel (news, blog, newsroom, changelog, GitHub, dev blog, Crunchbase, G2, job postings, analyst mentions)
2. Compare fresh data against existing battlecards (hybrid change detection via Gemini)
3. Synthesize updated battlecards and landscape summaries via Gemini (LiteLLM)
4. Write to `~/Documents/ObsidianNotes/Claude-Research/competitive-intel/`

## Usage

```bash
# Landscape mode (default) — all 7 vendors
python3 <skill-path>/scripts/research_competitive.py

# Quick mode — single vendor call prep
python3 <skill-path>/scripts/research_competitive.py --mode quick "Ping"

# Override vendor list
python3 <skill-path>/scripts/research_competitive.py --competitors "Ping,Delinea,BeyondTrust"

# Quick mode for non-default vendor
python3 <skill-path>/scripts/research_competitive.py --mode quick "Delinea"
```

Replace `<skill-path>` with: `/Users/craigverzosa/.claude/skills/competitive-intel`

## Modes

| Mode | What it does | Output |
|------|-------------|--------|
| `landscape` (default) | Scrapes all vendors, updates battlecards, produces landscape summary | Per-vendor battlecard files + `landscape-{YYYY-MM}.md` |
| `quick` | Scrapes one vendor, produces call-prep brief, updates battlecard | Brief to stdout + battlecard file updated |

## Default Vendors

Ping Identity, ForgeRock, Microsoft Entra, CyberArk, SailPoint, Lumos, ConductorOne

Override with `--competitors "slug1,slug2,..."`. Non-registry vendors are supported (scraping uses Google discovery fallback).

## Invocation

Parse the user's request to determine mode and vendor:

**Landscape triggers:** "update battlecards", "competitive landscape", "competitor update", "what's new in IAM"
**Quick triggers:** "prep for [vendor] deal", "what's new with [vendor]", "competitive brief on [vendor]"

Then dispatch:

```
Task tool (Bash subagent, model: "sonnet"):
  prompt: |
    Run: python3 /Users/craigverzosa/.claude/skills/competitive-intel/scripts/research_competitive.py [--mode quick "VENDOR"] [--competitors "OVERRIDES"]
    Report the output paths from stdout and any scraper failures from stderr.
```

## After Running

1. Report output file paths
2. In landscape mode: summarize the most notable changes across vendors, highlight market trends
3. In quick mode: present the call-prep brief directly (it's on stdout)
4. Mention any scraper failures from stderr
5. User can open reports in Obsidian for full view

## Output Location

- Battlecards: `~/Documents/ObsidianNotes/Claude-Research/competitive-intel/{vendor-slug}.md`
- Landscape: `~/Documents/ObsidianNotes/Claude-Research/competitive-intel/landscape-{YYYY-MM}.md`

## Dependencies

- Python 3 with `requests`, `beautifulsoup4`, `openai` (auto-installed if missing)
- LiteLLM credentials in `~/.claude-litellm.env`
- Obsidian vault at `~/Documents/ObsidianNotes/`
