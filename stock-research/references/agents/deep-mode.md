# Deep Mode Agent Definitions

These 5 agents are dispatched in parallel after the baseline stock research script has run.
Each agent receives the baseline report content, the ticker symbol, and its role instructions.
All agents use `model: "sonnet"` and `subagent_type: "general-purpose"`.

---

## Agent 1: Fundamentals & Valuation Agent

### Role
Extend the baseline report's financial data with deeper valuation context, historical comparisons, and multiple valuation models. The goal is to answer: "Is this stock cheap or expensive relative to its own history and intrinsic value?"

### What to Read from the Baseline Report
- Current P/E, P/S, P/B, EV/EBITDA multiples
- Revenue and earnings growth rates
- Analyst price targets
- Balance sheet summary (debt, cash, FCF)

### Research Steps

**Step 1 — SEC EDGAR (10-K / 10-Q)**
Use `firecrawl_scrape` on the SEC EDGAR full-text search to locate the most recent 10-K or 10-Q:
```
https://efts.sec.gov/LATEST/search-index?q="{TICKER}"&dateRange=custom&startdt={YYYY-01-01}&enddt={YYYY-12-31}&forms=10-K,10-Q
```
Then scrape the filing landing page and extract:
- Management Discussion & Analysis (MD&A) key highlights
- Risk factors section (top 5 most material)
- Any updated financial guidance mentioned in the filing

**Step 2 — GuruFocus Intrinsic Value**
Use `firecrawl_scrape` on:
```
https://www.gurufocus.com/term/iv_dcf_share/{TICKER}/Intrinsic-Value-DCF-Earnings-Based
```
Extract:
- DCF intrinsic value estimate
- Margin of safety percentage
- 10-year revenue and earnings growth assumptions used

**Step 3 — Simply Wall St (valuation)**
Use `firecrawl_search` or `WebSearch` for:
```
site:simplywall.st {TICKER} intrinsic value fair value
```
Extract any publicly visible fair value estimate and the methodology described.

**Step 4 — PEG Ratio and Forward Estimates (Zacks)**
Use `firecrawl_scrape` on:
```
https://www.zacks.com/stock/quote/{TICKER}/detailed-earning-estimates
```
Extract:
- Forward EPS estimates for current and next fiscal year
- Long-term earnings growth rate estimate
- PEG ratio (calculate as forward P/E divided by 5-year EPS growth rate if not shown directly)
- EPS estimate revision trend: how many analysts revised up vs. down in the last 30 days

**Step 5 — Historical Valuation Averages (Macrotrends)**
Use `firecrawl_scrape` on:
```
https://www.macrotrends.net/stocks/charts/{TICKER-SLUG}/{COMPANY-SLUG}/pe-ratio
```
Extract the 5-year and 10-year average P/E. Then compare current P/E to historical average to determine if the stock is at a premium or discount to its own history.

### Output Format

Produce a markdown section with this structure:

```markdown
## Fundamentals & Valuation (Deep)

### Intrinsic Value Estimates
| Model | Estimate | vs. Current Price | Source |
|-------|----------|-------------------|--------|
| DCF (GuruFocus) | $X.XX | X% discount/premium | GuruFocus |
| Fair Value (Simply Wall St) | $X.XX | X% discount/premium | Simply Wall St |
| Analyst Consensus Target | $X.XX | X% upside/downside | Yahoo/Finviz |

### Valuation vs. Historical Average
| Metric | Current | 5-Yr Avg | 10-Yr Avg | Verdict |
|--------|---------|----------|-----------|---------|
| P/E | X.Xx | X.Xx | X.Xx | Cheap / Fair / Expensive |
| P/S | X.Xx | X.Xx | X.Xx | ... |
| EV/EBITDA | X.Xx | X.Xx | X.Xx | ... |

### PEG & Forward Estimates
- Forward P/E: X.Xx (FY{YEAR} EPS estimate: $X.XX)
- Long-term EPS growth rate: X%
- PEG ratio: X.Xx (below 1 = potentially undervalued on growth basis)
- EPS revision trend (last 30 days): X upgrades, X downgrades

### SEC Filing Highlights (Most Recent 10-K/10-Q)
**MD&A Key Points:**
- [Point 1]
- [Point 2]
- [Point 3]

**Top Risk Factors:**
1. [Risk 1]
2. [Risk 2]
3. [Risk 3]

### Valuation Verdict
[2-3 sentence synthesis: Is the stock cheap or expensive on multiple frameworks? What does the historical comparison suggest?]
```

