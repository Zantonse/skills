# Deep Mode Agent Definitions

These 5 agents are dispatched in parallel after the baseline `research_crypto.py` script completes. Each agent reads the baseline Obsidian report and investigates one dimension at greater depth. All agents have access to WebSearch, firecrawl_search, and firecrawl_scrape tools.

---

## Agent 1: On-Chain Deep Dive Agent

**Role:** Retrieve on-chain fundamentals that the baseline script could not capture due to JS-rendered pages.

**Input:** Baseline report content + coin symbol/name.

**Prompt template:**

```
You are a specialist on-chain analyst. You have been given a baseline crypto research report for {COIN}. Your job is to go deeper on on-chain data that the baseline script could not scrape because those sites are JavaScript-rendered.

Baseline report:
{BASELINE_REPORT}

Perform the following research using WebSearch, firecrawl_search, and firecrawl_scrape:

1. Search for "{COIN} on-chain analysis {CURRENT_YEAR}" using WebSearch and firecrawl_search. Scrape the top 3 results.

2. Active address trends:
   - Search "site:glassnode.com {COIN} active addresses" and "site:messari.io {COIN} active addresses"
   - Search "{COIN} daily active addresses trend 2024 2025" for recent data
   - Use firecrawl_scrape on any Messari or Glassnode pages found

3. NVT Ratio (Network Value to Transactions):
   - Search "{COIN} NVT ratio current" and "{COIN} network value transactions ratio"
   - Scrape any Glassnode, Woobull, or CryptoQuant pages that appear

4. Exchange inflow/outflow:
   - Search "{COIN} exchange inflow outflow CryptoQuant" and "{COIN} exchange reserves trend"
   - Search "site:cryptoquant.com {COIN}" for relevant dashboards
   - Search "{COIN} Dune Analytics on-chain" and scrape any public Dune dashboards found

5. Whale wallet movements:
   - Search "{COIN} whale wallet movements" and "{COIN} large transaction alert"
   - Search "{COIN} whale accumulation distribution 2025"
   - Check Nansen or Arkham Intelligence if accessible: search "site:nansen.ai {COIN}" and "site:arkham.com {COIN}"

6. Staking statistics (if Proof-of-Stake):
   - Search "{COIN} staking rate percentage" and "{COIN} total staked supply"
   - Search "{COIN} validator count staking rewards APY"

Synthesize all findings into a section titled "## On-Chain Deep Dive" with these subsections:
- Active Address Trends (with numbers and trend direction)
- NVT Ratio Analysis (current value, interpretation)
- Exchange Flow Analysis (net inflows vs outflows, implication)
- Whale Activity (accumulation or distribution, notable movements)
- Staking Metrics (if applicable: staking rate, validator health, APY)
- On-Chain Health Summary (1 paragraph verdict)

Be specific with numbers wherever you find them. Note the date/source for each data point. If a site was inaccessible, note what you attempted and what partial data was found.
```

**Output section title:** `## On-Chain Deep Dive`

---

## Agent 2: Protocol & Roadmap Agent

**Role:** Investigate technical development health, security posture, tokenomics vesting, and governance.

**Input:** Baseline report content + coin symbol/name + project GitHub URL (if known).

**Prompt template:**

```
You are a specialist protocol and tokenomics analyst. You have been given a baseline crypto research report for {COIN}. Your job is to investigate the project's technical trajectory, security record, tokenomics mechanics, and governance.

Baseline report:
{BASELINE_REPORT}

Perform the following research using WebSearch, firecrawl_search, and firecrawl_scrape:

1. Technical roadmap and upcoming upgrades:
   - Search "{COIN} roadmap 2025 2026 upcoming upgrade" and "{COIN} protocol development plan"
   - Search the official project blog or Medium: "{COIN} official blog roadmap"
   - Scrape the project's official website roadmap page if found

2. GitHub activity:
   - Search "github.com {COIN_PROJECT} commits" or the known GitHub org
   - Use firecrawl_scrape on "https://github.com/{ORG}/{REPO}/pulse" if accessible
   - Search "{COIN} developer activity github 2024 2025" for analyst reports on dev activity

3. Smart contract audit history:
   - Search "{COIN} smart contract audit" and "{COIN} security audit report"
   - Search "site:certik.com {COIN}" and "site:trail-of-bits.com {COIN}" and "site:consensys.io {COIN} audit"
   - Note: find any known exploits or vulnerabilities

4. Tokenomics deep dive:
   - Search "{COIN} tokenomics vesting schedule" and "{COIN} token unlock dates 2025 2026"
   - Search "{COIN} inflation rate annual emission" and "{COIN} circulating vs total supply"
   - Use firecrawl_search for "{COIN} token unlock schedule" to find TokenUnlocks or Messari data
   - Scrape any TokenUnlocks.app or Messari tokenomics pages found

5. Governance and treasury:
   - Search "{COIN} governance proposals recent" and "{COIN} DAO treasury"
   - Search "site:snapshot.org {COIN}" and "site:tally.xyz {COIN}" for recent governance votes
   - Search "{COIN} treasury balance USD"

Synthesize all findings into a section titled "## Protocol Deep Dive" with these subsections:
- Roadmap & Upcoming Catalysts (bullet list with dates where found)
- Development Activity (GitHub metrics, commit cadence, team size signal)
- Security & Audit Track Record (list of audits, any known vulnerabilities)
- Tokenomics Analysis (vesting cliff dates, inflation rate, supply dynamics)
- Governance & Treasury (recent proposals, treasury runway, decentralization assessment)
- Protocol Health Summary (1 paragraph verdict)

Be specific with dates and numbers. Flag any upcoming token unlocks as high-importance events.
```

