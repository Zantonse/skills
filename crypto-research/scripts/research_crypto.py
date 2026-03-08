#!/usr/bin/env python3
"""Crypto research orchestrator — scrapes on-chain, market, and sentiment data, synthesizes with Gemini.

Usage:
    python3 research_crypto.py BTC
    python3 research_crypto.py ethereum
    python3 research_crypto.py SOL --output /custom/path.md

Environment:
    LITELLM_API_KEY + LITELLM_BASE_URL (set in ~/.claude-litellm.env)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Environment & dependency helpers
# ---------------------------------------------------------------------------

def _load_env_file():
    if os.environ.get("LITELLM_API_KEY"):
        return
    env_file = os.path.expanduser("~/.claude-litellm.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export ") and "=" in line:
                    line = line[7:]
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    if value.startswith("$"):
                        value = os.environ.get(value[1:], "")
                    if key and value:
                        os.environ[key] = value

_load_env_file()

def _ensure_packages():
    for pkg, imp in [("requests", "requests"), ("beautifulsoup4", "bs4"), ("openai", "openai"), ("tradingview_ta", "tradingview_ta")]:
        try:
            __import__(imp)
        except ImportError:
            print(f"Installing {pkg}...", file=sys.stderr)
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

_ensure_packages()

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
PROMPT_FILE = SKILL_DIR / "references" / "crypto-research-prompt.md"
OBSIDIAN_BASE = Path.home() / "Documents" / "ObsidianNotes" / "Claude-Research" / "crypto"
DEFAULT_MODEL = "gemini-3.1-pro-preview"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# Common symbol -> CoinGecko ID mappings
SYMBOL_MAP = {
    "BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana", "BNB": "binancecoin",
    "XRP": "ripple", "ADA": "cardano", "DOGE": "dogecoin", "AVAX": "avalanche-2",
    "DOT": "polkadot", "MATIC": "matic-network", "LINK": "chainlink",
    "UNI": "uniswap", "ATOM": "cosmos", "LTC": "litecoin", "NEAR": "near",
    "ARB": "arbitrum", "OP": "optimism", "APT": "aptos", "SUI": "sui",
    "FIL": "filecoin", "AAVE": "aave", "MKR": "maker", "INJ": "injective-protocol",
    "TIA": "celestia", "SEI": "sei-network", "RENDER": "render-token",
    "FET": "fetch-ai", "PEPE": "pepe", "WIF": "dogwifcoin", "BONK": "bonk",
    "POL": "pol-ex-matic", "HBAR": "hedera-hashgraph", "ICP": "internet-computer",
    "STX": "blockstack", "IMX": "immutable-x", "ALGO": "algorand",
}

# Symbol -> TradingView pair mapping
TV_PAIR_MAP = {
    "BTC": "BTCUSDT", "ETH": "ETHUSDT", "SOL": "SOLUSDT", "BNB": "BNBUSDT",
    "XRP": "XRPUSDT", "ADA": "ADAUSDT", "DOGE": "DOGEUSDT", "AVAX": "AVAXUSDT",
    "DOT": "DOTUSDT", "MATIC": "MATICUSDT", "LINK": "LINKUSDT", "UNI": "UNIUSDT",
    "ATOM": "ATOMUSDT", "LTC": "LTCUSDT", "NEAR": "NEARUSDT", "ARB": "ARBUSDT",
    "OP": "OPUSDT", "APT": "APTUSDT", "SUI": "SUIUSDT", "FIL": "FILUSDT",
    "AAVE": "AAVEUSDT", "INJ": "INJUSDT", "TIA": "TIAUSDT", "SEI": "SEIUSDT",
    "RENDER": "RENDERUSDT", "FET": "FETUSDT", "PEPE": "PEPEUSDT",
    "HBAR": "HBARUSDT", "ICP": "ICPUSDT", "STX": "STXUSDT", "IMX": "IMXUSDT",
}

# ---------------------------------------------------------------------------
# Symbol resolution
# ---------------------------------------------------------------------------

def resolve_coin(query: str) -> tuple[str, str]:
    """Resolve a query to (symbol, coingecko_id). Returns uppercase symbol and CG ID."""
    q = query.strip().upper()

    # Direct symbol match
    if q in SYMBOL_MAP:
        return q, SYMBOL_MAP[q]

    # Try lowercase as CoinGecko ID directly
    ql = query.strip().lower()
    if ql in SYMBOL_MAP.values():
        for sym, cg_id in SYMBOL_MAP.items():
            if cg_id == ql:
                return sym, cg_id

    # Search CoinGecko
    try:
        resp = requests.get(f"https://api.coingecko.com/api/v3/search?query={query}",
                            headers=HEADERS, timeout=10)
        resp.raise_for_status()
        coins = resp.json().get("coins", [])
        if coins:
            return coins[0]["symbol"].upper(), coins[0]["id"]
    except Exception as e:
        print(f"Warning: CoinGecko search failed: {e}", file=sys.stderr)

    # Fallback: use query as-is
    return q, ql.replace(" ", "-")


# ---------------------------------------------------------------------------
# Scrapers
# ---------------------------------------------------------------------------

def scrape_coingecko(cg_id: str) -> tuple[str, Optional[str]]:
    """Fetch comprehensive coin data from CoinGecko API."""
    source = "CoinGecko"
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{cg_id}?localization=false&tickers=false&market_data=true&community_data=true&developer_data=true"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        d = resp.json()

        md = d.get("market_data", {})
        lines = [
            f"Name: {d.get('name')}",
            f"Symbol: {d.get('symbol', '').upper()}",
            f"Market Cap Rank: #{d.get('market_cap_rank')}",
            f"Categories: {', '.join(d.get('categories', []) or [])}",
            "",
            "## Market Data",
            f"Price: ${md.get('current_price', {}).get('usd', 'N/A'):,.2f}" if isinstance(md.get('current_price', {}).get('usd'), (int, float)) else "Price: N/A",
            f"Market Cap: ${md.get('market_cap', {}).get('usd', 0):,.0f}",
            f"24h Volume: ${md.get('total_volume', {}).get('usd', 0):,.0f}",
            f"24h Change: {md.get('price_change_percentage_24h', 0):.2f}%",
            f"7d Change: {md.get('price_change_percentage_7d', 0):.2f}%",
            f"30d Change: {md.get('price_change_percentage_30d', 0):.2f}%",
            f"1y Change: {md.get('price_change_percentage_1y', 0) or 'N/A'}",
            f"ATH: ${md.get('ath', {}).get('usd', 0):,.2f}",
            f"ATH Change: {md.get('ath_change_percentage', {}).get('usd', 0):.1f}%",
            f"ATL: ${md.get('atl', {}).get('usd', 0):,.6f}",
            f"Circulating Supply: {md.get('circulating_supply', 0):,.0f}",
            f"Total Supply: {md.get('total_supply', 'N/A')}",
            f"Max Supply: {md.get('max_supply', 'N/A')}",
            f"Fully Diluted Valuation: ${md.get('fully_diluted_valuation', {}).get('usd', 0):,.0f}",
        ]

        # Developer data
        dev = d.get("developer_data", {})
        if dev:
            lines.extend([
                "",
                "## Developer Activity",
                f"GitHub Forks: {dev.get('forks', 0)}",
                f"GitHub Stars: {dev.get('stars', 0)}",
                f"GitHub Subscribers: {dev.get('subscribers', 0)}",
                f"Total Issues: {dev.get('total_issues', 0)}",
                f"Closed Issues: {dev.get('closed_issues', 0)}",
                f"Pull Requests Merged: {dev.get('pull_requests_merged', 0)}",
                f"Pull Request Contributors: {dev.get('pull_request_contributors', 0)}",
                f"Commit Count (4 weeks): {dev.get('commit_count_4_weeks', 0)}",
            ])

        # Community data
        comm = d.get("community_data", {})
        if comm:
            lines.extend([
                "",
                "## Community",
                f"Twitter Followers: {comm.get('twitter_followers', 0):,}",
                f"Reddit Subscribers: {comm.get('reddit_subscribers', 0):,}",
                f"Reddit Active Accounts (48h): {comm.get('reddit_accounts_active_48h', 0):,}",
            ])

        # Description
        desc = d.get("description", {}).get("en", "")
        if desc:
            # Truncate to first 1000 chars
            clean = BeautifulSoup(desc, "html.parser").get_text()[:1000]
            lines.extend(["", "## Description", clean])

        return source, "\n".join(lines)
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_tradingview_crypto(symbol: str) -> tuple[str, Optional[str]]:
    """Get TradingView technical analysis for a crypto pair."""
    source = "TradingView Technical Analysis"
    try:
        from tradingview_ta import TA_Handler, Interval

        pair = TV_PAIR_MAP.get(symbol, f"{symbol}USDT")
        exchanges = ["BINANCE", "COINBASE", "BYBIT"]
        analysis = None

        for ex in exchanges:
            try:
                handler = TA_Handler(symbol=pair, screener="crypto", exchange=ex,
                                     interval=Interval.INTERVAL_1_DAY)
                analysis = handler.get_analysis()
                break
            except Exception:
                continue

        if not analysis:
            return source, None

        ind = analysis.indicators
        lines = []

        # Price
        lines.append("## Price Data")
        for key in ["close", "open", "high", "low", "volume", "change"]:
            val = ind.get(key)
            if val is not None:
                if key == "volume":
                    lines.append(f"{key}: {val:,.0f}")
                elif key == "change":
                    lines.append(f"{key}: {val:+.2f}%")
                else:
                    lines.append(f"{key}: ${val:,.2f}")

        # Signals
        lines.append("")
        lines.append("## Composite Signals")
        s = analysis.summary
        lines.append(f"Overall: {s['RECOMMENDATION']} (Buy: {s['BUY']}, Sell: {s['SELL']}, Neutral: {s['NEUTRAL']})")
        o = analysis.oscillators
        lines.append(f"Oscillators: {o['RECOMMENDATION']} (Buy: {o['BUY']}, Sell: {o['SELL']}, Neutral: {o['NEUTRAL']})")
        m = analysis.moving_averages
        lines.append(f"Moving Averages: {m['RECOMMENDATION']} (Buy: {m['BUY']}, Sell: {m['SELL']}, Neutral: {m['NEUTRAL']})")

        # Key indicators
        lines.append("")
        lines.append("## Key Indicators")
        for key, label in [("RSI", "RSI (14)"), ("Stoch.K", "Stochastic %K"), ("CCI20", "CCI"),
                           ("ADX", "ADX"), ("MACD.macd", "MACD"), ("MACD.signal", "MACD Signal"),
                           ("Mom", "Momentum"), ("W.R", "Williams %R")]:
            val = ind.get(key)
            if val is not None:
                lines.append(f"{label}: {val:.2f}")

        # Moving averages
        lines.append("")
        lines.append("## Moving Averages")
        close = ind.get("close", 0)
        for key, label in [("SMA20", "SMA 20"), ("EMA50", "EMA 50"), ("SMA50", "SMA 50"),
                           ("EMA200", "EMA 200"), ("SMA200", "SMA 200"), ("VWMA", "VWMA")]:
            val = ind.get(key)
            signal = m.get("COMPUTE", {}).get(key, "")
            if val is not None:
                pct = ((close - val) / val * 100) if val else 0
                lines.append(f"{label}: ${val:,.2f} ({pct:+.1f}% from price) — {signal}")

        # Bollinger Bands
        bb_up = ind.get("BB.upper")
        bb_lo = ind.get("BB.lower")
        if bb_up and bb_lo:
            lines.extend(["", "## Bollinger Bands",
                          f"Upper: ${bb_up:,.2f}", f"Lower: ${bb_lo:,.2f}"])

        # Pivots
        pivot = ind.get("Pivot.M.Classic.Middle")
        s1 = ind.get("Pivot.M.Classic.S1")
        r1 = ind.get("Pivot.M.Classic.R1")
        if pivot:
            lines.extend(["", "## Pivot Points",
                          f"Monthly Pivot: ${pivot:,.2f}",
                          f"Support 1: ${s1:,.2f}" if s1 else "",
                          f"Resistance 1: ${r1:,.2f}" if r1 else ""])

        return source, "\n".join(lines)
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_fear_greed() -> tuple[str, Optional[str]]:
    """Fetch the Crypto Fear & Greed Index."""
    source = "Fear & Greed Index"
    try:
        resp = requests.get("https://api.alternative.me/fng/?limit=7", headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        if not data:
            return source, None

        lines = ["## Crypto Fear & Greed Index"]
        for entry in data:
            lines.append(f"{entry['value']} — {entry['value_classification']} ({entry.get('timestamp', '')})")

        return source, "\n".join(lines)
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_coinmarketcap(symbol: str) -> tuple[str, Optional[str]]:
    """Scrape CoinMarketCap for market dominance and sector data."""
    source = "CoinMarketCap"
    try:
        url = f"https://coinmarketcap.com/currencies/{symbol.lower()}/"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        for el in soup.find_all(["span", "dd", "div"]):
            text = el.get_text(" ", strip=True)
            if any(kw in text for kw in ["Market Cap", "Volume", "Dominance", "Supply",
                                          "Fully Diluted", "Max Supply", "Total Supply"]) and 5 < len(text) < 200:
                if text not in lines:
                    lines.append(text)

        if lines:
            return source, "## CoinMarketCap Data\n" + "\n".join(lines[:20])
        return source, f"CoinMarketCap loaded but limited data for {symbol}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_messari(cg_id: str) -> tuple[str, Optional[str]]:
    """Scrape Messari for on-chain metrics."""
    source = "Messari (On-Chain)"
    try:
        url = f"https://messari.io/project/{cg_id}/metrics"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        for el in soup.find_all(["td", "span", "div"]):
            text = el.get_text(" ", strip=True)
            if any(kw in text.lower() for kw in ["active address", "transaction", "nvt", "fee",
                                                   "hash rate", "staking", "validator"]) and 5 < len(text) < 200:
                if text not in lines:
                    lines.append(text)

        if lines:
            return source, "## On-Chain Metrics (Messari)\n" + "\n".join(lines[:25])
        return source, f"Messari loaded but limited on-chain data for {cg_id}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_intotheblock(symbol: str) -> tuple[str, Optional[str]]:
    """Scrape IntoTheBlock for whale and exchange flow data."""
    source = "IntoTheBlock (Whale/Exchange)"
    try:
        url = f"https://app.intotheblock.com/coin/{symbol.upper()}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        for el in soup.find_all(["span", "div", "p"]):
            text = el.get_text(" ", strip=True)
            if any(kw in text.lower() for kw in ["whale", "exchange", "concentration", "holder",
                                                   "large transaction", "inflow", "outflow",
                                                   "net flow"]) and 5 < len(text) < 200:
                if text not in lines:
                    lines.append(text)

        if lines:
            return source, "## Whale & Exchange Data (IntoTheBlock)\n" + "\n".join(lines[:20])
        return source, f"IntoTheBlock loaded but limited data for {symbol} (likely JS-rendered)"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_cryptoquant(symbol: str) -> tuple[str, Optional[str]]:
    """Scrape CryptoQuant for exchange reserves and funding rates."""
    source = "CryptoQuant"
    try:
        url = f"https://cryptoquant.com/asset/{symbol.lower()}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        for el in soup.find_all(["span", "div", "td"]):
            text = el.get_text(" ", strip=True)
            if any(kw in text.lower() for kw in ["reserve", "funding", "sopr", "miner",
                                                   "exchange flow", "net flow"]) and 5 < len(text) < 200:
                if text not in lines:
                    lines.append(text)

        if lines:
            return source, "## Exchange & Mining Data (CryptoQuant)\n" + "\n".join(lines[:20])
        return source, f"CryptoQuant loaded but limited data for {symbol} (likely JS-rendered)"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_lunarcrush(symbol: str) -> tuple[str, Optional[str]]:
    """Scrape LunarCrush for social sentiment data."""
    source = "LunarCrush (Social Sentiment)"
    try:
        url = f"https://lunarcrush.com/coins/{symbol.lower()}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        for el in soup.find_all(["span", "div"]):
            text = el.get_text(" ", strip=True)
            if any(kw in text.lower() for kw in ["sentiment", "social volume", "social dominance",
                                                   "galaxy score", "altrank", "bullish", "bearish"]) and 5 < len(text) < 200:
                if text not in lines:
                    lines.append(text)

        if lines:
            return source, "## Social Sentiment (LunarCrush)\n" + "\n".join(lines[:20])
        return source, f"LunarCrush loaded but limited data for {symbol} (likely JS-rendered)"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_google_news_crypto(symbol: str, name: str) -> tuple[str, Optional[str]]:
    """Fetch recent crypto news from Google News RSS."""
    source = "Google News"
    try:
        query = f"{name} {symbol} crypto"
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "xml")
        items = soup.find_all("item")

        headlines = []
        for item in items[:15]:
            title = item.find("title")
            pub_date = item.find("pubDate")
            source_tag = item.find("source")
            if title:
                line = title.get_text(strip=True)
                if source_tag:
                    line += f" — {source_tag.get_text(strip=True)}"
                if pub_date:
                    try:
                        from email.utils import parsedate_to_datetime
                        dt = parsedate_to_datetime(pub_date.get_text(strip=True))
                        line += f" ({dt.strftime('%b %d')})"
                    except Exception:
                        pass
                headlines.append(f"- {line}")

        if headlines:
            return source, "## Recent News\n" + "\n".join(headlines)
        return source, f"No recent news found for {name}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_blockchain_explorer(symbol: str) -> tuple[str, Optional[str]]:
    """Scrape basic blockchain stats from public explorers."""
    source = "Blockchain Explorer"
    try:
        lines = []
        if symbol == "BTC":
            # blockchain.com API
            resp = requests.get("https://blockchain.info/q/hashrate", headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                lines.append(f"Hash Rate: {float(resp.text) / 1e9:.2f} EH/s")
            resp2 = requests.get("https://blockchain.info/q/getdifficulty", headers=HEADERS, timeout=10)
            if resp2.status_code == 200:
                lines.append(f"Difficulty: {float(resp2.text):,.0f}")
        elif symbol == "ETH":
            # beaconcha.in for staking stats
            resp = requests.get("https://beaconcha.in/api/v1/epoch/latest", headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                try:
                    data = resp.json().get("data", {})
                    lines.append(f"Validators: {data.get('validatorscount', 'N/A'):,}")
                except Exception:
                    pass

        if lines:
            return source, "## Blockchain Stats\n" + "\n".join(lines)
        return source, f"Blockchain explorer data limited for {symbol}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


# ---------------------------------------------------------------------------
# Gemini synthesis
# ---------------------------------------------------------------------------

def load_system_prompt() -> str:
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text()
    return "You are an expert cryptocurrency analyst. Produce a comprehensive research report in markdown."


def synthesize_with_gemini(symbol: str, name: str, scraped: dict[str, str],
                           model: str = DEFAULT_MODEL) -> str:
    from openai import OpenAI

    api_key = os.environ.get("LITELLM_API_KEY")
    base_url = os.environ.get("LITELLM_BASE_URL")
    if not api_key or not base_url:
        print("Error: LITELLM_API_KEY and LITELLM_BASE_URL required.", file=sys.stderr)
        sys.exit(1)

    base_url = base_url.rstrip("/")
    if not base_url.endswith("/v1"):
        base_url += "/v1"

    client = OpenAI(api_key=api_key, base_url=base_url)
    system_prompt = load_system_prompt()

    context_parts = []
    failed = []
    for src, data in scraped.items():
        if data:
            context_parts.append(f"### {src}\n\n{data}")
        else:
            failed.append(src)

    context = "\n\n---\n\n".join(context_parts)
    query = f"Produce a comprehensive crypto research report for {symbol} ({name})."
    if failed:
        query += f"\n\nNote: These sources were unavailable: {', '.join(failed)}. Work with available data and note gaps."

    user_msg = f"## Scraped Crypto Data\n\n{context}\n\n---\n\n## Task\n\n{query}"

    print(f"Synthesizing with {model}...", file=sys.stderr)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_msg}],
            max_tokens=16000, temperature=0.3,
        )
    except Exception as e:
        print(f"Gemini API error: {e}", file=sys.stderr)
        sys.exit(1)

    result = response.choices[0].message.content or ""
    usage = getattr(response, "usage", None)
    if usage:
        print(f"Tokens — prompt: {usage.prompt_tokens:,}, completion: {usage.completion_tokens:,}, "
              f"total: {usage.total_tokens:,}", file=sys.stderr)
    return result


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def format_obsidian_output(symbol: str, report: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""---
date: {today}
tags:
  - crypto-research
  - {symbol}
source: claude-code
project: personal-investing
symbol: {symbol}
type: crypto
---

> Related: [[crypto-watchlist]] [[portfolio-notes]]

{report}
"""


