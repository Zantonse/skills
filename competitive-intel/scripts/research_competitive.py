#!/usr/bin/env python3
"""Competitive intelligence orchestrator — parallel scraping + Gemini synthesis.

Usage:
    python3 research_competitive.py                          # landscape mode (all vendors)
    python3 research_competitive.py --mode landscape         # same as above
    python3 research_competitive.py --mode quick 'Ping'      # quick call-prep brief
    python3 research_competitive.py -m quick 'Entra'
    python3 research_competitive.py --competitors ping,entra,cyberark
    python3 research_competitive.py --model gemini-3.1-pro-preview

Modes:
    landscape  — full refresh across all tracked vendors, updates battlecards + landscape doc
    quick      — fast call-prep brief for a single vendor (no Obsidian write)

Environment:
    LITELLM_API_KEY + LITELLM_BASE_URL (set in ~/.claude-litellm.env)
"""

import argparse
import json
import os
import re
import subprocess
import sys
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
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export ") and "=" in line:
                    line = line[7:]
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"")
                # Resolve $VAR references
                if value.startswith("$"):
                    ref_var = value[1:]
                    value = os.environ.get(ref_var, "")
                if key and value:
                    os.environ[key] = value


_load_env_file()


def _ensure_packages():
    """Install required packages if missing."""
    for pkg, import_name in [
        ("requests", "requests"),
        ("beautifulsoup4", "bs4"),
        ("openai", "openai"),
    ]:
        try:
            __import__(import_name)
        except ImportError:
            print(f"Installing {pkg}...", file=sys.stderr)
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )


_ensure_packages()

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
PROMPT_FILE = SKILL_DIR / "references" / "competitive-intel-prompt.md"
OBSIDIAN_BASE = Path.home() / "Documents" / "ObsidianNotes" / "Claude-Research" / "competitive-intel"
DEFAULT_MODEL = "gemini-3.1-pro-preview"
MAX_WORKERS = 20
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
}

# ---------------------------------------------------------------------------
# Firecrawl search helper
# ---------------------------------------------------------------------------

_FIRECRAWL_API_KEY = None


def _get_firecrawl_key() -> Optional[str]:
    """Load firecrawl API key from ~/.claude.json MCP server config."""
    global _FIRECRAWL_API_KEY
    if _FIRECRAWL_API_KEY is not None:
        return _FIRECRAWL_API_KEY or None

    claude_json = Path.home() / ".claude.json"
    if not claude_json.exists():
        _FIRECRAWL_API_KEY = ""
        return None
    try:
        with open(claude_json) as f:
            config = json.load(f)
        # Navigate mcpServers -> firecrawl -> env -> FIRECRAWL_API_KEY
        key = (
            config.get("mcpServers", {})
            .get("firecrawl", {})
            .get("env", {})
            .get("FIRECRAWL_API_KEY", "")
        )
        _FIRECRAWL_API_KEY = key
        return key or None
    except Exception:
        _FIRECRAWL_API_KEY = ""
        return None


def firecrawl_search(query: str, limit: int = 5) -> Optional[list]:
    """Call Firecrawl /v1/search API. Returns list of {title, url, markdown} or None."""
    api_key = _get_firecrawl_key()
    if not api_key:
        return None
    try:
        resp = requests.post(
            "https://api.firecrawl.dev/v1/search",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "query": query,
                "limit": limit,
                "scrapeOptions": {
                    "formats": ["markdown"],
                    "onlyMainContent": True,
                },
            },
            timeout=30,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        results = data.get("data", [])
        if not results:
            return None
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "markdown": r.get("markdown", "")[:2000],
            }
            for r in results
        ]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Vendor registry
# ---------------------------------------------------------------------------

