---
name: news-research
description: |
  Search news sources for specific topics and produce content-ready takes with LinkedIn angles.
  Dispatches 5-6 parallel source-specialized agents (tech press, business, security niche,
  social/community, analyst) then synthesizes into 5 angle categories: Headlines, Trend,
  Contrarian Take, Domain Connection, and LinkedIn Angles. Use this skill whenever the user
  mentions "news research", "what's in the news about", "latest news on", "news digest",
  "trending in", "find articles about", "news for LinkedIn", "industry news", "what happened
  this week in", "news brief", or any request combining a topic with news, articles, or
  trending intent. Also trigger when the user wants content ideas from current events, asks
  "what should I post about", or wants to know what's happening in a specific industry or
  domain. Saves to Obsidian and shows results inline.
---

# News Research — Source-Specialized Agent Teams + Content-Ready Synthesis

Search current news across 5-6 source types in parallel, then synthesize into content-ready
takes with LinkedIn angles. Every article is real, sourced, and dated. No fabricated links.

**Architecture:** Topic decomposition into source-specialized agents → parallel search →
coverage gap check → Gemini synthesis into 5 angle categories → Obsidian + inline output.

## Input

The user provides a **topic** and optionally:
- `--timeframe`: 24h | 7d (default) | 30d | 90d
- `--sources`: all (default) | tech | business | security | social | analyst | world

Parse the topic from the user's message. If ambiguous, ask: "What specific topic should I
search for?"

## Step 0: Present the Research Plan

Before dispatching, show the plan:

```
Researching: "[TOPIC]" | Timeframe: [X] days

Dispatching 5 source agents:
1. Tech Press (TechCrunch, Verge, Ars Technica, Wired, VentureBeat)
2. Business/Finance (Bloomberg, Reuters, Fortune, Forbes)
3. Security/Identity (Dark Reading, CSO Online, SC Media, Krebs)
4. Social/Community (Reddit, Hacker News, LinkedIn, X)
5. Analyst/Research (Gartner blog, Forrester, IDC)
[6. World/General (BBC, AP, NPR) — if non-tech topic]

Searching now. I'll synthesize findings into content-ready takes.
```

Then proceed immediately — don't wait for user confirmation.

## Step 1: Dispatch Source-Specialized Agents

Launch all agents in parallel using `Task` tool with `run_in_background: true` and
`model: "sonnet"` (per CLAUDE.md global config).

Each agent gets this prompt structure (customize the source list per agent type):

```
You are a news research specialist focused on [SOURCE TYPE] sources.

Topic: [TOPIC]
Timeframe: Last [X] days (today is [DATE])

## Search Strategy

Use firecrawl CLI via Bash for all searches. Create output dir first: mkdir -p /tmp/news-research

1. Search with 3 keyword variations to avoid blind spots:
   - Variation 1 (direct): "[topic] [source-specific keywords]"
   - Variation 2 (broader): "[related terms] [industry context]"
   - Variation 3 (recency): "[topic] 2026" or "[topic] this week"

   For each variation:
   ```
   firecrawl search "[query]" --scrape --limit 3 -o /tmp/news-research/[agent]-search-[N].json --json
   ```

2. For the most promising articles, scrape the full page:
   ```
   firecrawl scrape "[url]" -o /tmp/news-research/[agent]-article-[N].md
   ```

Fallbacks: litellm_web_search if firecrawl fails. WebFetch only for specific known URLs.

## Source Focus: [SOURCE TYPE]
[Insert source-specific site list and keyword guidance — see below]

## Output Format

Return structured markdown:

## [SOURCE TYPE] News Findings

### 1. [Article Title]
- **Source:** [Publication name]
- **Date:** [Publication date]
- **URL:** [Full URL]
- **Summary:** [2-3 sentence summary of the article's key points]
- **Why it matters:** [1 sentence on significance]
- **Confidence:** [HIGH if article scraped and read / MEDIUM if snippet only]

### 2. [Next article...]
[Repeat for top 3-5 most relevant articles]

### Source Coverage Assessment
- Searches performed: [N]
- Articles found: [N]
- Articles fully read: [N]
- Coverage quality: [Strong / Moderate / Thin]

## Quality Rules
- Only include articles from the last [X] days
- Every article must have a real, verifiable URL
- Never fabricate or guess URLs
- If an article is paywalled, note it and summarize from the available snippet
- Prefer articles with specific data, quotes, or announcements over opinion pieces
- If you find fewer than 2 relevant articles, say so honestly rather than padding with
  tangentially related content
```