def output_filename(symbol: str) -> Path:
    return OBSIDIAN_BASE / f"{symbol}-{datetime.now().strftime('%Y-%m')}.md"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Cryptocurrency research")
    parser.add_argument("coin", help="Coin symbol (BTC, ETH) or name (bitcoin, ethereum)")
    parser.add_argument("--output", "-o", default=None, help="Custom output file path")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"LLM model (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    symbol, cg_id = resolve_coin(args.coin)
    print(f"Researching crypto: {symbol} (CoinGecko ID: {cg_id})", file=sys.stderr)

    # Get the coin name from CoinGecko for news searches
    coin_name = cg_id.replace("-", " ").title()

    print("Scraping crypto data...", file=sys.stderr)
    scrapers = [
        ("CoinGecko", lambda: scrape_coingecko(cg_id)),
        ("TradingView Technical Analysis", lambda: scrape_tradingview_crypto(symbol)),
        ("Fear & Greed Index", lambda: scrape_fear_greed()),
        ("CoinMarketCap", lambda: scrape_coinmarketcap(cg_id)),
        ("Messari (On-Chain)", lambda: scrape_messari(cg_id)),
        ("IntoTheBlock (Whale/Exchange)", lambda: scrape_intotheblock(symbol)),
        ("CryptoQuant", lambda: scrape_cryptoquant(symbol)),
        ("LunarCrush (Social)", lambda: scrape_lunarcrush(symbol)),
        ("Google News", lambda: scrape_google_news_crypto(symbol, coin_name)),
        ("Blockchain Explorer", lambda: scrape_blockchain_explorer(symbol)),
    ]

    scraped = {}

    def _run(item):
        name, fn = item
        print(f"  Scraping {name}...", file=sys.stderr)
        _, data = fn()
        return name, data

    with ThreadPoolExecutor(max_workers=min(len(scrapers), 10)) as pool:
        futures = {pool.submit(_run, s): s[0] for s in scrapers}
        for future in as_completed(futures):
            name, data = future.result()
            scraped[name] = data

    ok = sum(1 for v in scraped.values() if v)
    total = len(scraped)
    print(f"Scraped {ok}/{total} sources in parallel", file=sys.stderr)

    if ok == 0:
        print("Error: All sources failed.", file=sys.stderr)
        sys.exit(1)

    report = synthesize_with_gemini(symbol, coin_name, scraped, model=args.model)
    output = format_obsidian_output(symbol, report)

    out_path = Path(args.output) if args.output else output_filename(symbol)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output)
    print(f"Report saved to: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