VENDORS = {
    "ping": {
        "name": "Ping Identity",
        "domain": "pingidentity.com",
        "newsroom_url": "https://www.pingidentity.com/en/company/press-releases-folder.html",
        "blog_url": "https://www.pingidentity.com/en/resources/blog.html",
        "changelog_url": None,
        "github_org": "pingidentity",
        "aliases": ["Ping", "PingOne", "PingFederate", "PingAccess"],
        "is_self": False,
    },
    "forgerock": {
        "name": "ForgeRock",
        "domain": "forgerock.com",
        "newsroom_url": "https://www.forgerock.com/blog",
        "blog_url": "https://www.forgerock.com/blog",
        "changelog_url": None,
        "github_org": "ForgeRock",
        "aliases": ["ForgeRock", "PingOne Advanced Identity Cloud"],
        "is_self": False,
    },
    "entra": {
        "name": "Microsoft Entra",
        "domain": "microsoft.com",
        "newsroom_url": "https://www.microsoft.com/en-us/security/blog/",
        "blog_url": "https://techcommunity.microsoft.com/category/microsoft-entra/blog/identity",
        "changelog_url": "https://learn.microsoft.com/en-us/entra/fundamentals/whats-new",
        "github_org": "AzureAD",
        "aliases": ["Entra ID", "Azure AD", "Azure Active Directory", "Microsoft Entra ID"],
        "is_self": False,
    },
    "cyberark": {
        "name": "CyberArk",
        "domain": "cyberark.com",
        "newsroom_url": "https://www.cyberark.com/press/",
        "blog_url": "https://www.cyberark.com/blog/",
        "changelog_url": None,
        "github_org": "cyberark",
        "aliases": ["CyberArk", "CyberArk Identity", "CyberArk PAM"],
        "is_self": False,
    },
    "sailpoint": {
        "name": "SailPoint",
        "domain": "sailpoint.com",
        "newsroom_url": "https://www.sailpoint.com/press-releases/",
        "blog_url": "https://www.sailpoint.com/blog/",
        "changelog_url": None,
        "github_org": "sailpoint-oss",
        "aliases": ["SailPoint", "SailPoint IdentityNow", "SailPoint ISC"],
        "is_self": False,
    },
    "lumos": {
        "name": "Lumos",
        "domain": "lumos.com",
        "newsroom_url": None,
        "blog_url": "https://www.lumos.com/blog",
        "changelog_url": None,
        "github_org": None,
        "aliases": ["Lumos", "Lumos Identity"],
        "is_self": False,
    },
    "conductorone": {
        "name": "ConductorOne",
        "domain": "conductorone.com",
        "newsroom_url": None,
        "blog_url": "https://www.conductorone.com/blog/",
        "changelog_url": None,
        "github_org": "ConductorOne",
        "aliases": ["ConductorOne", "Conductor One", "C1"],
        "is_self": False,
    },
    "self": {
        "name": "Okta",
        "domain": "okta.com",
        "newsroom_url": "https://www.okta.com/press-room/",
        "blog_url": "https://www.okta.com/blog/",
        "changelog_url": "https://help.okta.com/en-us/content/topics/releasenotes/production.htm",
        "github_org": "okta",
        "aliases": ["Okta", "Auth0", "Okta Workforce Identity", "Okta CIC"],
        "is_self": True,
    },
}

DEFAULT_COMPETITORS = ["ping", "forgerock", "entra", "cyberark", "sailpoint", "lumos", "conductorone"]

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Convert vendor name to URL-friendly slug."""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def resolve_vendor(query: str) -> dict:
    """Resolve a vendor name/alias to a registry entry. Falls back to ad-hoc entry."""
    q = query.lower().strip()
    # Check exact slug match
    if q in VENDORS:
        return VENDORS[q]
    # Check aliases (case-insensitive)
    for slug, vendor in VENDORS.items():
        for alias in vendor.get("aliases", []):
            if alias.lower() == q:
                return vendor
    # Ad-hoc vendor not in registry
    domain_guess = re.sub(r'[^a-z0-9]', '', q) + ".com"
    return {
        "name": query,
        "domain": domain_guess,
        "newsroom_url": None,
        "blog_url": None,
        "changelog_url": None,
        "github_org": None,
        "aliases": [query],
        "is_self": False,
    }


def load_prompts() -> dict:
    """Load the three Gemini prompts from the reference file, keyed by section header."""
    prompts = {}
    if not os.path.exists(PROMPT_FILE):
        return prompts
    with open(PROMPT_FILE) as f:
        content = f.read()
    # Split on ## PROMPT_ headers
    sections = re.split(r'^## (PROMPT_\w+)', content, flags=re.MULTILINE)
    for i in range(1, len(sections), 2):
        key = sections[i].strip()
        body = sections[i + 1].strip() if i + 1 < len(sections) else ""
        prompts[key] = body
    return prompts


def battlecard_path(vendor: dict) -> str:
    """Path for a vendor's evergreen battlecard."""
    slug = slugify(vendor["name"])
    return os.path.join(OBSIDIAN_BASE, f"{slug}.md")


