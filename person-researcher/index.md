---
name: person-researcher
description: Research a person by name, LinkedIn URL, or company context — scrapes LinkedIn via firecrawl, runs deep web research, cross-references existing Obsidian account notes, and produces a structured brief saved to the vault. Use whenever the user asks to research a person, look up someone's background, prep for a meeting with someone specific, review someone's LinkedIn, or improve someone's LinkedIn profile. Triggers on: "research [name]", "look up [person]", "LinkedIn review for [name]", "background on [name]", "who is [person] at [company]", "prep for meeting with [name]", or any request combining a person's name with research, background, LinkedIn, or meeting prep intent. Do NOT use for company research (use account-research), stock research (use stock-research), or general topic research (use deep-research).
---

## Steps

### Step 1: Parse the input

Extract from the user's prompt:
- Person's name (required)
- LinkedIn URL (if provided)
- Company name (if mentioned or inferrable from context)
- Context: is this for account/sales prep, coaching/career help, or general info?
- Any specific angle (e.g., "improve their LinkedIn", "background for call prep", "understand their role")

### Step 2: Gather data (parallel where possible)

Use parallel subagents or tool calls to:

1. **LinkedIn scrape** (if URL provided): Use firecrawl-scrape on the LinkedIn URL to get profile data — current role, company, tenure, previous roles, education, skills, recent posts/activity. If no LinkedIn URL is provided and none can be found via web search, note in the brief header: "⚠ LinkedIn data unavailable — profile sourced from web only" and flag the Professional Profile section accordingly. Do not present web-sourced role information as if it came from LinkedIn.

2. **Web research**: Use WebSearch + WebFetch (or firecrawl-search) to find:
   - Recent news mentions, conference talks, blog posts
   - Company role/team context
   - Professional background beyond LinkedIn

3. **Obsidian cross-reference**: Check if there are existing notes about this person or their company:
   - Search Obsidian vault with `mcp__obsidian__search_notes` for the person's name
   - Search for their company name in `Claude-Research/accounts/`
   - If found, read existing notes to avoid duplicating known info and to add context

4. **mem0 check**: Search mem0 for any stored facts about this person (`mcp__mem0__memory_search`)

### Step 3: Synthesize the brief

Produce a structured brief based on the context:

**For sales/account prep:**
```
# [Name] — [Title] at [Company]
## Background
- Current role and tenure
- Previous relevant roles
- Education/certifications
## Professional Profile
- Areas of responsibility
- Technical interests (from LinkedIn activity/posts)
- Communication style signals (if inferrable)
## Okta Relevance
- What Okta products/solutions map to their role
- Pain points they likely face (based on role + company)
- Talking points tailored to their perspective
## Meeting Notes
- What we already know (from Obsidian/mem0)
- Open questions to explore
- Recommended approach
```

**For coaching/career help:**
```
# [Name] — LinkedIn Review & Career Brief
## Current Profile Summary
- Headline, about section, experience highlights
## Strengths
- What's working well on their profile
## Improvement Areas
- Specific recommendations with rewritten examples
  - Headline suggestions (3 options)
  - About section rewrite
  - Experience bullet improvements
## Career Context
- Industry trends relevant to their role
- Positioning recommendations
```

**For general info:**
Use a simplified version with Background + Professional Profile + Key Findings.

### Step 4: Save to Obsidian

Save using `mcp__obsidian__write_note`:
- **Sales context path:** `Claude-Research/accounts/[company]/people/[name].md`
- **Coaching context path:** `Claude-Research/coaching/[name]-brief.md`
- **General path:** `Claude-Research/people/[name].md`

Frontmatter:
```yaml
date: YYYY-MM-DD
tags: [person-research, [company-name]]
source: claude-code
project: [inferred-project]
```

If a note already exists at that path, append with a dated section header rather than overwriting.

### Step 5: Print summary

Print a condensed version to the terminal (Background + key talking points or improvement highlights). Tell the user where the full note was saved.