---

## Agent 2: Earnings & Management Agent

### Role
Surface what company leadership is actually saying — not just the numbers, but the tone, confidence level, forward guidance, and strategic narrative from the most recent earnings call. Management communication quality is a leading indicator.

### What to Read from the Baseline Report
- Most recent quarterly EPS and revenue (beat/miss vs. estimates)
- Revenue and earnings growth rates
- Analyst consensus and price targets
- Any existing mentions of guidance in the baseline

### Research Steps

**Step 1 — Earnings Call Transcript (Motley Fool)**
Motley Fool publishes free, scrapable earnings call transcripts. Use `firecrawl_scrape` with:
```
https://www.fool.com/earnings-call-transcripts/?symbol={TICKER}
```
Or use `WebSearch` for:
```
"{TICKER}" earnings call transcript site:fool.com {CURRENT_QUARTER}
```
Then scrape the most recent transcript page. Extract:
- Management's prepared remarks summary (CEO/CFO opening statements)
- Forward guidance: revenue and EPS guidance for next quarter and full year
- Guidance vs. prior guidance: was it raised, lowered, or maintained?
- Tone language: words like "accelerating," "headwinds," "uncertainty," "confident," "cautious"
- Key strategic initiatives mentioned (new products, markets, cost programs)

**Step 2 — Earnings Revisions (Zacks)**
Use `firecrawl_scrape` on:
```
https://www.zacks.com/stock/quote/{TICKER}/consensus-estimate-trend
```
Extract:
- Direction of EPS estimate revisions over the last 7, 30, and 60 days
- Zacks Rank (1-5: Strong Buy to Strong Sell) and the reason for the rank
- Whether revisions are broad (many analysts moving) or isolated

**Step 3 — Analyst Reaction to Earnings (Google News / WebSearch)**
Use `WebSearch` for:
```
{TICKER} earnings reaction analyst upgrade downgrade price target change {CURRENT_MONTH} {CURRENT_YEAR}
```
Extract any post-earnings analyst actions: upgrades, downgrades, price target raises or cuts, and the stated reasoning.

**Step 4 — Earnings History (StockAnalysis)**
Use `firecrawl_scrape` on:
```
https://stockanalysis.com/stocks/{TICKER}/forecast/
```
Extract the last 8 quarters of EPS surprises (beat/miss and magnitude) to establish the company's earnings quality and consistency track record.

### Output Format

Produce a markdown section with this structure:

```markdown
## What Management Is Saying (Deep)

### Most Recent Earnings Call — [Quarter] [Year]
**EPS:** $X.XX (beat/missed by $X.XX vs. estimate of $X.XX)
**Revenue:** $X.XXB (beat/missed by X%)

### Forward Guidance
| Metric | Next Quarter Guidance | Full Year Guidance | vs. Prior Guidance |
|--------|----------------------|--------------------|--------------------|
| Revenue | $X.XX–X.XX B | $X.XX–X.XX B | Raised / Maintained / Lowered |
| EPS | $X.XX–X.XX | $X.XX–X.XX | Raised / Maintained / Lowered |

### Management Tone Assessment
**Overall tone:** [Confident / Cautious / Mixed]
**Key themes mentioned:**
- [Theme 1 with direct quote or paraphrase]
- [Theme 2]
- [Theme 3]

**Notable quotes:**
> "[Direct quote from CEO or CFO about the most significant issue]"

> "[Direct quote about guidance or a specific risk/opportunity]"

### Strategic Initiatives Highlighted
- [Initiative 1: brief description and management's stated confidence level]
- [Initiative 2]
- [Initiative 3]

### Earnings Revision Trend
| Period | EPS Revisions Up | EPS Revisions Down | Net Direction |
|--------|------------------|--------------------|---------------|
| Last 7 days | X | X | Up / Down / Flat |
| Last 30 days | X | X | Up / Down / Flat |
| Last 60 days | X | X | Up / Down / Flat |

**Zacks Rank:** X/5 — [Rank Label]

### Earnings Quality (Last 8 Quarters)
| Quarter | EPS Estimate | EPS Actual | Surprise % |
|---------|-------------|------------|------------|
| [Q] | $X.XX | $X.XX | +X% |
...

**Beat rate:** X/8 quarters | **Average surprise:** X%

### Post-Earnings Analyst Actions
- [Firm]: [Upgraded/Downgraded/PT raised/PT cut] to $X — "[Reason]"
- [Firm]: [Action] — "[Reason]"

### Management Credibility Assessment
[2-3 sentence synthesis: Does management consistently deliver on guidance? Are they raising or lowering the bar? What is the market's trust level based on price reactions to earnings?]
```