def landscape_path() -> str:
    """Path for the periodic landscape summary."""
    month = datetime.now().strftime("%Y-%m")
    return os.path.join(OBSIDIAN_BASE, f"landscape-{month}.md")


def read_existing_doc(path: str) -> Optional[str]:
    """Read an existing Obsidian doc, or return None."""
    if os.path.isfile(path):
        with open(path) as f:
            return f.read()
    return None


def extract_my_notes(doc: str) -> Optional[str]:
    """Extract the ## My Notes section from an existing battlecard."""
    match = re.search(r'(## My Notes.*)', doc, re.DOTALL)
    return match.group(1) if match else None


def extract_changes(gemini_output: str) -> str:
    """Extract the CHANGES: section from Gemini's battlecard output."""
    match = re.search(r'---\s*\nCHANGES:\s*\n(.*)', gemini_output, re.DOTALL)
    return match.group(1).strip() if match else "No changes detected."


def strip_changes_section(gemini_output: str) -> str:
    """Remove the CHANGES: section from Gemini output."""
    return re.sub(r'\n---\s*\nCHANGES:.*', '', gemini_output, flags=re.DOTALL).strip()


def format_frontmatter(vendor: dict, doc_type: str = "battlecard") -> str:
    """Generate Obsidian YAML frontmatter."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(vendor["name"])
    if doc_type == "landscape":
        return f"""---
date: {date_str}
tags:
  - competitive-intel
  - landscape
source: claude-code
project: se-competitive
---

> Related: [[competitive-intel-index]]

"""
    return f"""---
date: {date_str}
tags:
  - competitive-intel
  - {slug}
source: claude-code
project: se-competitive
last-updated: {date_str}
---

> Related: [[competitive-intel-index]] [[landscape-{datetime.now().strftime('%Y-%m')}]]