### Agent-Specific Source Guidance

**Agent 1: Tech Press**
Sites: TechCrunch, The Verge, Ars Technica, Wired, VentureBeat, ZDNET, The Information
Keywords: product launches, funding, acquisitions, technical capabilities
Search tip: Add "announced" or "launches" to find concrete news vs opinion

**Agent 2: Business/Finance**
Sites: Bloomberg, Reuters, WSJ, Fortune, Forbes, Business Insider, Financial Times
Keywords: market impact, revenue, investment, IPO, earnings, regulatory
Search tip: Add "billion" or "market" to surface business-impact stories

**Agent 3: Security/Identity Niche**
Sites: Dark Reading, CSO Online, SC Media, KrebsOnSecurity, BleepingComputer, The Record
Keywords: vulnerability, breach, CISO, zero trust, identity, compliance, regulation
Search tip: Add "incident" or "advisory" for breaking security news

**Agent 4: Social/Community**
Sites: Reddit (r/cybersecurity, r/netsec, r/sysadmin, r/technology), Hacker News, LinkedIn
Keywords: discussion, opinion, reaction, "what do you think"
Search tip: Search reddit.com and news.ycombinator.com directly. Capture upvote counts
and top comments as sentiment signals.

**Agent 5: Analyst/Research**
Sites: Gartner blog, Forrester blog, IDC, McKinsey, Deloitte Insights, Harvard Business Review
Keywords: report, forecast, prediction, framework, market share, quadrant
Search tip: Add "2026" to filter for recent analyst content

**Agent 6: World/General** (dispatch only if topic is non-tech or user requests)
Sites: BBC, AP News, NPR, Al Jazeera, The Guardian, NY Times
Keywords: regulation, policy, government, international, economy
Search tip: Focus on policy/regulatory angles that connect to tech

## Step 2: Extract Agent Outputs

After all agents complete, extract their research text from the JSONL transcript files:

```python
# Same extraction pattern as /deep-research
import json, os

agents = {
    'tech-press': '[AGENT_ID]',
    'business': '[AGENT_ID]',
    'security': '[AGENT_ID]',
    'social': '[AGENT_ID]',
    'analyst': '[AGENT_ID]',
}

base_path = '[TASK_OUTPUT_DIR]'

for name, agent_id in agents.items():
    filepath = f'{base_path}/{agent_id}.output'
    all_texts = []
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
    with open(f'/tmp/news-research/{name}.md', 'w') as f:
        f.write(combined)
```

## Step 3: Coverage Gap Check

Check each agent's output size. If any returned <500 chars, dispatch a second-pass agent
with broader search terms or alternative sources.

```bash
for f in /tmp/news-research/*.md; do
    size=$(wc -c < "$f")
    name=$(basename "$f" .md)
    if [ "$size" -lt 500 ]; then
        echo "THIN: $name ($size chars) — needs second pass"
    else
        echo "OK: $name ($size chars)"
    fi
done
```

## Step 4: Synthesize with Gemini

Concatenate all agent outputs and send to Gemini via the deep-research synthesis script:

