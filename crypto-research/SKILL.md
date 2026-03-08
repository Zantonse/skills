---
name: crypto-research
description: "Comprehensive cryptocurrency research that scrapes on-chain data, market metrics, technicals, whale activity, social sentiment, and news from 12 sources in parallel, synthesizes analysis with Gemini, and writes structured reports to the Obsidian vault. Use when the user asks to research a cryptocurrency, analyze a coin or token, check crypto prices or fundamentals, build a crypto investment thesis, or do a crypto deep dive. Triggers on: crypto symbols (BTC, ETH, SOL), coin names (bitcoin, ethereum, solana), 'crypto research', 'analyze [coin]', 'what do you think about [crypto]', 'research bitcoin', 'crypto deep dive', 'on-chain analysis', 'whale activity', or any request combining a cryptocurrency name/symbol with investment, trading, or analysis intent. Also trigger when the user mentions checking crypto sentiment, fear and greed index, or wants to compare cryptocurrencies."
---

# Crypto Research

Perform investment research for cryptocurrencies and write structured reports to the Obsidian vault.

## How It Works

The skill uses `scripts/research_crypto.py` to:
1. Resolve a coin symbol or name to a CoinGecko ID
2. Scrape 12 data sources concurrently (CoinGecko, TradingView, CoinMarketCap, Messari, IntoTheBlock, CryptoQuant, LunarCrush, Fear & Greed Index, Google News, blockchain explorers)
3. Send all scraped context to Gemini (via LiteLLM) with a crypto-analysis system prompt
4. Format the output with Obsidian YAML frontmatter and wiki-links
5. Save to `~/Documents/ObsidianNotes/Claude-Research/crypto/`

All scrapers run in parallel via ThreadPoolExecutor.

## Single Coin Usage

```bash
python3 /Users/craigverzosa/.claude/skills/crypto-research/scripts/research_crypto.py BTC
python3 /Users/craigverzosa/.claude/skills/crypto-research/scripts/research_crypto.py ethereum
python3 /Users/craigverzosa/.claude/skills/crypto-research/scripts/research_crypto.py SOL
python3 /Users/craigverzosa/.claude/skills/crypto-research/scripts/research_crypto.py SOL --output /custom/path.md
```

The script accepts ticker symbols (BTC, ETH, SOL) or full names (bitcoin, ethereum, solana) and resolves them to CoinGecko IDs automatically.

## Multi-Coin: Parallel Subagent Dispatching

When the user asks to research multiple coins, dispatch one subagent per coin using the Task tool in a single message:

```
For each coin, create a Task with:
  subagent_type: "Bash"
  model: "sonnet"
  prompt: "Run: python3 /Users/craigverzosa/.claude/skills/crypto-research/scripts/research_crypto.py {SYMBOL}
           Report the output path and any source failures from stderr."
```

## After Running

1. Report the output file path(s)
2. Summarize key findings: price, market cap, on-chain health, sentiment, bull/bear thesis
3. Mention the Fear & Greed Index as market-wide context
4. Note any data sources that failed
5. For multi-coin runs, provide a comparison table

## Output Location

`~/Documents/ObsidianNotes/Claude-Research/crypto/{SYMBOL}-{YYYY-MM}.md`

## Data Sources (12 total, all scraped concurrently)

| Source | Data |
|--------|------|
| CoinGecko API | Price, market cap, volume, supply, ATH/ATL, rank, categories |
| CoinGecko Developer | GitHub commits, stars, forks, pull requests |
| CoinGecko Community | Reddit subscribers, Twitter followers |
| TradingView TA | RSI, MACD, MAs, Bollinger Bands, composite buy/sell signals |
| CoinMarketCap | Market dominance, FDV, sector tags, supply % |
| Messari | On-chain metrics: active addresses, NVT, fees, tx count |
| IntoTheBlock | Whale concentration, exchange flows, holder composition |
| CryptoQuant | Exchange reserves, funding rates, miner flows |
| Fear & Greed Index | Market-wide sentiment (0-100 scale) |
| LunarCrush | Social sentiment score, social volume, social dominance |
| Google News RSS | Recent news with dates and sources |
| Blockchain explorers | Hash rate (PoW) or staking rate (PoS) |

## Dependencies

- Python 3 with `requests`, `beautifulsoup4`, `tradingview_ta` (auto-installed if missing)
- LiteLLM credentials in `~/.claude-litellm.env` (same as deep-research skill)
- Obsidian vault at `~/Documents/ObsidianNotes/`
