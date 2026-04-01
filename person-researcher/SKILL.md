---
name: person-researcher
description: Research a person by name, LinkedIn URL, or company context — scrapes LinkedIn via firecrawl, runs deep web research, discovers personal interests and hobbies, cross-references existing Obsidian account notes, and produces a structured brief saved to the vault. Covers BOTH professional background AND personal profile (interests, hobbies, sports teams, alma mater, social media, charitable causes, gift ideas). Use whenever the user asks to research a person, look up someone's background, prep for a meeting with someone specific, review someone's LinkedIn, improve someone's LinkedIn profile, find out what someone likes, figure out gift ideas for a contact, or understand someone beyond their job title. Triggers on: "research [name]", "look up [person]", "LinkedIn review for [name]", "background on [name]", "who is [person] at [company]", "prep for meeting with [name]", "what does [name] like", "gift ideas for [name]", "personal interests of [name]", or any request combining a person's name with research, background, LinkedIn, meeting prep, relationship-building, or gift intent. Do NOT use for company research (use account-research), stock research (use stock-research), or general topic research (use deep-research).
---

## Why personal context matters

In sales and account management, the strongest relationships are built on understanding the whole person — not just their job title. Knowing someone's alma mater, favorite sports team, hobbies, or causes they care about creates natural rapport and shows genuine interest. This skill gathers both professional AND personal context so you can connect authentically.

## Steps

### Step 1: Parse the input

Extract from the user's prompt:
- Person's name (required)
- LinkedIn URL (if provided)
- Company name (if mentioned or inferrable from context)
- Email address (if provided — useful for finding social profiles)
- Context: is this for account/sales prep, coaching/career help, gift research, or general info?
- Any specific angle (e.g., "improve their LinkedIn", "background for call prep", "understand their role", "what do they like", "gift ideas")

### Step 2: Gather data (parallel where possible)

Launch these research tracks in parallel using subagents or parallel tool calls:

#### Track A: Professional Data

1. **LinkedIn scrape** (if URL provided): Use firecrawl-scrape on the LinkedIn URL to get profile data — current role, company, tenure, previous roles, education, skills, recent posts/activity, volunteer experience, causes they follow. If no LinkedIn URL is provided and none can be found via web search, note in the brief header: "⚠ LinkedIn data unavailable — profile sourced from web only" and flag the Professional Profile section accordingly. Do not present web-sourced role information as if it came from LinkedIn.

   LinkedIn is especially valuable for personal context because people often list:
   - **Volunteer Experience & Causes** — charities, nonprofits, board seats
   - **Education** — alma mater, Greek life, honors societies
   - **Skills & endorsements** — reveals what they take pride in
   - **Posts/activity** — what they share reveals personal passions beyond work
   - **Interests/groups** — industry groups but also hobby groups, alumni networks

2. **Professional web research**: Use WebSearch + WebFetch (or firecrawl-search) to find:
   - Recent news mentions, conference talks, blog posts
   - Company role/team context
   - Professional background beyond LinkedIn

#### Track B: Personal Data

3. **Social media & personal web research**: Search for the person across personal channels. Use firecrawl-search or WebSearch for each:
   - `"[Full Name]" [Company] site:x.com OR site:twitter.com` — X/Twitter profile, posts, interests
   - `"[Full Name]" [Company] site:instagram.com` — Instagram (often reveals hobbies, travel, food, pets)
   - `"[Full Name]" [Company] site:facebook.com` — Facebook (community involvement, family, interests)
   - `"[Full Name]" [Company] site:strava.com OR site:github.com OR site:medium.com` — Niche platforms (running/cycling, coding, writing)
   - `"[Full Name]" [Company] marathon OR triathlon OR golf OR volunteer OR charity OR board` — Activity-specific searches
   - `"[Full Name]" [Company] alumni OR graduation OR university` — Education and school pride
   - `"[Full Name]" blog OR podcast OR speaking` — Personal brand / thought leadership

   If the user provided an email address, also try:
   - Search the email handle (the part before @) across social platforms — people often reuse handles

   **Important:** Only gather information that is publicly available. Don't attempt to access private profiles, gated content, or anything requiring authentication. If a profile is private, note it as "private profile found but not accessible" and move on.

4. **Charitable / community involvement**: Search specifically for:
   - `"[Full Name]" nonprofit OR foundation OR charity OR volunteer OR "board of directors"`
   - `"[Full Name]" [hometown or alma mater] community` — local involvement
   - LinkedIn Volunteer Experience section (from Track A)

#### Track C: Internal Context

