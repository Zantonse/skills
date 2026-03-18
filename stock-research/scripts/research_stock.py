#!/usr/bin/env python3
"""Stock research orchestrator — scrapes financial data and synthesizes with Gemini.

Usage:
    python3 research_stock.py AAPL
    python3 research_stock.py "Apple Inc"
    python3 research_stock.py SPY --type etf
    python3 research_stock.py semiconductors --type sector
    python3 research_stock.py AAPL --output /custom/path.md

Environment:
    LITELLM_API_KEY + LITELLM_BASE_URL (set in ~/.claude-litellm.env)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

# ---------------------------------------------------------------------------
# Environment & dependency helpers
# ---------------------------------------------------------------------------

def _load_env_file():
    """Auto-load credentials from ~/.claude-litellm.env if env vars are missing."""
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
                        ref_var = value[1:]
                        value = os.environ.get(ref_var, "")
                    if key and value:
                        os.environ[key] = value


_load_env_file()


def _ensure_packages():
    """Install required packages if missing."""
    for pkg, import_name in [("requests", "requests"), ("beautifulsoup4", "bs4"), ("anthropic", "anthropic"), ("tradingview_ta", "tradingview_ta")]:
        try:
            __import__(import_name)
        except ImportError:
            print(f"Installing {pkg}...", file=sys.stderr)
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            )


_ensure_packages()

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
PROMPT_FILE = SKILL_DIR / "references" / "stock-research-prompt.md"
OBSIDIAN_BASE = Path.home() / "Documents" / "ObsidianNotes" / "Claude-Research" / "investments"
DEFAULT_MODEL = "claude-4-6-sonnet"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# ---------------------------------------------------------------------------
# Ticker resolution
# ---------------------------------------------------------------------------

def resolve_ticker(query: str) -> Optional[str]:
    """Resolve a company name to a ticker symbol using Yahoo Finance search."""
    # If it looks like a ticker already (all caps, 1-5 chars), use it directly
    if re.match(r"^[A-Z]{1,5}$", query.upper()) and " " not in query:
        return query.upper()

    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={requests.utils.quote(query)}&quotesCount=1&newsCount=0"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        quotes = data.get("quotes", [])
        if quotes:
            return quotes[0].get("symbol", "").upper()
    except Exception as e:
        print(f"Warning: Ticker resolution failed: {e}", file=sys.stderr)

    # Fallback: treat the input as a ticker
    return query.upper().replace(" ", "")


# ---------------------------------------------------------------------------
# Scrapers — each returns (source_name, data_string) or (source_name, None)
# ---------------------------------------------------------------------------

def scrape_yahoo_quote(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape Yahoo Finance quote page for key metrics."""
    source = "Yahoo Finance Quote"
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}/"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        # Extract the page title for company name
        title_tag = soup.find("title")
        if title_tag:
            lines.append(f"Page: {title_tag.get_text(strip=True)}")

        # Look for key stats in list items and table rows
        for li in soup.find_all("li"):
            text = li.get_text(" ", strip=True)
            # Filter for financial metric patterns
            if any(kw in text for kw in [
                "Previous Close", "Open", "Bid", "Ask", "Day's Range", "52 Week Range",
                "Volume", "Avg. Volume", "Market Cap", "Beta", "PE Ratio", "EPS",
                "Earnings Date", "Forward Dividend", "Ex-Dividend", "1y Target",
                "Net Assets", "Yield", "Expense Ratio", "Inception Date",
            ]):
                lines.append(text)

        if lines:
            return source, "\n".join(lines)
        return source, f"Page loaded but no structured metrics extracted for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_yahoo_profile(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape Yahoo Finance profile page for business description."""
    source = "Yahoo Finance Profile"
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}/profile"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        # Look for the company description section
        for section in soup.find_all("section"):
            text = section.get_text(" ", strip=True)
            if len(text) > 200 and any(kw in text.lower() for kw in ["founded", "company", "provides", "develops", "operates"]):
                lines.append(text[:3000])  # Cap length
                break

        # Sector/industry info
        for span in soup.find_all("span"):
            text = span.get_text(strip=True)
            if text in ["Sector", "Industry", "Full Time Employees"]:
                parent = span.parent
                if parent:
                    lines.append(parent.get_text(" ", strip=True))

        if lines:
            return source, "\n\n".join(lines)
        return source, f"Profile page loaded but limited data extracted for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_finviz(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape Finviz snapshot for analyst data and technicals."""
    source = "Finviz"
    try:
        url = f"https://finviz.com/quote.ashx?t={ticker}&ty=c&p=d&b=1"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        # Finviz uses a snapshot-table2 class for the key metrics grid
        tables = soup.find_all("table", class_="snapshot-table2")
        if not tables:
            # Fallback: look for any table with financial metrics
            tables = soup.find_all("table")

        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                # Finviz pairs metrics as label-value-label-value...
                pairs = []
                for i in range(0, len(cells) - 1, 2):
                    label = cells[i].get_text(strip=True)
                    value = cells[i + 1].get_text(strip=True)
                    if label and value:
                        pairs.append(f"{label}: {value}")
                if pairs:
                    lines.append(" | ".join(pairs))

        if lines:
            return source, "\n".join(lines[:50])  # Cap at 50 rows
        return source, f"Finviz loaded but no table data extracted for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_stockanalysis(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape StockAnalysis.com for financials and news."""
    source = "StockAnalysis"
    try:
        url = f"https://stockanalysis.com/stocks/{ticker.lower()}/financials/"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        # Extract financial tables
        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            for row in rows[:25]:
                cells = row.find_all(["td", "th"])
                row_text = " | ".join(c.get_text(strip=True) for c in cells)
                if row_text.strip() and len(row_text) < 500:
                    lines.append(row_text)

        if lines:
            return source, "\n".join(lines[:40])

        # Fallback: try the main quote page
        url2 = f"https://stockanalysis.com/stocks/{ticker.lower()}/"
        resp2 = requests.get(url2, headers=HEADERS, timeout=15)
        resp2.raise_for_status()
        soup2 = BeautifulSoup(resp2.text, "html.parser")

        for el in soup2.find_all(["td", "span", "div"]):
            text = el.get_text(" ", strip=True)
            if any(kw in text for kw in [
                "Market Cap", "Revenue", "EPS", "P/E", "Dividend",
                "52-Week", "Volume", "Shares",
            ]) and len(text) < 200:
                lines.append(text)

        if lines:
            return source, "\n".join(lines[:40])
        return source, f"StockAnalysis loaded but limited data for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_macrotrends(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape Macrotrends for historical financial data."""
    source = "Macrotrends"
    try:
        # First, search for the company to get the correct URL slug
        search_url = f"https://www.macrotrends.net/assets/php/fundamental_iframe.php?t={ticker}"
        resp = requests.get(search_url, headers=HEADERS, timeout=15, allow_redirects=True)
        # If search fails, try revenue page directly with common slug patterns
        if resp.status_code != 200:
            # Try the stock screener as fallback
            search_url = f"https://www.macrotrends.net/stocks/charts/{ticker}/{ticker.lower()}/revenue"
            resp = requests.get(search_url, headers=HEADERS, timeout=15, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            for row in rows[:20]:
                cells = row.find_all(["td", "th"])
                row_text = " | ".join(c.get_text(strip=True) for c in cells)
                if row_text.strip():
                    lines.append(row_text)

        if lines:
            return source, "\n".join(lines[:30])
        return source, f"Macrotrends loaded but limited data for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_sec_edgar(ticker: str) -> tuple[str, Optional[str]]:
    """Fetch latest 10-K filing summary from SEC EDGAR."""
    source = "SEC EDGAR"
    try:
        # Get CIK from ticker
        cik_url = f"https://efts.sec.gov/LATEST/search-index?q=%22{ticker}%22&dateRange=custom&startdt=2025-01-01&forms=10-K"
        edgar_headers = {**HEADERS, "Accept": "application/json"}

        # Use the EDGAR full-text search to find recent 10-K
        search_url = f"https://efts.sec.gov/LATEST/search-index?q={ticker}&forms=10-K&dateRange=custom&startdt=2024-01-01"
        resp = requests.get(search_url, headers=edgar_headers, timeout=15)

        # Fallback: use company search
        company_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=&CIK={ticker}&type=10-K&dateb=&owner=include&count=1&search_text=&action=getcompany"
        resp = requests.get(company_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(" ", strip=True)[:2000]
            if "10-K" in text:
                return source, f"SEC EDGAR filing search results for {ticker}:\n{text}"

        return source, f"SEC EDGAR search completed for {ticker} but no 10-K content extracted"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_openinsider(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape OpenInsider for recent insider trading activity."""
    source = "OpenInsider (Insider Trading)"
    try:
        url = f"http://openinsider.com/search?q={ticker}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = ["## Recent Insider Trades"]
        # Find the main insider trades table
        for table in soup.find_all("table", class_="tinytable"):
            rows = table.find_all("tr")
            for row in rows[:15]:  # Header + 14 trades
                cells = row.find_all(["td", "th"])
                if cells:
                    row_text = " | ".join(c.get_text(strip=True) for c in cells)
                    if row_text.strip() and len(row_text) > 10:
                        lines.append(row_text)

        if len(lines) > 1:
            return source, "\n".join(lines)
        return source, f"OpenInsider loaded but no insider trades found for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_barchart_options(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape Barchart for options overview and unusual activity."""
    source = "Barchart (Options)"
    try:
        url = f"https://www.barchart.com/stocks/quotes/{ticker}/overview"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        # Extract key data points from the overview page
        for el in soup.find_all(["span", "td", "div", "li"]):
            text = el.get_text(" ", strip=True)
            if any(kw in text for kw in [
                "Put/Call", "Implied Volatility", "Options Volume",
                "Open Interest", "IV Rank", "IV Percentile",
                "Historical Volatility", "Call Volume", "Put Volume",
                "Unusual", "Most Active",
            ]) and 5 < len(text) < 200:
                if text not in lines:
                    lines.append(text)

        # Also try the options overview page
        url2 = f"https://www.barchart.com/stocks/quotes/{ticker}/options-overview"
        resp2 = requests.get(url2, headers=HEADERS, timeout=15)
        if resp2.status_code == 200:
            soup2 = BeautifulSoup(resp2.text, "html.parser")
            for el in soup2.find_all(["span", "td", "div"]):
                text = el.get_text(" ", strip=True)
                if any(kw in text for kw in [
                    "Put/Call", "Implied Volatility", "Volume",
                    "Open Interest", "IV Rank", "IV Percentile",
                ]) and 5 < len(text) < 200:
                    if text not in lines:
                        lines.append(text)

        if lines:
            return source, "## Options Overview\n" + "\n".join(lines[:25])
        return source, f"Barchart loaded but limited options data for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_finviz_peers(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape Finviz for peer comparison by looking up the company's industry peers."""
    source = "Finviz (Peer Comparison)"
    try:
        # First get the ticker's industry from Finviz
        quote_url = f"https://finviz.com/quote.ashx?t={ticker}&ty=c&p=d&b=1"
        resp = requests.get(quote_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Find industry link and peers section
        peers = []
        for a in soup.find_all("a", class_="tab-link"):
            text = a.get_text(strip=True)
            href = a.get("href", "")
            if href.startswith("/quote.ashx?t=") and text != ticker:
                if text not in peers and len(text) <= 5:
                    peers.append(text)

        if not peers:
            # Fallback: find peers from the page
            for a in soup.find_all("a"):
                href = a.get("href", "")
                text = a.get_text(strip=True)
                if "/quote.ashx?t=" in href and text != ticker and re.match(r"^[A-Z]{1,5}$", text):
                    if text not in peers:
                        peers.append(text)
                    if len(peers) >= 5:
                        break

        if not peers:
            return source, f"No peer tickers found for {ticker}"

        # Now scrape the peer comparison screener
        peer_tickers = ",".join([ticker] + peers[:5])
        screener_url = f"https://finviz.com/screener.ashx?v=152&ft=4&t={peer_tickers}&o=-marketcap"
        resp2 = requests.get(screener_url, headers=HEADERS, timeout=15)
        resp2.raise_for_status()
        soup2 = BeautifulSoup(resp2.text, "html.parser")

        lines = [f"## Peer Comparison: {ticker} vs {', '.join(peers[:5])}"]

        # Look for the data table with actual stock data
        for table in soup2.find_all("table"):
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 5:
                    row_text = " | ".join(c.get_text(strip=True) for c in cells[:12])
                    # Filter for rows with ticker symbols or numeric data
                    if any(t in row_text for t in [ticker] + peers[:5]) or "Ticker" in row_text:
                        lines.append(row_text)

        if len(lines) > 1:
            return source, "\n".join(lines)
        return source, f"Peer comparison screener loaded but limited data for {ticker}. Peers found: {', '.join(peers)}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_capitol_trades(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape CapitolTrades for congressional/political trading activity."""
    source = "CapitolTrades (Congressional Trading)"
    try:
        url = f"https://www.capitoltrades.com/trades?ticker={ticker}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = ["## Congressional/Political Trading"]
        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            for row in rows[:12]:  # Header + 11 trades
                cells = row.find_all(["td", "th"])
                if cells:
                    row_text = " | ".join(c.get_text(strip=True)[:35] for c in cells)
                    if row_text.strip() and len(row_text) > 10:
                        lines.append(row_text)

        if len(lines) > 1:
            return source, "\n".join(lines)

        # Check for "no results" text
        page_text = soup.get_text(" ", strip=True)
        if "no results" in page_text.lower() or "no trades" in page_text.lower():
            return source, f"No congressional trades found for {ticker}"
        return source, f"CapitolTrades loaded but no trade data extracted for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_tradingview(ticker: str, exchange: str = "NASDAQ") -> tuple[str, Optional[str]]:
    """Get structured technical analysis from TradingView via tradingview_ta."""
    source = "TradingView Technical Analysis"
    try:
        from tradingview_ta import TA_Handler, Interval

        # Try common US exchanges in order
        exchanges = [exchange, "NASDAQ", "NYSE", "AMEX"]
        analysis = None
        used_exchange = None
        for ex in exchanges:
            try:
                handler = TA_Handler(
                    symbol=ticker, screener="america",
                    exchange=ex, interval=Interval.INTERVAL_1_DAY,
                )
                analysis = handler.get_analysis()
                used_exchange = ex
                break
            except Exception:
                continue

        if not analysis:
            return source, None

        ind = analysis.indicators
        lines = [f"Exchange: {used_exchange}", ""]

        # Price data
        lines.append("## Price Data")
        for key in ["close", "open", "high", "low", "volume", "change"]:
            val = ind.get(key)
            if val is not None:
                if key == "volume":
                    lines.append(f"{key}: {val:,.0f}")
                elif key == "change":
                    lines.append(f"{key}: {val:+.2f}%")
                else:
                    lines.append(f"{key}: ${val:.2f}")

        # Overall recommendation
        lines.append("")
        lines.append("## TradingView Composite Signals")
        summary = analysis.summary
        lines.append(f"Overall: {summary['RECOMMENDATION']} (Buy: {summary['BUY']}, Sell: {summary['SELL']}, Neutral: {summary['NEUTRAL']})")
        osc = analysis.oscillators
        lines.append(f"Oscillators: {osc['RECOMMENDATION']} (Buy: {osc['BUY']}, Sell: {osc['SELL']}, Neutral: {osc['NEUTRAL']})")
        ma = analysis.moving_averages
        lines.append(f"Moving Averages: {ma['RECOMMENDATION']} (Buy: {ma['BUY']}, Sell: {ma['SELL']}, Neutral: {ma['NEUTRAL']})")

        # Key oscillator values
        lines.append("")
        lines.append("## Oscillator Values")
        osc_keys = [
            ("RSI", "RSI (14)"), ("Stoch.K", "Stochastic %K"),
            ("Stoch.D", "Stochastic %D"), ("CCI20", "CCI (20)"),
            ("ADX", "ADX (14)"), ("MACD.macd", "MACD"),
            ("MACD.signal", "MACD Signal"), ("Mom", "Momentum"),
            ("W.R", "Williams %R"), ("AO", "Awesome Oscillator"),
        ]
        for key, label in osc_keys:
            val = ind.get(key)
            signal = osc.get("COMPUTE", {}).get(key.split(".")[0] if "." not in key else key.replace(".", "").replace("macd", ""), "")
            if val is not None:
                lines.append(f"{label}: {val:.2f} ({signal})" if signal else f"{label}: {val:.2f}")

        # Moving average values
        lines.append("")
        lines.append("## Moving Average Values")
        ma_keys = [
            ("EMA10", "EMA 10"), ("SMA20", "SMA 20"), ("EMA50", "EMA 50"),
            ("SMA50", "SMA 50"), ("EMA200", "EMA 200"), ("SMA200", "SMA 200"),
            ("VWMA", "VWMA"),
        ]
        for key, label in ma_keys:
            val = ind.get(key)
            signal = ma.get("COMPUTE", {}).get(key, "")
            if val is not None:
                close = ind.get("close", 0)
                pct = ((close - val) / val * 100) if val else 0
                lines.append(f"{label}: ${val:.2f} ({pct:+.1f}% from price) — {signal}")

        # Bollinger Bands and Pivots
        lines.append("")
        lines.append("## Bollinger Bands & Pivot Points")
        bb_upper = ind.get("BB.upper")
        bb_lower = ind.get("BB.lower")
        if bb_upper and bb_lower:
            lines.append(f"Bollinger Upper: ${bb_upper:.2f}")
            lines.append(f"Bollinger Lower: ${bb_lower:.2f}")
        pivot = ind.get("Pivot.M.Classic.Middle")
        s1 = ind.get("Pivot.M.Classic.S1")
        r1 = ind.get("Pivot.M.Classic.R1")
        if pivot:
            lines.append(f"Monthly Pivot: ${pivot:.2f}")
        if s1:
            lines.append(f"Support 1 (S1): ${s1:.2f}")
        if r1:
            lines.append(f"Resistance 1 (R1): ${r1:.2f}")

        # Individual MA signals for detailed breakdown
        lines.append("")
        lines.append("## Individual MA Signals")
        for key, signal in ma.get("COMPUTE", {}).items():
            val = ind.get(key)
            if val is not None:
                lines.append(f"{key}: ${val:.2f} — {signal}")

        return source, "\n".join(lines)
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_yahoo_news(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape recent news headlines from Yahoo Finance."""
    source = "Yahoo Finance News"
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}/news/"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        headlines = []
        # Look for news article links
        for a in soup.find_all("a"):
            href = a.get("href", "")
            text = a.get_text(strip=True)
            if (("/news/" in href or "/m/" in href or "finance.yahoo.com" in href)
                    and len(text) > 25 and len(text) < 300
                    and text not in [h.split(" — ", 1)[-1] if " — " in h else h for h in headlines]):
                headlines.append(text)
                if len(headlines) >= 10:
                    break

        # Also try finding article elements with h3 tags
        if len(headlines) < 3:
            for h3 in soup.find_all("h3"):
                text = h3.get_text(strip=True)
                if len(text) > 20 and len(text) < 300 and text not in headlines:
                    headlines.append(text)
                    if len(headlines) >= 10:
                        break

        if headlines:
            return source, "## Recent News Headlines\n" + "\n".join(f"- {h}" for h in headlines)
        return source, f"Yahoo Finance News loaded but no headlines extracted for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_google_news_rss(ticker: str, company_name: str = "") -> tuple[str, Optional[str]]:
    """Fetch recent news from Google News RSS feed for the ticker."""
    source = "Google News"
    try:
        # Google News RSS supports search queries
        query = f"{ticker} stock"
        if company_name:
            query = f"{company_name} {ticker} stock"
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        # Parse RSS XML
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
                    # Parse and simplify the date
                    date_text = pub_date.get_text(strip=True)
                    # Extract just the date portion
                    try:
                        from email.utils import parsedate_to_datetime
                        dt = parsedate_to_datetime(date_text)
                        line += f" ({dt.strftime('%b %d')})"
                    except Exception:
                        pass
                headlines.append(f"- {line}")

        if headlines:
            return source, "## Recent News (Google News)\n" + "\n".join(headlines)
        return source, f"Google News RSS returned no results for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_industry_trends(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape Finviz sector performance and industry data for context."""
    source = "Industry & Sector Trends"
    try:
        lines = []

        # Finviz sector performance page
        url = "https://finviz.com/groups.ashx?g=sector&v=140&o=-perf1w"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            for row in rows[:15]:
                cells = row.find_all(["td", "th"])
                row_text = " | ".join(c.get_text(strip=True) for c in cells)
                if row_text.strip() and any(kw in row_text for kw in [
                    "Technology", "Healthcare", "Financial", "Energy", "Consumer",
                    "Industrial", "Basic Materials", "Communication", "Utilities",
                    "Real Estate", "Sector", "Name", "Perf",
                ]):
                    lines.append(row_text)

        # Also get industry-level performance
        url2 = "https://finviz.com/groups.ashx?g=industry&v=140&o=-perf1w"
        resp2 = requests.get(url2, headers=HEADERS, timeout=15)
        if resp2.status_code == 200:
            soup2 = BeautifulSoup(resp2.text, "html.parser")
            for table in soup2.find_all("table"):
                rows = table.find_all("tr")
                for row in rows[:30]:
                    cells = row.find_all(["td", "th"])
                    row_text = " | ".join(c.get_text(strip=True) for c in cells)
                    if row_text.strip() and len(row_text) > 10:
                        lines.append(row_text)

        if lines:
            return source, "## Sector & Industry Performance\n" + "\n".join(lines[:40])
        return source, "Sector/industry performance data loaded but limited extraction"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


def scrape_etf_com(ticker: str) -> tuple[str, Optional[str]]:
    """Scrape etf.com for ETF-specific data."""
    source = "ETF.com"
    try:
        url = f"https://www.etf.com/{ticker}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        lines = []
        for el in soup.find_all(["td", "span", "div", "li"]):
            text = el.get_text(" ", strip=True)
            if any(kw in text for kw in [
                "Expense Ratio", "AUM", "Holdings", "Yield", "Inception",
                "Index", "Issuer", "Structure",
            ]) and len(text) < 200:
                lines.append(text)

        if lines:
            return source, "\n".join(lines[:30])
        return source, f"ETF.com loaded but limited data for {ticker}"
    except Exception as e:
        print(f"Warning: {source} failed: {e}", file=sys.stderr)
        return source, None


# ---------------------------------------------------------------------------
# Gemini synthesis
# ---------------------------------------------------------------------------

def load_system_prompt() -> str:
    """Load the system prompt from references/stock-research-prompt.md."""
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text()
    # Fallback minimal prompt
    return (
        "You are an expert investment analyst. Given scraped financial data, "
        "produce a comprehensive investment research report in markdown format."
    )


def synthesize_with_gemini(ticker: str, asset_type: str, scraped_data: dict[str, str],
                           model: str = DEFAULT_MODEL) -> str:
    """Send all scraped data to Claude with extended thinking for synthesis.

    Uses extended thinking (8K budget) for deeper analytical planning before
    writing the investment research report.
    """
    from anthropic import Anthropic

    api_key = os.environ.get("LITELLM_API_KEY")
    base_url = os.environ.get("LITELLM_BASE_URL")
    if not api_key or not base_url:
        print(
            "Error: LITELLM_API_KEY and LITELLM_BASE_URL required.\n"
            "Configure in ~/.claude-litellm.env",
            file=sys.stderr,
        )
        sys.exit(1)

    client = Anthropic(api_key=api_key, base_url=base_url)
    system_prompt = load_system_prompt()

    # Build context from all scraped sources
    context_parts = []
    failed_sources = []
    for source_name, data in scraped_data.items():
        if data:
            context_parts.append(f"### {source_name}\n\n{data}")
        else:
            failed_sources.append(source_name)

    context = "\n\n---\n\n".join(context_parts)

    query = f"Produce a comprehensive investment research report for {ticker} (asset type: {asset_type})."
    if failed_sources:
        query += f"\n\nNote: The following sources were unavailable: {', '.join(failed_sources)}. Work with the data available and note any gaps."

    user_msg = f"## Scraped Financial Data\n\n{context}\n\n---\n\n## Task\n\n{query}"

    print(f"Synthesizing with {model} (extended thinking)...", file=sys.stderr)

    try:
        with client.messages.stream(
            model=model,
            max_tokens=24000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_msg}],
            temperature=1,  # Required for extended thinking
            thinking={
                "type": "enabled",
                "budget_tokens": 8000,
            },
        ) as stream:
            for event in stream:
                pass

        response = stream.get_final_message()
    except Exception as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract text block (skip thinking blocks)
    result = ""
    for block in response.content:
        if block.type == "text":
            result = block.text
            break

    if not result:
        print("Warning: Empty response from model", file=sys.stderr)
        return ""

    usage = response.usage
    if usage:
        print(
            f"Tokens — input: {usage.input_tokens:,}, "
            f"output: {usage.output_tokens:,}",
            file=sys.stderr,
        )

    return result


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_obsidian_output(ticker: str, asset_type: str, report: str) -> str:
    """Wrap the Gemini report with Obsidian YAML frontmatter and wiki-links."""
    today = datetime.now().strftime("%Y-%m-%d")

    if asset_type == "sector":
        tags_extra = f"  - sector\n  - {ticker.lower()}"
    elif asset_type == "etf":
        tags_extra = f"  - etf\n  - {ticker}"
    else:
        tags_extra = f"  - stock\n  - {ticker}"

    frontmatter = f"""---
date: {today}
tags:
  - investment-research
{tags_extra}
source: claude-code
project: personal-investing
ticker: {ticker}
type: {asset_type}
---

"""

    wiki_links = f"> Related: [[investment-watchlist]] [[portfolio-notes]]\n\n"

    return frontmatter + wiki_links + report


def output_filename(ticker: str, asset_type: str) -> Path:
    """Generate the output file path."""
    date_suffix = datetime.now().strftime("%Y-%m")
    if asset_type == "sector":
        name = f"sector-{ticker.lower()}-{date_suffix}.md"
    else:
        name = f"{ticker}-{date_suffix}.md"
    return OBSIDIAN_BASE / name


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Stock/ETF/Sector investment research")
    parser.add_argument("ticker", help="Stock ticker, company name, ETF symbol, or sector name")
    parser.add_argument(
        "--type", "-t", choices=["stock", "etf", "sector"], default="stock",
        help="Asset type (default: stock)",
    )
    parser.add_argument("--output", "-o", default=None, help="Custom output file path")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"LLM model (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    asset_type = args.type
    ticker_input = args.ticker

    # Resolve ticker
    if asset_type == "sector":
        ticker = ticker_input.lower().replace(" ", "-")
        print(f"Researching sector: {ticker}", file=sys.stderr)
    else:
        ticker = resolve_ticker(ticker_input)
        if not ticker:
            print(f"Error: Could not resolve ticker for '{ticker_input}'", file=sys.stderr)
            sys.exit(1)
        print(f"Researching {asset_type}: {ticker}", file=sys.stderr)

    # Scrape data
    print("Scraping financial data...", file=sys.stderr)
    scraped = {}

    if asset_type == "stock":
        scrapers = [
            ("Yahoo Finance Quote", lambda: scrape_yahoo_quote(ticker)),
            ("Yahoo Finance Profile", lambda: scrape_yahoo_profile(ticker)),
            ("Finviz", lambda: scrape_finviz(ticker)),
            ("TradingView Technical Analysis", lambda: scrape_tradingview(ticker)),
            ("StockAnalysis", lambda: scrape_stockanalysis(ticker)),
            ("Macrotrends", lambda: scrape_macrotrends(ticker)),
            ("SEC EDGAR", lambda: scrape_sec_edgar(ticker)),
            ("OpenInsider (Insider Trading)", lambda: scrape_openinsider(ticker)),
            ("Barchart (Options)", lambda: scrape_barchart_options(ticker)),
            ("Finviz (Peer Comparison)", lambda: scrape_finviz_peers(ticker)),
            ("CapitolTrades (Congressional)", lambda: scrape_capitol_trades(ticker)),
            ("Yahoo Finance News", lambda: scrape_yahoo_news(ticker)),
            ("Google News", lambda: scrape_google_news_rss(ticker)),
            ("Industry & Sector Trends", lambda: scrape_industry_trends(ticker)),
        ]
    elif asset_type == "etf":
        scrapers = [
            ("Yahoo Finance Quote", lambda: scrape_yahoo_quote(ticker)),
            ("Yahoo Finance Profile", lambda: scrape_yahoo_profile(ticker)),
            ("Finviz", lambda: scrape_finviz(ticker)),
            ("TradingView Technical Analysis", lambda: scrape_tradingview(ticker)),
            ("ETF.com", lambda: scrape_etf_com(ticker)),
            ("StockAnalysis", lambda: scrape_stockanalysis(ticker)),
            ("Yahoo Finance News", lambda: scrape_yahoo_news(ticker)),
            ("Google News", lambda: scrape_google_news_rss(ticker)),
            ("Industry & Sector Trends", lambda: scrape_industry_trends(ticker)),
        ]
    else:  # sector
        scrapers = [
            ("Finviz Sector", lambda: scrape_finviz(ticker_input)),
            ("Yahoo Finance", lambda: scrape_yahoo_quote(ticker_input)),
            ("StockAnalysis", lambda: scrape_stockanalysis(ticker_input)),
            ("Google News", lambda: scrape_google_news_rss(ticker_input)),
            ("Industry & Sector Trends", lambda: scrape_industry_trends(ticker_input)),
        ]

    # Scrape all sources concurrently for speed
    def _run_scraper(item):
        name, fn = item
        print(f"  Scraping {name}...", file=sys.stderr)
        _, data = fn()
        return name, data

    with ThreadPoolExecutor(max_workers=min(len(scrapers), 10)) as pool:
        futures = {pool.submit(_run_scraper, s): s[0] for s in scrapers}
        for future in as_completed(futures):
            name, data = future.result()
            scraped[name] = data

    sources_ok = sum(1 for v in scraped.values() if v)
    sources_total = len(scraped)
    print(f"Scraped {sources_ok}/{sources_total} sources in parallel", file=sys.stderr)

    if sources_ok == 0:
        print("Error: All sources failed. Cannot produce report.", file=sys.stderr)
        sys.exit(1)

    # Synthesize with Gemini
    report = synthesize_with_gemini(ticker, asset_type, scraped, model=args.model)

    # Format output
    output = format_obsidian_output(ticker, asset_type, report)

    # Write to file
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = output_filename(ticker, asset_type)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output)
    print(f"Report saved to: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