```bash
cat /tmp/news-research/tech-press.md \
    /tmp/news-research/business.md \
    /tmp/news-research/security.md \
    /tmp/news-research/social.md \
    /tmp/news-research/analyst.md \
    > /tmp/news-research/all_findings.md

python3 ~/.claude/skills/deep-research/scripts/research.py \
  -q "Synthesize the following news research into a content-ready briefing.

TOPIC: [TOPIC]
TIMEFRAME: Last [X] days
DATE: [TODAY]

Produce these 5 sections:

## 1. THE HEADLINES
The top 3-5 most significant stories across all sources. For each:
- What happened (1 sentence)
- Why it matters (1 sentence)
- Source + date + URL

Rank by significance, not recency. If sources disagree on the significance of a story,
note the disagreement.

## 2. THE TREND
What pattern is emerging across multiple articles? Look for:
- 3+ sources pointing in the same direction
- A shift from previous consensus
- Something accelerating or decelerating
Write as a single paragraph that connects the dots. Cite the specific articles that
form the pattern.

## 3. THE CONTRARIAN TAKE
The minority opinion, the overlooked risk, or the 'everyone is wrong about this' angle.
Find the article or thread that challenges the dominant narrative. If no genuine contrarian
view exists, say so — do not fabricate one. This section drives the most LinkedIn engagement
because it provokes thinking.

## 4. THE DOMAIN CONNECTION
How this topic connects to identity security, AI governance, or enterprise security
specifically. Even if the topic is general (e.g., 'AI regulation'), find the identity
angle. If the user's topic IS identity/security, go deeper — what does this mean for
practitioners, not just vendors?

## 5. YOUR LINKEDIN ANGLES
3 draft post hooks ready to write from. Each one:
- Hook sentence (pattern-interrupt opener that stops the scroll)
- Why this matters (2 sentences connecting to the reader's world)
- Your take (1 sentence opinion — take a position)
- Engagement question (end with a question that invites comments)

Format each as a ready-to-expand outline, not a full post.

## SOURCE LIST
Numbered list of every article cited, with: [N] Title — Source (Date) — URL

RULES:
- Only cite articles that appear in the source data below
- Never fabricate URLs or article titles
- If a section has insufficient data, say so rather than padding
- Prefer specificity over breadth — 3 well-analyzed stories beat 10 summaries
- Include publication dates on everything — readers need to know how fresh this is" \
  -c /tmp/news-research/all_findings.md \
  -o ~/Documents/ObsidianNotes/Claude-Research/news-[TOPIC-SLUG]-[YYYY-MM].md \
  --max-tokens 8000
```

## Step 5: Save and Present

1. **Prepend YAML frontmatter** to the Obsidian file:
```yaml
---
date: [TODAY]
tags:
  - news-research
  - [topic-specific tags]
source: claude-code
project: general-research
type: news-digest
---
```

2. **Show results inline** — read the saved file and present the 5 sections conversationally.
   Highlight the LinkedIn angles specifically since that's the primary use case.

3. **Close with:** "Full briefing saved to Obsidian at `Claude-Research/news-[topic]-[date].md`.
   Want me to expand any of the LinkedIn angles into a full draft post?"

## Fallback

If Gemini synthesis fails (API error, rate limit), synthesize directly in the main
conversation by reading all agent output files and producing the 5-section format inline.

If firecrawl is unavailable across all agents, fall back to `litellm_web_search` for
each source category, acknowledging that results will be snippet-level rather than
full-article summaries.

## Quality Principles

1. **Every URL must be real.** Never generate, guess, or reconstruct URLs. If you can't
   confirm the URL, cite the article title and source name without a link.

2. **Recency matters.** Default to 7-day window. Flag anything older than the requested
   timeframe explicitly.

3. **Source diversity is the point.** The value of 5 parallel agents is 5 different
   perspectives. If all agents return the same 3 articles, that's convergence (note it).
   If they return different articles, that's coverage (the desired state).

4. **Contrarian takes must be genuine.** Do not manufacture disagreement. If consensus is
   strong across all sources, say: "No significant contrarian view found — consensus is
   unusually strong on this topic, which is itself notable."

5. **LinkedIn angles should be opinionated.** A post that says "this is interesting" gets
   no engagement. A post that says "everyone is thinking about this wrong because..." gets
   comments. Push the user toward a position.