---

## Agent 3: Competitive Moat Agent

### Role
Assess the durability of the company's competitive advantage using Porter's Five Forces and quantitative peer comparison. Determine whether the business has a genuine moat or is competing in a structurally difficult industry.

### What to Read from the Baseline Report
- Industry and sector classification
- Revenue, margins, and profitability metrics
- Any existing peer/competitor mentions
- Market cap and business description

### Research Steps

**Step 1 — Identify Closest Peers**
Use `WebSearch` for:
```
{TICKER} main competitors peer comparison {INDUSTRY}
```
Identify the 3-5 closest publicly traded competitors by business model and market cap.

**Step 2 — Peer Metrics Comparison (Finviz Screener)**
Use `firecrawl_scrape` on Finviz's screener filtered to the same industry:
```
https://finviz.com/screener.ashx?v=111&f=ind_{INDUSTRY_CODE}&o=marketcap
```
Extract: P/E, P/S, gross margin, operating margin, revenue growth, ROE, debt/equity for the top 5-6 companies in the sector.

**Step 3 — Gross Margin Trend (Macrotrends)**
Use `firecrawl_scrape` on:
```
https://www.macrotrends.net/stocks/charts/{TICKER-SLUG}/{COMPANY-SLUG}/gross-profit-margin
https://www.macrotrends.net/stocks/charts/{TICKER-SLUG}/{COMPANY-SLUG}/return-on-equity
```
Extract 5-year trend. A widening gross margin over time is one of the strongest signals of a strengthening moat.

**Step 4 — Market Share and Competitive Position (WebSearch + Firecrawl)**
Use `WebSearch` for:
```
{COMPANY} market share {YEAR} industry report
{COMPANY} competitive advantage moat analysis
```
Use `firecrawl_scrape` on any relevant industry research pages or analyst notes that appear in results. Extract any market share estimates or qualitative competitive analysis.

**Step 5 — Moat Indicators Research (WebSearch)**
Use `WebSearch` for specific moat signals:
```
{COMPANY} switching costs customers
{COMPANY} network effects
{COMPANY} patents intellectual property moat
{COMPANY} brand value intangible assets
```
Synthesize findings into the five moat categories: cost advantage, switching costs, network effects, intangible assets (brand/patents/licenses), efficient scale.

**Step 6 — Analyst Moat Commentary (Morningstar if accessible)**
Use `WebSearch` for:
```
{TICKER} Morningstar moat rating economic moat
```
Or use `firecrawl_scrape` on any accessible Morningstar page. Note Morningstar's moat rating (None / Narrow / Wide) if findable.

### Output Format

Produce a markdown section with this structure:

```markdown
## Competitive Moat & Peer Analysis (Deep)

### Morningstar Economic Moat Rating
**Moat:** [Wide / Narrow / None / Not rated]
**Moat Trend:** [Stable / Widening / Narrowing]
*Source: Morningstar (or "Not available — see analysis below")*

### Porter's Five Forces Assessment
| Force | Level | Key Factors |
|-------|-------|-------------|
| Threat of New Entrants | Low / Med / High | [Capital requirements, regulatory barriers, brand loyalty, etc.] |
| Bargaining Power of Suppliers | Low / Med / High | [Supplier concentration, substitutes available, etc.] |
| Bargaining Power of Buyers | Low / Med / High | [Customer concentration, price sensitivity, switching costs] |
| Threat of Substitutes | Low / Med / High | [Alternative products, disruption risk] |
| Industry Rivalry | Low / Med / High | [Number of competitors, differentiation, price wars] |

**Overall Industry Attractiveness:** [Low / Moderate / High]

### Moat Sources
| Moat Type | Present? | Evidence |
|-----------|----------|---------|
| Cost Advantage | Yes / No / Partial | [Evidence] |
| Switching Costs | Yes / No / Partial | [Evidence] |
| Network Effects | Yes / No / Partial | [Evidence] |
| Intangible Assets (Brand/Patents) | Yes / No / Partial | [Evidence] |
| Efficient Scale | Yes / No / Partial | [Evidence] |

**Moat Verdict:** [Wide / Narrow / None] — [1-2 sentence justification]

### Peer Comparison Table
| Metric | {TICKER} | [Peer 1] | [Peer 2] | [Peer 3] | [Peer 4] |
|--------|----------|----------|----------|----------|----------|
| Market Cap | $XB | $XB | $XB | $XB | $XB |
| Revenue Growth (YoY) | X% | X% | X% | X% | X% |
| Gross Margin | X% | X% | X% | X% | X% |
| Operating Margin | X% | X% | X% | X% | X% |
| P/E | X.Xx | X.Xx | X.Xx | X.Xx | X.Xx |
| P/S | X.Xx | X.Xx | X.Xx | X.Xx | X.Xx |
| ROE | X% | X% | X% | X% | X% |
| Debt/Equity | X.Xx | X.Xx | X.Xx | X.Xx | X.Xx |

**Relative Position:** {TICKER} ranks [X/5] on gross margin, [X/5] on growth, [X/5] on valuation.

### Gross Margin & ROE Trend (5 Years)
| Year | Gross Margin | ROE |
|------|-------------|-----|
| [Y-4] | X% | X% |
| [Y-3] | X% | X% |
| [Y-2] | X% | X% |
| [Y-1] | X% | X% |
| [Current] | X% | X% |

**Trend:** [Widening / Stable / Contracting] — [1 sentence interpretation]

### Competitive Position Summary
[3-4 sentences: What is the company's competitive advantage (or lack of one)? Is the moat durable or under threat? How does it stack up against peers on the metrics that matter most for this industry?]
```

---

## Agent 4: Catalyst & Risk Deep Dive Agent

### Role
Build a complete picture of what could move the stock significantly in the next 6-18 months — both upside catalysts and downside risks. Go beyond the standard risk factors to find specific, time-bound events and structural vulnerabilities.

### What to Read from the Baseline Report
- Current price and analyst price targets
- Industry and sector
- Any existing risk mentions
- Insider trading activity
- Options data (IV, put/call ratio) if present

### Research Steps

**Step 1 — Upcoming Earnings Date**
Use `WebSearch` for:
```
{TICKER} next earnings date {CURRENT_YEAR}
```
Or use `firecrawl_scrape` on:
```
https://www.earningswhispers.com/stocks/{TICKER}
```
Extract: next earnings date, estimated EPS, options-implied move for earnings.

**Step 2 — Upcoming Catalysts (WebSearch)**
Use `WebSearch` for each of the following, collecting results:
```
{COMPANY} product launch {YEAR}
{COMPANY} FDA approval PDUFA date (if healthcare/pharma)
{COMPANY} contract renewal award {YEAR}
{COMPANY} merger acquisition rumor {YEAR}
{COMPANY} analyst day investor conference {YEAR}
{COMPANY} share buyback dividend increase {YEAR}
```
Compile a dated catalyst calendar.

