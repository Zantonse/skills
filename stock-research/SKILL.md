---
name: stock-research
description: "Comprehensive stock, ETF, and sector investment research that scrapes financial data from 14 public sources, synthesizes analysis with Claude Sonnet (extended thinking) for deeper analytical quality, and writes structured reports to the Obsidian vault. Use when the user asks to research a stock, analyze a ticker, look up company financials, build an investment thesis, do a stock deep dive, or perform any financial/investment analysis. Triggers on: stock ticker symbols (AAPL, TSLA, NVDA), 'stock research', 'analyze [ticker]', 'investment research', 'financial analysis', 'look up [company]', 'stock deep dive', 'research [ticker]', 'what do you think about [stock]', 'should I buy [stock]', 'pull up financials for', 'ETF analysis', 'sector research', or any request combining a company name or ticker with investment, financial, or trading intent. Also trigger when the user mentions wanting to add a stock to a watchlist or compare investments."
---

# Stock Research

Perform investment research for stocks, ETFs, or sectors and write structured reports to the Obsidian vault.

## How It Works

The skill uses `scripts/research_stock.py` to:
1. Resolve a ticker symbol (or look one up from a company name)
2. Scrape 14 data sources concurrently (Yahoo Finance, Finviz, TradingView, StockAnalysis, Macrotrends, SEC EDGAR, OpenInsider, Barchart, CapitolTrades, Google News, sector trends)
3. Send all scraped context to Claude Sonnet with extended thinking (via LiteLLM) for deep synthesis
4. Format the output with Obsidian YAML frontmatter and wiki-links
5. Save to `~/Documents/ObsidianNotes/Claude-Research/investments/`

All 14 scrapers run in parallel via ThreadPoolExecutor, so the total scrape phase completes in ~3-5 seconds regardless of source count.

## Single Ticker Usage

For a single ticker, run the script directly:

```bash
python3 <skill-path>/scripts/research_stock.py AAPL
python3 <skill-path>/scripts/research_stock.py "Apple Inc"
python3 <skill-path>/scripts/research_stock.py SPY --type etf
python3 <skill-path>/scripts/research_stock.py semiconductors --type sector
```

Replace `<skill-path>` with: `/Users/craigverzosa/.claude/skills/stock-research`

## Multi-Ticker: Parallel Subagent Dispatching

When the user asks to research multiple tickers (e.g., "research AAPL, MSFT, and GOOG" or "compare these 5 cybersecurity stocks"), dispatch one subagent per ticker using the Task tool. Each subagent runs independently and writes its own Obsidian file.

Dispatch all tickers in a **single message** with multiple Task tool calls so they run concurrently:

```
For each ticker, create a Task with:
  subagent_type: "Bash"
  model: "sonnet"
  prompt: "Run: python3 /Users/craigverzosa/.claude/skills/stock-research/scripts/research_stock.py {TICKER}
           Report the output path and any source failures from stderr."
```

Example — user says "research CRWD, ZS, PANW, and OKTA":
- Dispatch 4 Bash subagents simultaneously, one per ticker
- Each produces its own report in ~/Documents/ObsidianNotes/Claude-Research/investments/
- When all complete, summarize the key findings across all tickers conversationally
- If the user asked for a comparison, synthesize a comparison table from the reports

This approach researches 4 stocks in roughly the same wall-clock time as 1, because each subagent scrapes its 14 sources in parallel internally.

## After Running

1. Report the output file path(s) to the user
2. Summarize the key findings conversationally: price, valuation, analyst consensus, bull/bear thesis
3. Mention any data sources that failed (the script logs warnings for sources it couldn't reach)
4. For multi-ticker runs, provide a brief comparison highlighting how the stocks differ on key metrics
5. The user can open the report(s) in Obsidian for the full detailed view

## Output Location

- Stocks: `~/Documents/ObsidianNotes/Claude-Research/investments/{TICKER}-{YYYY-MM}.md`
- ETFs: `~/Documents/ObsidianNotes/Claude-Research/investments/{TICKER}-{YYYY-MM}.md`
- Sectors: `~/Documents/ObsidianNotes/Claude-Research/investments/sector-{name}-{YYYY-MM}.md`

## Data Sources (14 total, all scraped concurrently)

| Source | Data |
|--------|------|
| Yahoo Finance | Price, fundamentals, profile |
| Finviz | Analyst ratings, technicals, snapshot |
| TradingView (tradingview_ta) | Full technical analysis: 26 oscillators, 15 MAs, composite signals |
| StockAnalysis | Income statement, balance sheet, cash flow |
| Macrotrends | Historical financial trends |
| SEC EDGAR | 10-K risk factors |
| OpenInsider | Insider buying/selling activity |
| Barchart | Options data: IV, put/call ratio, unusual activity |
| Finviz Screener | Peer comparison vs industry competitors |
| CapitolTrades | Congressional/political trading activity |
| Yahoo Finance News | Company-specific headlines |
| Google News RSS | Broader news coverage with dates and sources |
| Finviz Groups | Sector and industry performance rankings |

## Dependencies

- Python 3 with `requests`, `beautifulsoup4`, `anthropic`, `tradingview_ta` (auto-installed if missing)
- LiteLLM credentials in `~/.claude-litellm.env` (same as deep-research and account-research skills)
- Obsidian vault at `~/Documents/ObsidianNotes/`

## Troubleshooting

- If scraping fails for a source, the script continues with remaining sources and notes the gap
- If the API returns an error, check that `~/.claude-litellm.env` has valid `LITELLM_API_KEY` and `LITELLM_BASE_URL`
- The script auto-installs missing packages (`requests`, `beautifulsoup4`, `anthropic`, `tradingview_ta`)
- Extended thinking requires `temperature=1` — this is set automatically in the synthesis function