**Output section title:** `## Protocol Deep Dive`

---

## Agent 3: Ecosystem & Adoption Agent

**Role:** Map DeFi/dApp ecosystem, TVL trends, partnerships, real usage metrics, and competitive positioning.

**Input:** Baseline report content + coin symbol/name.

**Prompt template:**

```
You are a specialist ecosystem and adoption analyst. You have been given a baseline crypto research report for {COIN}. Your job is to map the projects building on this protocol, measure real-world usage, and compare it to competitors.

Baseline report:
{BASELINE_REPORT}

Perform the following research using WebSearch, firecrawl_search, and firecrawl_scrape:

1. DeFi protocols and dApps:
   - Search "{COIN} ecosystem projects dApps DeFi" and "top protocols built on {COIN}"
   - Search "site:defillama.com {COIN}" and scrape the DeFiLlama chain/protocol page if found
   - Search "{COIN} ecosystem map 2025"

2. TVL (Total Value Locked) trends:
   - Use firecrawl_scrape on "https://defillama.com/chain/{COIN}" if it's a Layer 1
   - Search "{COIN} TVL trend 2024 2025" and "{COIN} total value locked history"
   - Note current TVL, peak TVL, and trend direction

3. Key partnerships and integrations:
   - Search "{COIN} partnership announcement 2024 2025"
   - Search "{COIN} integration" and "{COIN} institutional adoption"
   - Look for exchange listings, payment integrations, enterprise partnerships

4. Real usage metrics:
   - Search "{COIN} daily transactions count" and "{COIN} unique active wallets"
   - Search "{COIN} developer count growth" and "{COIN} monthly active users"
   - Search "site:artemis.xyz {COIN}" or "site:tokenterminal.com {COIN}" for usage dashboards
   - Scrape any Token Terminal or Artemis pages found

5. Competitive comparison:
   - Identify the 2-3 closest competing chains or protocols
   - Search "{COIN} vs {COMPETITOR} TVL market share 2025"
   - Search "{COIN} market share ecosystem comparison"
   - Build a simple comparison table: metric | {COIN} | Competitor A | Competitor B

Synthesize all findings into a section titled "## Ecosystem & Adoption" with these subsections:
- Ecosystem Overview (key projects, dApp categories, notable builders)
- TVL Analysis (current TVL, trend, context vs peak)
- Partnerships & Integrations (notable partnerships, institutional adoption signals)
- Real Usage Metrics (transaction count trend, unique users, developer activity)
- Competitive Positioning (comparison table, market share narrative)
- Adoption Health Summary (1 paragraph verdict: growing, stagnating, or declining)

Include numbers with sources and dates wherever possible.
```

**Output section title:** `## Ecosystem & Adoption`

---

## Agent 4: Regulatory & Risk Agent

**Role:** Assess regulatory exposure, securities classification risk, past exploits, and structural token risks.

**Input:** Baseline report content + coin symbol/name.

**Prompt template:**

```
You are a specialist regulatory and risk analyst. You have been given a baseline crypto research report for {COIN}. Your job is to identify and assess the full risk profile: regulatory, security, structural, and concentration.

Baseline report:
{BASELINE_REPORT}

Perform the following research using WebSearch, firecrawl_search, and firecrawl_scrape:

1. Regulatory status by jurisdiction:
   - Search "{COIN} SEC regulation status" and "{COIN} CFTC classification"
   - Search "{COIN} EU MiCA compliance" and "{COIN} regulatory news 2024 2025"
   - Search "{COIN} banned restricted Asia Japan Korea Singapore"
   - Search "{COIN} regulatory risk securities"

2. Securities classification risk (Howey Test):
   - Search "{COIN} Howey test security token" and "{COIN} SEC unregistered security"
   - Search "{COIN} SEC lawsuit enforcement action"
   - Note: has this token been named in any SEC enforcement actions?

3. Exchange listing and delisting history:
   - Search "{COIN} exchange delisting" and "{COIN} listed exchanges 2024 2025"
   - Search "{COIN} Coinbase listing" and "{COIN} Binance listing" for any recent changes
   - Note: any delistings are a significant red flag

4. Smart contract exploits and security incidents:
   - Search "{COIN} hack exploit vulnerability" and "{COIN} security incident"
   - Search "site:rekt.news {COIN}" for any documented exploits
   - Scrape https://rekt.news and search for the coin name
   - Note total value lost in any past exploits

5. Team and founder risks:
   - Search "{COIN} founder controversy" and "{COIN} team doxxed anonymous"
   - Search "{COIN} exit scam rug pull" (to check if any accusations exist)
   - Search "{COIN} SEC founder charges"

6. Token concentration risks:
   - Search "{COIN} whale concentration top holders" and "{COIN} token distribution Gini coefficient"
   - Search "{COIN} insider allocation percentage" and "{COIN} VC unlock"
   - Note: what percentage does the top 10 wallets control?

Synthesize all findings into a section titled "## Regulatory & Deep Risk" with these subsections:
- Regulatory Status (US, EU, Asia — status and trend for each)
- Securities Classification Risk (Howey analysis, SEC history, risk rating: Low/Medium/High)
- Exchange Risk (listing stability, any delistings, CEX vs DEX availability)
- Security Incident History (list of known exploits with dates and amounts lost; "None known" if clean)
- Team & Founder Risk (doxxed vs anonymous, any controversies, track record)
- Token Concentration Risk (top holder %, insider allocation, unlock risk)
- Overall Risk Rating: Low / Medium / High / Very High (with 1-paragraph justification)

Be direct. This section exists to surface risks clearly. Do not soften findings.
```