"""

# ---------------------------------------------------------------------------
# CLI parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Competitive intelligence: parallel scraping + Gemini synthesis"
    )
    parser.add_argument(
        "vendor", nargs="?", default=None,
        help="Vendor name for quick mode (e.g., 'Ping')"
    )
    parser.add_argument(
        "--mode", "-m", choices=["landscape", "quick"],
        default="landscape", help="Mode: landscape (all vendors) or quick (single vendor call prep)"
    )
    parser.add_argument(
        "--competitors", "-c", default=None,
        help="Comma-separated vendor slugs to override defaults"
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="LLM model for synthesis")
    args = parser.parse_args()
    if args.mode == "quick" and not args.vendor:
        parser.error("Quick mode requires a vendor name: --mode quick 'Ping'")
    return args

# ---------------------------------------------------------------------------
# Scrapers
# ---------------------------------------------------------------------------

def scrape_google_news(vendor: dict) -> tuple:
    """Google News RSS — recent news mentions for the vendor."""
    name = "Google News"
    try:
        aliases = vendor.get("aliases", [vendor["name"]])
        query = " OR ".join(f'"{a}"' for a in aliases[:3])
        url = (
            f"https://news.google.com/rss/search"
            f"?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
        )
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "xml")
        items = soup.find_all("item")[:15]
        if not items:
            return (name, None)
        lines = []
        for item in items:
            title = item.find("title")
            source = item.find("source")
            pubdate = item.find("pubDate")
            t = title.get_text(strip=True) if title else "No title"
            s = source.get_text(strip=True) if source else "Unknown source"
            d = pubdate.get_text(strip=True) if pubdate else ""
            lines.append(f"- {t} ({s}, {d})")
        return (name, "\n".join(lines))
    except Exception as e:
        print(f"  [{vendor['name']}] google_news error: {e}", file=sys.stderr)
        return (name, None)


def scrape_newsroom(vendor: dict) -> tuple:
    """Vendor newsroom / press releases page."""
    name = "Newsroom"
    try:
        urls_to_try = []
        if vendor.get("newsroom_url"):
            urls_to_try.append(vendor["newsroom_url"])
        domain = vendor.get("domain", "")
        if domain:
            for path in ["/press", "/press-releases", "/newsroom", "/news"]:
                urls_to_try.append(f"https://www.{domain}{path}")
        for url in urls_to_try:
            try:
                resp = requests.get(url, headers=HEADERS, timeout=10)
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                for tag in soup(["nav", "footer", "script", "style", "header"]):
                    tag.decompose()
                text = soup.get_text(separator="\n", strip=True)
                text = re.sub(r'\n{3,}', '\n\n', text)
                if len(text) > 200:
                    return (name, text[:4000])
            except Exception:
                continue
        return (name, None)
    except Exception as e:
        print(f"  [{vendor['name']}] newsroom error: {e}", file=sys.stderr)
        return (name, None)


def scrape_blog(vendor: dict) -> tuple:
    """Vendor engineering / product blog."""
    name = "Blog"
    try:
        domain = vendor.get("domain", "")
        urls_to_try = []
        if vendor.get("blog_url"):
            urls_to_try.append(vendor["blog_url"])
        if domain:
            urls_to_try.append(f"https://www.{domain}/blog")
        for url in urls_to_try:
            try:
                resp = requests.get(url, headers=HEADERS, timeout=10)
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                for tag in soup(["nav", "footer", "script", "style", "header"]):
                    tag.decompose()
                text = soup.get_text(separator="\n", strip=True)
                text = re.sub(r'\n{3,}', '\n\n', text)
                if len(text) > 200:
                    return (name, text[:4000])
            except Exception:
                continue
        return (name, None)
    except Exception as e:
        print(f"  [{vendor['name']}] blog error: {e}", file=sys.stderr)
        return (name, None)


def scrape_crunchbase(vendor: dict) -> tuple:
    """Crunchbase funding / revenue / headcount data via Firecrawl search."""
    name = "Crunchbase / Funding"
    try:
        results = firecrawl_search(
            f"{vendor['name']} crunchbase funding revenue employees", limit=5
        )
        if not results:
            return (name, None)
        parts = []
        for r in results:
            title = r.get("title", "")
            url = r.get("url", "")
            md = r.get("markdown", "")
            if md:
                parts.append(f"**{title}** ({url})\n{md}")
        return (name, "\n\n---\n\n".join(parts) if parts else None)
    except Exception as e:
        print(f"  [{vendor['name']}] crunchbase error: {e}", file=sys.stderr)
        return (name, None)


def scrape_changelog(vendor: dict) -> tuple:
    """Product changelog / release notes."""
    name = "Changelog"
    try:
        domain = vendor.get("domain", "")
        urls_to_try = []
        if vendor.get("changelog_url"):
            urls_to_try.append(vendor["changelog_url"])
        if domain:
            for subdomain in ["www", "docs"]:
                for path in ["/changelog", "/release-notes", "/whats-new", "/updates"]:
                    urls_to_try.append(f"https://{subdomain}.{domain}{path}")
        for url in urls_to_try:
            try:
                resp = requests.get(url, headers=HEADERS, timeout=8)
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                for tag in soup(["nav", "footer", "script", "style", "header"]):
                    tag.decompose()
                text = soup.get_text(separator="\n", strip=True)
                text = re.sub(r'\n{3,}', '\n\n', text)
                if len(text) > 200:
                    return (name, text[:5000])
            except Exception:
                continue
        return (name, None)
    except Exception as e:
        print(f"  [{vendor['name']}] changelog error: {e}", file=sys.stderr)
        return (name, None)


def scrape_github(vendor: dict) -> tuple:
    """GitHub org repos via the GitHub public API."""
    name = "GitHub"
    try:
        github_org = vendor.get("github_org")
        if not github_org:
            return (name, None)
        url = (
            f"https://api.github.com/orgs/{github_org}/repos"
            f"?sort=updated&per_page=10"
        )
        headers = {"Accept": "application/vnd.github.v3+json"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        repos = resp.json()
        if not isinstance(repos, list) or not repos:
            return (name, None)
        lines = []
        for repo in repos:
            r_name = repo.get("name", "")
            lang = repo.get("language") or "N/A"
            stars = repo.get("stargazers_count", 0)
            desc = (repo.get("description") or "").strip()
            updated = (repo.get("updated_at") or "")[:10]
            lines.append(
                f"- {r_name} [{lang}, {stars} stars] {desc} (updated {updated})"
            )
        return (name, "\n".join(lines))
    except Exception as e:
        print(f"  [{vendor['name']}] github error: {e}", file=sys.stderr)
        return (name, None)


def scrape_dev_blog(vendor: dict) -> tuple:
    """Developer / API blog announcements via Firecrawl search."""
    name = "Developer Blog"
    try:
        results = firecrawl_search(
            f"{vendor['name']} developer blog API SDK integration announcement", limit=5
        )
        if not results:
            return (name, None)
        parts = []
        for r in results:
            title = r.get("title", "")
            url = r.get("url", "")
            md = r.get("markdown", "")
            if md:
                parts.append(f"**{title}** ({url})\n{md}")
        return (name, "\n\n---\n\n".join(parts) if parts else None)
    except Exception as e:
        print(f"  [{vendor['name']}] dev_blog error: {e}", file=sys.stderr)
        return (name, None)


def scrape_g2_trustradius(vendor: dict) -> tuple:
    """G2 / TrustRadius review data via Firecrawl search."""
    name = "G2 / TrustRadius Reviews"
    try:
        results = firecrawl_search(
            f"{vendor['name']} G2 OR TrustRadius reviews identity SSO IAM", limit=5
        )
        if not results:
            return (name, None)
        parts = []
        for r in results:
            title = r.get("title", "")
            url = r.get("url", "")
            md = r.get("markdown", "")
            if md:
                parts.append(f"**{title}** ({url})\n{md}")
        return (name, "\n\n---\n\n".join(parts) if parts else None)
    except Exception as e:
        print(f"  [{vendor['name']}] g2_trustradius error: {e}", file=sys.stderr)
        return (name, None)


def scrape_job_postings(vendor: dict) -> tuple:
    """Job postings via Firecrawl search — signals hiring priorities."""
    name = "Job Postings"
    try:
        results = firecrawl_search(
            f"{vendor['name']} hiring jobs engineer product security identity cloud", limit=5
        )
        if not results:
            return (name, None)
        parts = []
        for r in results:
            title = r.get("title", "")
            url = r.get("url", "")
            md = r.get("markdown", "")
            if md:
                parts.append(f"**{title}** ({url})\n{md}")
        return (name, "\n\n---\n\n".join(parts) if parts else None)
    except Exception as e:
        print(f"  [{vendor['name']}] job_postings error: {e}", file=sys.stderr)
        return (name, None)


def scrape_analyst_mentions(vendor: dict) -> tuple:
    """Analyst mentions (Gartner, Forrester, KuppingerCole) via Google News RSS."""
    name = "Analyst Mentions"
    try:
        query = (
            f"{vendor['name']} Gartner OR Forrester OR KuppingerCole "
            f"identity access management 2025 2026"
        )
        # Try Google News RSS first
        rss_url = (
            f"https://news.google.com/rss/search"
            f"?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
        )
        resp = requests.get(rss_url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "xml")
        items = soup.find_all("item")
        keywords = re.compile(
            r'gartner|forrester|magic quadrant|wave|leader|kuppingercole|analyst',
            re.IGNORECASE,
        )
        lines = []
        for item in items:
            title = item.find("title")
            source = item.find("source")
            pubdate = item.find("pubDate")
            t = title.get_text(strip=True) if title else ""
            s = source.get_text(strip=True) if source else ""
            d = pubdate.get_text(strip=True) if pubdate else ""
            if keywords.search(t):
                lines.append(f"- {t} ({s}, {d})")
        if lines:
            return (name, "\n".join(lines))

        # Fallback: Google web search
        web_url = (
            f"https://www.google.com/search"
            f"?q={requests.utils.quote(query)}&num=10"
        )
        resp2 = requests.get(web_url, headers=HEADERS, timeout=10)
        resp2.raise_for_status()
        soup2 = BeautifulSoup(resp2.text, "html.parser")
        snippets = []
        seen = set()
        for el in soup2.find_all(["span", "div", "p"]):
            text = el.get_text(separator=" ", strip=True)
            if keywords.search(text) and len(text) > 40:
                key = text[:80]
                if key not in seen:
                    seen.add(key)
                    snippets.append(text[:500])
                if len(snippets) >= 6:
                    break
        if snippets:
            return (name, "\n\n".join(snippets))
        return (name, None)
    except Exception as e:
        print(f"  [{vendor['name']}] analyst_mentions error: {e}", file=sys.stderr)
        return (name, None)


# ---------------------------------------------------------------------------
# Scraper registry
# ---------------------------------------------------------------------------

SCRAPER_REGISTRY = {
    "google_news": scrape_google_news,
    "newsroom": scrape_newsroom,
    "blog": scrape_blog,
    "crunchbase": scrape_crunchbase,
    "changelog": scrape_changelog,
    "github": scrape_github,
    "dev_blog": scrape_dev_blog,
    "g2_trustradius": scrape_g2_trustradius,
    "job_postings": scrape_job_postings,
    "analyst_mentions": scrape_analyst_mentions,
}

# ---------------------------------------------------------------------------
# Vendor scraping
# ---------------------------------------------------------------------------

def scrape_vendor(vendor: dict) -> dict:
    """Run all 10 scrapers for a single vendor. Returns {source_name: data}."""
    scraped = {}
    for scraper_name, scraper_fn in SCRAPER_REGISTRY.items():
        try:
            source_name, data = scraper_fn(vendor)
            scraped[source_name] = data
            status = "✓" if data else "✗"
            print(f"  [{vendor['name']}] [{status}] {source_name}", file=sys.stderr)
        except Exception as e:
            print(f"  [{vendor['name']}] [✗ ERROR] {scraper_name}: {e}", file=sys.stderr)
            scraped[scraper_name] = None
    return scraped


# ---------------------------------------------------------------------------
# Gemini synthesis helpers
# ---------------------------------------------------------------------------

def _make_client():
    """Build and return an OpenAI-compatible client pointed at LiteLLM."""
    from openai import OpenAI

    api_key = os.environ.get("LITELLM_API_KEY")
    base_url = os.environ.get("LITELLM_BASE_URL", "").rstrip("/")
    if not api_key or not base_url:
        print("Error: LITELLM_API_KEY and LITELLM_BASE_URL required.", file=sys.stderr)
        sys.exit(1)
    if not base_url.endswith("/v1"):
        base_url += "/v1"
    return OpenAI(api_key=api_key, base_url=base_url)


def _format_scraped(scraped: dict) -> str:
    """Convert a scraped dict into a readable block for LLM consumption."""
    parts = []
    for source, data in scraped.items():
        if data:
            parts.append(f"### {source}\n{data}")
        else:
            parts.append(f"### {source}\n(no data)")
    return "\n\n".join(parts)


def synthesize_battlecard(
    vendor: dict,
    scraped: dict,
    self_scraped: dict,
    prompts: dict,
    model: str,
    existing_doc: Optional[str] = None,
) -> str:
    """Send vendor scrape data + self-product data to Gemini for battlecard synthesis."""
    client = _make_client()

    system_prompt = prompts.get("PROMPT_BATTLECARD_UPDATE", "")

    date_str = datetime.now().strftime("%Y-%m-%d")
    competitor_block = _format_scraped(scraped)
    self_block = _format_scraped(self_scraped)

    user_parts = [
        f"Vendor: {vendor['name']}",
        f"Domain: {vendor.get('domain', 'N/A')}",
        f"Date: {date_str}",
        "",
        "## Scraped Competitor Data",
        competitor_block,
        "",
        "## [SELF] Okta Product Data",
        self_block,
    ]

    if existing_doc:
        my_notes = extract_my_notes(existing_doc)
        user_parts += [
            "",
            "## Previous Battlecard",
            existing_doc,
        ]
        if my_notes:
            user_parts += [
                "",
                "IMPORTANT: Preserve the '## My Notes' section exactly as written above.",
            ]

    user_message = "\n".join(user_parts)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=8000,
        temperature=0.3,
    )

    usage = response.usage
    if usage:
        print(
            f"  [{vendor['name']}] tokens: prompt={usage.prompt_tokens} "
            f"completion={usage.completion_tokens} total={usage.total_tokens}",
            file=sys.stderr,
        )

    return response.choices[0].message.content


def synthesize_landscape(
    change_summaries: dict,
    prompts: dict,
    model: str,
    existing_doc: Optional[str] = None,
) -> str:
    """Cross-vendor landscape analysis from per-vendor change summaries."""
    client = _make_client()

    system_prompt = prompts.get("PROMPT_LANDSCAPE_SYNTHESIS", "")

    date_str = datetime.now().strftime("%Y-%m-%d")
    vendor_count = len(change_summaries)

    summary_block = "\n\n".join(
        f"### {vendor_name}\n{summary}"
        for vendor_name, summary in change_summaries.items()
    )

    user_parts = [
        f"Date: {date_str}",
        f"Vendors analyzed: {vendor_count}",
        "",
        "## Per-Vendor Change Summaries",
        summary_block,
    ]

    if existing_doc:
        user_parts += [
            "",
            "## Previous Landscape Document",
            existing_doc,
        ]

    user_message = "\n".join(user_parts)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=10000,
        temperature=0.3,
    )

    usage = response.usage
    if usage:
        print(
            f"  [Landscape] tokens: prompt={usage.prompt_tokens} "
            f"completion={usage.completion_tokens} total={usage.total_tokens}",
            file=sys.stderr,
        )

    return response.choices[0].message.content


def synthesize_quick_brief(
    vendor: dict,
    scraped: dict,
    self_scraped: dict,
    prompts: dict,
    model: str,
    existing_battlecard: Optional[str] = None,
) -> str:
    """Produce a concise call-prep brief for a single vendor."""
    client = _make_client()

    system_prompt = prompts.get("PROMPT_QUICK_BRIEF", "")

    date_str = datetime.now().strftime("%Y-%m-%d")
    competitor_block = _format_scraped(scraped)
    self_block = _format_scraped(self_scraped)

    user_parts = [
        f"Vendor: {vendor['name']}",
        f"Date: {date_str}",
        "",
        "## Scraped Competitor Data",
        competitor_block,
        "",
        "## [SELF] Okta Product Data",
        self_block,
    ]

    if existing_battlecard:
        user_parts += [
            "",
            "## Existing Battlecard",
            existing_battlecard,
        ]

    user_message = "\n".join(user_parts)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=4000,
        temperature=0.3,
    )

    usage = response.usage
    if usage:
        print(
            f"  [{vendor['name']}] quick brief tokens: prompt={usage.prompt_tokens} "
            f"completion={usage.completion_tokens} total={usage.total_tokens}",
            file=sys.stderr,
        )

    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Mode functions
# ---------------------------------------------------------------------------

def run_landscape_mode(args):
    """Full landscape refresh across all tracked vendors."""
    # 1. Parse competitor list
    if args.competitors:
        competitor_slugs = [s.strip() for s in args.competitors.split(",")]
    else:
        competitor_slugs = DEFAULT_COMPETITORS

    # 2. Resolve all vendors
    vendors = [resolve_vendor(slug) for slug in competitor_slugs]
    self_vendor = VENDORS["self"]

    # 3. Load prompts
    prompts = load_prompts()

    print(
        f"[landscape] Scraping {len(vendors)} competitors + self ({self_vendor['name']})...",
        file=sys.stderr,
    )

    # 4. Scrape self first
    print(f"\n[self] Scraping {self_vendor['name']}...", file=sys.stderr)
    self_scraped = scrape_vendor(self_vendor)

    # 5. Scrape all competitors in parallel (max 4 workers; each vendor is sequential internally)
    all_scraped: dict[str, dict] = {}
    worker_count = min(len(vendors), 4)

    print(f"\n[landscape] Scraping competitors (up to {worker_count} parallel)...", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_to_vendor = {
            executor.submit(scrape_vendor, vendor): vendor for vendor in vendors
        }
        for future in as_completed(future_to_vendor):
            vendor = future_to_vendor[future]
            try:
                all_scraped[vendor["name"]] = future.result()
            except Exception as e:
                print(f"  [{vendor['name']}] scrape failed: {e}", file=sys.stderr)
                all_scraped[vendor["name"]] = {}

    # 6. For each vendor: synthesize battlecard, extract changes, write file
    change_summaries: dict[str, str] = {}
    written_battlecards: list[str] = []

    print("\n[landscape] Synthesizing battlecards...", file=sys.stderr)

    os.makedirs(OBSIDIAN_BASE, exist_ok=True)

    for vendor in vendors:
        vendor_name = vendor["name"]
        scraped = all_scraped.get(vendor_name, {})
        bc_path = battlecard_path(vendor)
        existing_doc = read_existing_doc(bc_path)

        print(f"  [{vendor_name}] synthesizing battlecard...", file=sys.stderr)
        try:
            raw_output = synthesize_battlecard(
                vendor=vendor,
                scraped=scraped,
                self_scraped=self_scraped,
                prompts=prompts,
                model=args.model,
                existing_doc=existing_doc,
            )
        except Exception as e:
            print(f"  [{vendor_name}] synthesis error: {e}", file=sys.stderr)
            change_summaries[vendor_name] = f"Synthesis failed: {e}"
            continue

        changes = extract_changes(raw_output)
        change_summaries[vendor_name] = changes

        battlecard_content = strip_changes_section(raw_output)
        frontmatter = format_frontmatter(vendor, doc_type="battlecard")
        final_content = frontmatter + battlecard_content

        with open(bc_path, "w") as f:
            f.write(final_content)

        written_battlecards.append(bc_path)
        print(f"  [{vendor_name}] battlecard written: {bc_path}", file=sys.stderr)

    # 7. Synthesize landscape summary
    lp = landscape_path()
    existing_landscape = read_existing_doc(lp)

    print("\n[landscape] Synthesizing landscape summary...", file=sys.stderr)
    try:
        landscape_output = synthesize_landscape(
            change_summaries=change_summaries,
            prompts=prompts,
            model=args.model,
            existing_doc=existing_landscape,
        )
    except Exception as e:
        print(f"[landscape] landscape synthesis error: {e}", file=sys.stderr)
        landscape_output = f"# Landscape {datetime.now().strftime('%Y-%m')}\n\nSynthesis failed: {e}"

    # 8. Write landscape file
    landscape_frontmatter = format_frontmatter(self_vendor, doc_type="landscape")
    with open(lp, "w") as f:
        f.write(landscape_frontmatter + landscape_output)
    print(f"\n[landscape] landscape written: {lp}", file=sys.stderr)

    # 9. Print summary to stderr, file paths to stdout
    print(
        f"\n[landscape] Done. {len(written_battlecards)}/{len(vendors)} battlecards updated.",
        file=sys.stderr,
    )
    for path in written_battlecards:
        print(path)
    print(lp)


def run_quick_mode(args):
    """Quick call-prep brief for a single vendor."""
    # 1. Resolve vendor
    vendor = resolve_vendor(args.vendor)
    self_vendor = VENDORS["self"]

    # 2. Load prompts
    prompts = load_prompts()

    print(
        f"[quick] Preparing call brief for {vendor['name']}...",
        file=sys.stderr,
    )

    # 3. Scrape vendor + self in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_vendor = executor.submit(scrape_vendor, vendor)
        future_self = executor.submit(scrape_vendor, self_vendor)
        scraped = future_vendor.result()
        self_scraped = future_self.result()

    # 4. Read existing battlecard
    bc_path = battlecard_path(vendor)
    existing_battlecard = read_existing_doc(bc_path)

    # 5. Synthesize quick brief (conversation output)
    print(f"[quick] Synthesizing call-prep brief...", file=sys.stderr)
    quick_brief = synthesize_quick_brief(
        vendor=vendor,
        scraped=scraped,
        self_scraped=self_scraped,
        prompts=prompts,
        model=args.model,
        existing_battlecard=existing_battlecard,
    )

    # 6. Also synthesize updated battlecard as a side effect
    print(f"[quick] Updating battlecard as side effect...", file=sys.stderr)
    try:
        raw_battlecard = synthesize_battlecard(
            vendor=vendor,
            scraped=scraped,
            self_scraped=self_scraped,
            prompts=prompts,
            model=args.model,
            existing_doc=existing_battlecard,
        )

        # 7. Write updated battlecard file
        os.makedirs(OBSIDIAN_BASE, exist_ok=True)
        battlecard_content = strip_changes_section(raw_battlecard)
        frontmatter = format_frontmatter(vendor, doc_type="battlecard")
        final_content = frontmatter + battlecard_content

        with open(bc_path, "w") as f:
            f.write(final_content)

        print(f"[quick] Battlecard updated: {bc_path}", file=sys.stderr)
    except Exception as e:
        print(f"[quick] Battlecard update failed (non-fatal): {e}", file=sys.stderr)

    # 8. Print quick brief to stdout
    print(quick_brief)


def main():
    args = parse_args()
    if args.mode == "quick":
        run_quick_mode(args)
    else:
        run_landscape_mode(args)


if __name__ == "__main__":
    main()