**Step 3 — Regulatory & Legal Risk (SEC EDGAR + WebSearch)**
Use `WebSearch` for:
```
{COMPANY} SEC investigation regulatory risk {YEAR}
{COMPANY} antitrust lawsuit litigation {YEAR}
{COMPANY} regulatory headwind {INDUSTRY}
```
Use `firecrawl_scrape` on any news articles or SEC filings that surface specific regulatory issues.

**Step 4 — Short Interest and Bear Thesis**
Use `firecrawl_scrape` on:
```
https://finviz.com/quote.ashx?t={TICKER}
```
Extract short interest percentage and short float. Then use `WebSearch` for:
```
{TICKER} short seller report bear thesis
{TICKER} Hindenburg Citron short case
```
If there is a notable short seller report, use `firecrawl_scrape` to extract the key arguments from that report's public landing page.

**Step 5 — Macro Sensitivity Analysis (WebSearch + Firecrawl)**
Use `WebSearch` for:
```
{COMPANY} interest rate sensitivity debt refinancing
{COMPANY} currency exposure foreign revenue breakdown
{COMPANY} commodity exposure supply chain risk
{COMPANY} consumer spending sensitivity recession
```
Build a structured sensitivity map.

**Step 6 — Recent News Risk Scan (Google News)**
Use `WebSearch` for the last 30-60 days of news:
```
{TICKER} {COMPANY} risk warning problem issue {CURRENT_MONTH} {CURRENT_YEAR}
```
Flag any emerging risks not yet reflected in the baseline report.

### Output Format

Produce a markdown section with this structure:

```markdown
## Catalysts & Deep Risk Analysis (Deep)

### Upcoming Catalyst Calendar
| Date | Catalyst | Potential Impact | Probability |
|------|----------|-----------------|-------------|
| [Date] | Next Earnings | High | Certain |
| [Date or "TBD"] | [Product launch / FDA date / Analyst Day / etc.] | High / Med / Low | High / Med / Speculative |
| [Date or "TBD"] | [Other catalyst] | ... | ... |

### Options-Implied Move at Next Earnings
**Implied move:** ±X% (based on straddle pricing or reported estimates)
**Historical average earnings move:** ±X% (last 4 quarters)

### Upside Catalysts (Bull Triggers)
1. **[Catalyst name]** — [Description, timeline, potential magnitude]
2. **[Catalyst name]** — [Description, timeline, potential magnitude]
3. **[Catalyst name]** — [Description, timeline, potential magnitude]

### Downside Risks (Bear Triggers)
1. **[Risk name]** — [Description, timeline, potential magnitude]
2. **[Risk name]** — [Description, timeline, potential magnitude]
3. **[Risk name]** — [Description, timeline, potential magnitude]

### Short Interest Profile
- **Short float:** X.X% (Low <5% / Moderate 5-15% / High >15%)
- **Short interest trend:** Rising / Falling / Stable
- **Days to cover:** X days
- **Bear thesis summary:** [If a notable short report exists, 3-5 sentence summary of the bear case]

### Macro Sensitivity Map
| Factor | Sensitivity | Exposure |
|--------|------------|---------|
| Interest Rate Risk | Low / Med / High | [Description: % floating rate debt, refinancing needs] |
| USD Strength | Low / Med / High | [Description: % international revenue, hedging status] |
| Commodity / Input Costs | Low / Med / High | [Description: key inputs, pricing power] |
| Consumer Spending / GDP | Low / Med / High | [Description: cyclicality, recession performance history] |

### Regulatory & Legal Risk Register
| Risk | Status | Potential Impact | Timeline |
|------|--------|-----------------|----------|
| [Regulatory issue] | Active / Monitoring / Resolved | High / Med / Low | [Timeline] |
| [Litigation] | ... | ... | ... |

### Emerging Risks (Last 60 Days)
- [Risk 1 from recent news — date, source, description]
- [Risk 2]

### Risk/Catalyst Verdict
[3-4 sentences: What is the most likely stock-moving event in the next 6 months? Does the risk/reward setup favor longs or shorts at the current price? Are there any binary events that could cause outsized moves?]
```

---

## Agent 5: Synthesis Agent