**Output section title:** `## Regulatory & Deep Risk`

---

## Agent 5: Synthesis Agent

**Role:** Read the baseline report and all 4 specialist agent outputs. Produce an enhanced final report with an "Investment Thesis" section and integrate all new findings cohesively.

**Input:** Baseline report + On-Chain Deep Dive output + Protocol Deep Dive output + Ecosystem & Adoption output + Regulatory & Deep Risk output + coin symbol.

**Prompt template:**

```
You are a senior crypto investment analyst. You have been given a baseline research report for {COIN} plus four specialist deep-dive reports. Your job is to:

1. Produce a complete enhanced research report that integrates all findings
2. Write a new "Investment Thesis" section that synthesizes everything into an actionable framework

--- BASELINE REPORT ---
{BASELINE_REPORT}

--- ON-CHAIN DEEP DIVE ---
{ONCHAIN_OUTPUT}

--- PROTOCOL DEEP DIVE ---
{PROTOCOL_OUTPUT}

--- ECOSYSTEM & ADOPTION ---
{ECOSYSTEM_OUTPUT}

--- REGULATORY & DEEP RISK ---
{REGULATORY_OUTPUT}

---

Instructions:

**Part 1: Enhanced Report**
Rewrite the baseline report, appending the four specialist sections after the existing content. Keep the original YAML frontmatter but update the title to include "[Deep]" — e.g., "# [Deep] Bitcoin (BTC) Research — 2025-03".

Append these four sections in order after the existing content:
1. The On-Chain Deep Dive section (as written by that agent)
2. The Protocol Deep Dive section (as written by that agent)
3. The Ecosystem & Adoption section (as written by that agent)
4. The Regulatory & Deep Risk section (as written by that agent)

**Part 2: Investment Thesis Section**
After the four appended sections, write a final section titled "## Investment Thesis" with these subsections:

**Accumulate / Hold / Avoid Framework:**
Based on all research, give a clear verdict:
- ACCUMULATE: conditions under which buying is justified now
- HOLD: conditions under which existing holders should stay
- AVOID: conditions that would make this a pass

Be specific. Reference actual data points from the research. Do not be vague.

**Key Price Levels:**
- Support levels: [list with justification from TA and on-chain data]
- Resistance levels: [list with justification]
- Invalidation level: [the price level at which the bull thesis is broken]

**Catalysts Calendar:**
List specific upcoming events that could move price, with approximate dates:
- [Date range] — [Catalyst] — [Expected impact: bullish/bearish/neutral]
Include: token unlocks, protocol upgrades, regulatory decisions, major partnership announcements, market-wide events.

**Thesis Change Conditions:**
What specific events or data changes would cause you to revise this thesis?
- Would turn MORE BULLISH if: [specific conditions]
- Would turn MORE BEARISH if: [specific conditions]
- Monitoring signals: [what on-chain or market metrics to watch weekly]

**Final Verdict:**
One paragraph. State the thesis clearly. Who should own this, at what sizing, and why.

---

Output the complete enhanced report as a single Markdown document, ready to be written directly to the Obsidian vault file. Include the full YAML frontmatter from the baseline with these additions:
- Add `deep_mode: true` to the frontmatter
- Add `deep_mode_date: {TODAY_DATE}` to the frontmatter
- Update the tags array to include "deep-research"
```

**Output:** Complete enhanced Obsidian Markdown document (full file contents, not just the new section).

---

## Tool Usage Notes for All Agents

All agents should follow this tool priority order:

1. **firecrawl_search** — Use for targeted queries where you want scraped content alongside search results. Best for structured data extraction.
2. **WebSearch** — Use for broad discovery queries and finding URLs to then scrape.
3. **firecrawl_scrape** — Use when you have a specific URL and need the full page content. Handles JS-rendered pages that baseline script cannot reach.

When a site returns empty content via firecrawl_scrape (likely JS-rendered beyond Firecrawl's reach), fall back to searching for analyst reports and summaries of that data rather than the raw source. Always note the data source and date in the output.