5. **Obsidian cross-reference**: Check if there are existing notes about this person or their company:
   - Search Obsidian vault with `mcp__obsidian__search_notes` for the person's name
   - Search for their company name in `Claude-Research/accounts/`
   - If found, read existing notes to avoid duplicating known info and to add context
   - Look for personal details already captured in call debriefs or meeting notes (people often mention personal things in passing — kids, vacations, hobbies, weekend plans)

6. **mem0 check**: Search mem0 for any stored facts about this person (`mcp__mem0__memory_search`)

### Step 3: Synthesize the brief

Produce a structured brief based on the context. The key addition is the **Personal Profile** section, which appears in all output formats.

**For sales/account prep:**
```
# [Name] — [Title] at [Company]

## Background
- Current role and tenure
- Previous relevant roles
- Education / alma mater

## Professional Profile
- Areas of responsibility
- Technical interests (from LinkedIn activity/posts)
- Communication style signals (if inferrable)

## Personal Profile
### Interests & Hobbies
- Sports (teams they follow, sports they play — running, golf, cycling, etc.)
- Hobbies (cooking, travel, photography, gaming, music, etc.)
- Alma mater & school pride (if evident from posts, gear in photos, alumni activity)
- Hometown / where they grew up (if publicly available)

### Social Media Presence
- X/Twitter: [@handle] — what they post about
- Instagram: [@handle] — themes (travel, food, family, fitness, etc.)
- Other platforms found (Strava, GitHub, Medium, personal blog)

### Community & Causes
- Charitable involvement (nonprofits, volunteer work, board seats)
- Causes they publicly support
- Community organizations

### Relationship-Building Context
- Conversation starters beyond work (based on discovered interests)
- Gift ideas (3-5 specific suggestions based on their interests, with price ranges)
- Shared interests with the user (if known from mem0)
- Things to avoid / be sensitive about (if any signals found)

## Okta Relevance
- What Okta products/solutions map to their role
- Pain points they likely face (based on role + company)
- Talking points tailored to their perspective

## Meeting Notes
- What we already know (from Obsidian/mem0)
- Open questions to explore (both professional and personal)
- Recommended approach
```

**For gift research** (when the user specifically asks about gifts or preferences):
```
# [Name] — Gift & Preferences Brief

## What We Know
- Interests and hobbies discovered
- Brands/products they mention or display in posts
- Causes they care about

## Gift Ideas
For each idea, include: what it is, why it fits them, where to get it, and approximate price.

### Thoughtful ($25-75)
- [3 ideas based on discovered interests]

### Premium ($75-200)
- [3 ideas based on discovered interests]

### Experience-Based
- [2-3 experience gifts — event tickets, classes, tastings]

### Charitable
- [1-2 donation-in-their-name options based on causes they support]

## Conversation Starters
- [5 non-work topics you can bring up naturally based on their interests]
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
Use a simplified version with Background + Professional Profile + Personal Profile + Key Findings.

### Step 4: Generate gift ideas (when applicable)

When the context involves relationship-building or gift research, put real thought into gift suggestions. Good gift ideas are:

- **Specific, not generic.** "A book about running" is weak. "Shoe Dog by Phil Knight (memoir about building Nike) — since they ran the Chicago Marathon" is strong.
- **Connected to discovered interests.** Every suggestion should trace back to something you actually found about the person.
- **Varied in type and price.** Include physical items, experiences, consumables, and charitable options.
- **Culturally appropriate.** Be mindful of dietary restrictions (if discovered), religious observances, and corporate gift policies.

If you couldn't find personal interests, be honest: "Limited personal data found — these are general suggestions based on their role/industry" and suggest safe options like high-quality notebooks, local food/coffee from their city, or a donation to a tech-industry nonprofit.

### Step 5: Save to Obsidian

Save using `mcp__obsidian__write_note`:
- **Sales context path:** `Claude-Research/accounts/[company]/people/[name].md`
- **Gift research path:** `Claude-Research/accounts/[company]/people/[name].md` (append if exists)
- **Coaching context path:** `Claude-Research/coaching/[name]-brief.md`
- **General path:** `Claude-Research/people/[name].md`

Frontmatter:
```yaml
date: YYYY-MM-DD
tags: [person-research, [company-name]]
source: claude-code
project: [inferred-project]
```

If a note already exists at that path, append with a dated section header rather than overwriting. This preserves the history of what was known about someone over time.

### Step 6: Print summary

Print a condensed version to the terminal:
- Background + key talking points or improvement highlights
- Personal highlights (top 3 interests/hobbies found)
- Gift ideas (if applicable — top 3)
- Tell the user where the full note was saved
- Flag any personal data that was thin: "Personal profile is limited — [name] has a low public footprint. Consider asking about interests directly in your next conversation."