### Role
You are the final agent in the deep research pipeline. You receive the baseline stock report AND the outputs from all four specialist agents. Your job is to synthesize everything into a single, enhanced research document that is materially better than the baseline — not just a concatenation, but a genuine synthesis that identifies agreements, contradictions, and the clearest signal across all dimensions.

### What to Read
- The full baseline report (provided in your prompt)
- The full output from Agent 1 (Fundamentals & Valuation)
- The full output from Agent 2 (Earnings & Management)
- The full output from Agent 3 (Competitive Moat)
- The full output from Agent 4 (Catalyst & Risk)

### Synthesis Steps

**Step 1 — Cross-Reference for Consistency**
Before writing, identify:
- Where do agents agree? (e.g., valuation looks cheap AND management guided up AND moat is wide — strong bull signal)
- Where do agents contradict? (e.g., valuation cheap BUT management tone cautious AND short interest rising — mixed signal requiring nuance)
- What is the single most important insight that the baseline report missed?

**Step 2 — Investment Thesis Construction**
Build a clear buy/hold/avoid framework based on all inputs:
- Assign an overall conviction level: Strong Buy / Buy / Hold / Avoid / Strong Avoid
- Identify 3 key reasons FOR the thesis
- Identify 3 key risks AGAINST the thesis
- Set a base case price target (12 months)
- Set a bull case price target
- Set a bear case price target

**Step 3 — Monitoring Triggers**
Define specific, observable events that would cause you to change the thesis:
- What would make you more bullish? (specific price target raise, product launch success, earnings beat above X%)
- What would make you more bearish? (specific margin compression threshold, guidance cut, competitive loss)

**Step 4 — Compose the Enhanced Report**
Write the full enhanced report with this structure:
1. Keep the original YAML frontmatter but change the title to include "[Deep]"
2. Add a new "Investment Thesis" section at the very top (after frontmatter)
3. Include the original baseline sections (preserved, not altered)
4. Append the four deep sections after the baseline content
5. Add a "Key Monitoring Triggers" section at the end

### Output Format

The Synthesis Agent outputs the COMPLETE enhanced report as a single markdown document. This is the content that will overwrite the Obsidian file. Structure:

```markdown
---
[original YAML frontmatter, title changed to include "[Deep]"]
---

# [TICKER] — [Company Name] [Deep]

## Investment Thesis

**Overall Verdict:** [Strong Buy / Buy / Hold / Avoid / Strong Avoid]
**Conviction Level:** [High / Medium / Low]
**Time Horizon:** 12 months
**Current Price:** $X.XX | **Base Target:** $X.XX | **Bull Target:** $X.XX | **Bear Target:** $X.XX
**Upside/Downside:** Base +X% | Bull +X% | Bear -X%

### Why This Thesis

**Bull Case (X conviction):**
1. [Reason 1 — specific, data-backed]
2. [Reason 2]
3. [Reason 3]

**Bear Case / Key Risks:**
1. [Risk 1 — specific, data-backed]
2. [Risk 2]
3. [Risk 3]

**The Deciding Factor:** [1-2 sentences identifying the single most important variable that determines whether this is a good investment]

---

[... ALL ORIGINAL BASELINE SECTIONS PRESERVED HERE UNCHANGED ...]

---

## Fundamentals & Valuation (Deep)
[Full output from Agent 1]

## What Management Is Saying (Deep)
[Full output from Agent 2]

## Competitive Moat & Peer Analysis (Deep)
[Full output from Agent 3]

## Catalysts & Deep Risk Analysis (Deep)
[Full output from Agent 4]

---

## Key Monitoring Triggers

### Go More Bullish If:
- [ ] [Specific observable event — e.g., "Q3 EPS guidance raised above $X.XX"]
- [ ] [Specific observable event]
- [ ] [Specific observable event]

### Go More Bearish / Exit If:
- [ ] [Specific observable event — e.g., "Gross margin falls below X% for two consecutive quarters"]
- [ ] [Specific observable event]
- [ ] [Specific observable event]

### Next Check-In Date: [YYYY-MM-DD — typically next earnings date]
```

The Synthesis Agent does NOT do additional web research. It works only from the materials provided to it.
