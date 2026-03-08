#!/usr/bin/env python3
"""Account research orchestrator — scrapes company intelligence and synthesizes with Gemini.

Usage:
    python3 research_account.py "Salesforce"
    python3 research_account.py "HubSpot" --angle "expansion opportunity"
    python3 research_account.py "Snowflake" --depth deep
    python3 research_account.py "Databricks" --depth full --angle "competitive displacement"
    python3 research_account.py "Stripe" --output /custom/path.md
    python3 research_account.py "Figma" --depth quick --angle "new logo"

Depth levels:
    quick  — fast signals: website, news, crunchbase, jobs, tech stack
    deep   — + reviews, SEC filings, glassdoor
    full   — + industry news, competitor references

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
PROMPT_FILE = SKILL_DIR / "references" / "account-research-prompt.md"
OBSIDIAN_BASE = Path.home() / "Documents" / "ObsidianNotes" / "Claude-Research" / "accounts"
DEFAULT_MODEL = "gemini-3.1-pro-preview"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
}

# Depth controls which source keys are run.
# Tasks 4-6 will populate SCRAPER_REGISTRY with functions keyed by these names.
DEPTH_SOURCES = {
    "quick": ["website", "google_news", "crunchbase", "job_postings", "builtwith"],
    "deep": [
        "website", "google_news", "crunchbase", "job_postings", "builtwith",
        "g2_trustradius", "sec_edgar", "glassdoor",
    ],
    "full": [
        "website", "google_news", "crunchbase", "job_postings", "builtwith",
        "g2_trustradius", "sec_edgar", "glassdoor",
        "industry_news", "competitor_refs",
    ],
}

# ---------------------------------------------------------------------------
# Company resolution
# ---------------------------------------------------------------------------

def resolve_company(query: str) -> dict:
    """Resolve a company name/domain query to a structured company dict.

    Returns a dict with keys: name, domain, query.
    Tries a HEAD request against {slug}.com first, then falls back to a
    Google search to discover the real domain.
    """
    # Build a slug from the query for the optimistic domain guess
    slug = re.sub(r"[^a-z0-9]", "", query.lower())
    guessed_domain = f"{slug}.com"

    # Try the guessed domain with a HEAD request
    try:
        resp = requests.head(
            f"https://{guessed_domain}",
            headers=HEADERS,
            timeout=8,
            allow_redirects=True,
        )
        if resp.status_code < 400:
            final_url = resp.url
            # Extract the bare domain from the final URL after redirects
            domain_match = re.search(r"https?://(?:www\.)?([^/]+)", final_url)
            domain = domain_match.group(1) if domain_match else guessed_domain
            print(f"Resolved domain: {domain} (direct HEAD)", file=sys.stderr)
            return {"name": query, "domain": domain, "query": query}
    except Exception:
        pass  # Fall through to Google search

    # Fallback: use Google search to find the company's domain
    try:
        search_url = (
            f"https://www.google.com/search?q={requests.utils.quote(query + ' official site')}"
            f"&num=3&hl=en"
        )
        resp = requests.get(search_url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # Look for cite tags or result URLs that match company domain patterns
            for cite in soup.find_all("cite"):
                text = cite.get_text(strip=True)
                # Extract domain from result
                domain_match = re.search(r"(?:https?://)?(?:www\.)?([a-z0-9-]+\.[a-z]{2,})", text)
                if domain_match:
                    candidate = domain_match.group(1).lower()
                    # Skip generic sites
                    skip = {"google.com", "wikipedia.org", "linkedin.com", "twitter.com",
                            "facebook.com", "youtube.com", "glassdoor.com", "indeed.com"}
                    if candidate not in skip:
                        print(f"Resolved domain: {candidate} (Google search)", file=sys.stderr)
                        return {"name": query, "domain": candidate, "query": query}
    except Exception as e:
        print(f"Warning: Google domain resolution failed: {e}", file=sys.stderr)

    # Last resort: use the guessed slug domain even if HEAD check failed
    print(f"Warning: Could not confirm domain, using guess: {guessed_domain}", file=sys.stderr)
    return {"name": query, "domain": guessed_domain, "query": query}


# ---------------------------------------------------------------------------
# Scraper functions — Tasks 4, 5, 6
# ---------------------------------------------------------------------------

def scrape_website(company: dict) -> tuple:
    """Scrape company about and careers pages.

    Returns ("Company Website", text) or ("Company Website", None) on failure.
    """
    domain = company.get("domain", "")
    base = f"https://{domain}"

    about_paths = ["/about", "/about-us", "/company", "/"]
    careers_paths = ["/careers", "/jobs", "/about/careers"]

    about_text = ""
    careers_text = ""

    def _fetch_text(url: str, max_chars: int) -> str:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=9, allow_redirects=True)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for tag in soup(["nav", "footer", "script", "style", "header"]):
                    tag.decompose()
                return soup.get_text(separator=" ", strip=True)[:max_chars]
        except Exception:
            pass
        return ""

    for path in about_paths:
        text = _fetch_text(base + path, 3000)
        if len(text) > 200:
            about_text = text
            break

    for path in careers_paths:
        text = _fetch_text(base + path, 2000)
        if len(text) > 200:
            careers_text = text
            break

    combined = ""
    if about_text:
        combined += f"[About]\n{about_text}\n\n"
    if careers_text:
        combined += f"[Careers]\n{careers_text}\n\n"

    if not combined:
        print(f"scrape_website: no content found for {domain}", file=sys.stderr)
        return ("Company Website", None)

    return ("Company Website", combined.strip())


def scrape_google_news(company: dict) -> tuple:
    """Scrape recent news from Google News RSS.

    Returns ("Google News", text) or ("Google News", None) on failure.
    """
    name = company.get("name", "")
    query = requests.utils.quote(f"{name} company")
    url = (
        f"https://news.google.com/rss/search?q={query}"
        f"&hl=en-US&gl=US&ceid=US:en"
    )
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"scrape_google_news: HTTP {resp.status_code}", file=sys.stderr)
            return ("Google News", None)

        soup = BeautifulSoup(resp.text, "xml")
        items = soup.find_all("item")[:10]
        if not items:
            return ("Google News", None)

        lines = []
        for item in items:
            title = item.find("title")
            source = item.find("source")
            pub_date = item.find("pubDate")
            title_text = title.get_text(strip=True) if title else "(no title)"
            source_text = source.get_text(strip=True) if source else ""
            date_text = pub_date.get_text(strip=True) if pub_date else ""
            lines.append(f"- {title_text} [{source_text}] ({date_text})")

        return ("Google News", "\n".join(lines))
    except Exception as e:
        print(f"scrape_google_news: {e}", file=sys.stderr)
        return ("Google News", None)


def scrape_crunchbase(company: dict) -> tuple:
    """Search Google for Crunchbase/funding signals.

    Returns ("Crunchbase / Funding", text) or ("Crunchbase / Funding", None) on failure.
    """
    name = company.get("name", "")
    query = requests.utils.quote(
        f"{name} crunchbase funding revenue employees"
    )
    url = f"https://www.google.com/search?q={query}&num=10&hl=en"

    funding_keywords = {
        "funding", "revenue", "employees", "founded", "series",
        "valuation", "raised", "investors", "headcount", "ipo",
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"scrape_crunchbase: HTTP {resp.status_code}", file=sys.stderr)
            return ("Crunchbase / Funding", None)

        soup = BeautifulSoup(resp.text, "html.parser")
        snippets = []
        for el in soup.find_all(["span", "div", "p"]):
            text = el.get_text(separator=" ", strip=True)
            if len(text) < 40 or len(text) > 600:
                continue
            lower = text.lower()
            if any(kw in lower for kw in funding_keywords):
                snippets.append(text)
            if len(snippets) >= 8:
                break

        if not snippets:
            return ("Crunchbase / Funding", None)

        return ("Crunchbase / Funding", "\n\n".join(snippets))
    except Exception as e:
        print(f"scrape_crunchbase: {e}", file=sys.stderr)
        return ("Crunchbase / Funding", None)


def scrape_job_postings(company: dict) -> tuple:
    """Search Google for job postings with identity/tech keywords.

    Returns ("Job Postings", text) or ("Job Postings", None) on failure.
    """
    name = company.get("name", "")
    query = requests.utils.quote(
        f"{name} jobs site:indeed.com OR site:linkedin.com/jobs"
    )
    url = f"https://www.google.com/search?q={query}&num=10&hl=en"

    identity_keywords = {
        "okta", "azure ad", "entra", "ping", "forgerock", "saml", "oidc",
        "sso", "mfa", "scim", "ldap", "aws", "azure", "gcp", "kubernetes",
        "terraform", "python", "java", "react", "soc 2", "iso 27001",
        "fedramp", "hipaa", "gdpr", "security engineer", "identity", "iam",
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"scrape_job_postings: HTTP {resp.status_code}", file=sys.stderr)
            return ("Job Postings", None)

        soup = BeautifulSoup(resp.text, "html.parser")
        snippets = []
        for el in soup.find_all(["span", "div", "p", "h3"]):
            text = el.get_text(separator=" ", strip=True)
            if len(text) < 30 or len(text) > 600:
                continue
            lower = text.lower()
            if any(kw in lower for kw in identity_keywords):
                snippets.append(text)
            if len(snippets) >= 10:
                break

        if not snippets:
            return ("Job Postings", None)

        return ("Job Postings", "\n\n".join(snippets))
    except Exception as e:
        print(f"scrape_job_postings: {e}", file=sys.stderr)
        return ("Job Postings", None)


def scrape_builtwith(company: dict) -> tuple:
    """Fetch HTTP headers via HackerTarget and Google-search BuiltWith data.

    Returns ("Tech Stack Detection", text) or ("Tech Stack Detection", None) on failure.
    """
    domain = company.get("domain", "")
    parts = []

    # HackerTarget HTTP headers
    try:
        ht_url = f"https://api.hackertarget.com/httpheaders/?q={domain}"
        resp = requests.get(ht_url, headers=HEADERS, timeout=9)
        if resp.status_code == 200 and resp.text.strip():
            parts.append(f"[HTTP Headers via HackerTarget]\n{resp.text.strip()[:1500]}")
    except Exception as e:
        print(f"scrape_builtwith (hackertarget): {e}", file=sys.stderr)

    # Google search for BuiltWith data
    try:
        query = requests.utils.quote(f"site:builtwith.com {domain}")
        bw_url = f"https://www.google.com/search?q={query}&num=5&hl=en"
        resp = requests.get(bw_url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            snippets = []
            for el in soup.find_all(["span", "div"]):
                text = el.get_text(separator=" ", strip=True)
                if 40 < len(text) < 500:
                    snippets.append(text)
                if len(snippets) >= 5:
                    break
            if snippets:
                parts.append(f"[BuiltWith Google Snippets]\n" + "\n".join(snippets))
    except Exception as e:
        print(f"scrape_builtwith (google): {e}", file=sys.stderr)

    if not parts:
        return ("Tech Stack Detection", None)

    return ("Tech Stack Detection", "\n\n".join(parts))


def scrape_g2_trustradius(company: dict) -> tuple:
    """Search Google for G2 / TrustRadius reviews related to identity/SSO.

    Returns ("G2 / TrustRadius", text) or ("G2 / TrustRadius", None) on failure.
    """
    name = company.get("name", "")
    query = requests.utils.quote(
        f"{name} site:g2.com OR site:trustradius.com identity security SSO"
    )
    url = f"https://www.google.com/search?q={query}&num=10&hl=en"

    review_keywords = {
        "review", "rating", "identity", "sso", "authentication", "security",
        "star", "users", "reviews", "okta", "azure", "saml", "mfa",
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"scrape_g2_trustradius: HTTP {resp.status_code}", file=sys.stderr)
            return ("G2 / TrustRadius", None)

        soup = BeautifulSoup(resp.text, "html.parser")
        snippets = []
        for el in soup.find_all(["span", "div", "p", "h3"]):
            text = el.get_text(separator=" ", strip=True)
            if len(text) < 40 or len(text) > 600:
                continue
            lower = text.lower()
            if any(kw in lower for kw in review_keywords):
                snippets.append(text)
            if len(snippets) >= 8:
                break

        if not snippets:
            return ("G2 / TrustRadius", None)

        return ("G2 / TrustRadius", "\n\n".join(snippets))
    except Exception as e:
        print(f"scrape_g2_trustradius: {e}", file=sys.stderr)
        return ("G2 / TrustRadius", None)


def scrape_sec_edgar(company: dict) -> tuple:
    """Search SEC EDGAR full-text search for 10-K filings.

    Returns ("SEC EDGAR", text) or ("SEC EDGAR", None) on failure.
    """
    name = company.get("name", "")
    # SEC requires an identifying User-Agent
    sec_headers = {
        "User-Agent": "AccountResearch/1.0 research@example.com",
        "Accept": "application/json",
    }
    encoded_name = requests.utils.quote(f'"{name}"')
    url = (
        f"https://efts.sec.gov/LATEST/search-index?q={encoded_name}"
        f"&forms=10-K"
    )

    try:
        resp = requests.get(url, headers=sec_headers, timeout=10)
        if resp.status_code != 200:
            print(f"scrape_sec_edgar: HTTP {resp.status_code}", file=sys.stderr)
            return ("SEC EDGAR", None)

        try:
            data = resp.json()
        except Exception:
            return ("SEC EDGAR", None)

        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            return ("SEC EDGAR", None)

        lines = []
        for hit in hits[:5]:
            source = hit.get("_source", {})
            entity = source.get("entity_name", "")
            form = source.get("form_type", "")
            filed = source.get("file_date", "")
            period = source.get("period_of_report", "")
            lines.append(
                f"- {entity} | Form: {form} | Filed: {filed} | Period: {period}"
            )

        return ("SEC EDGAR", "\n".join(lines))
    except Exception as e:
        print(f"scrape_sec_edgar: {e}", file=sys.stderr)
        return ("SEC EDGAR", None)


def scrape_glassdoor(company: dict) -> tuple:
    """Search Google for Glassdoor engineering/culture information.

    Returns ("Glassdoor", text) or ("Glassdoor", None) on failure.
    """
    name = company.get("name", "")
    query = requests.utils.quote(
        f"{name} glassdoor engineering technology team"
    )
    url = f"https://www.google.com/search?q={query}&num=10&hl=en"

    culture_keywords = {
        "glassdoor", "engineering", "technology", "culture", "team",
        "tech stack", "work", "employees", "reviews", "interview",
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"scrape_glassdoor: HTTP {resp.status_code}", file=sys.stderr)
            return ("Glassdoor", None)

        soup = BeautifulSoup(resp.text, "html.parser")
        snippets = []
        for el in soup.find_all(["span", "div", "p", "h3"]):
            text = el.get_text(separator=" ", strip=True)
            if len(text) < 40 or len(text) > 600:
                continue
            lower = text.lower()
            if any(kw in lower for kw in culture_keywords):
                snippets.append(text)
            if len(snippets) >= 8:
                break

        if not snippets:
            return ("Glassdoor", None)

        return ("Glassdoor", "\n\n".join(snippets))
    except Exception as e:
        print(f"scrape_glassdoor: {e}", file=sys.stderr)
        return ("Glassdoor", None)


def scrape_industry_news(company: dict) -> tuple:
    """Search Google News tab for compliance/regulation/security/breach news.

    Returns ("Industry News", text) or ("Industry News", None) on failure.
    """
    name = company.get("name", "")
    query = requests.utils.quote(
        f"{name} regulation compliance identity security breach data privacy 2025 2026"
    )
    url = f"https://www.google.com/search?q={query}&tbm=nws&num=10&hl=en"

    news_keywords = {
        "compliance", "regulation", "breach", "security", "privacy", "identity",
        "audit", "gdpr", "hipaa", "fedramp", "soc 2", "cyber", "vulnerability",
        "data", "hack", "incident",
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"scrape_industry_news: HTTP {resp.status_code}", file=sys.stderr)
            return ("Industry News", None)

        soup = BeautifulSoup(resp.text, "html.parser")
        snippets = []
        for el in soup.find_all(["span", "div", "p", "h3"]):
            text = el.get_text(separator=" ", strip=True)
            if len(text) < 40 or len(text) > 600:
                continue
            lower = text.lower()
            if any(kw in lower for kw in news_keywords):
                snippets.append(text)
            if len(snippets) >= 10:
                break

        if not snippets:
            return ("Industry News", None)

        return ("Industry News", "\n\n".join(snippets))
    except Exception as e:
        print(f"scrape_industry_news: {e}", file=sys.stderr)
        return ("Industry News", None)


def scrape_competitor_refs(company: dict) -> tuple:
    """Search Google for references to identity vendors alongside the company.

    Returns ("Competitor References", text) or ("Competitor References", None) on failure.
    """
    name = company.get("name", "")
    query = requests.utils.quote(
        f'"{name}" ("Okta" OR "Azure AD" OR "Entra ID" OR "Ping Identity" OR "ForgeRock") '
        f"case study OR partnership OR deployment"
    )
    url = f"https://www.google.com/search?q={query}&num=10&hl=en"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"scrape_competitor_refs: HTTP {resp.status_code}", file=sys.stderr)
            return ("Competitor References", None)

        soup = BeautifulSoup(resp.text, "html.parser")
        vendor_keywords = {
            "okta", "azure ad", "entra id", "ping identity", "forgerock",
            "case study", "partnership", "deployment", "integration",
        }
        snippets = []
        for el in soup.find_all(["span", "div", "p", "h3"]):
            text = el.get_text(separator=" ", strip=True)
            if len(text) < 40 or len(text) > 600:
                continue
            lower = text.lower()
            if any(kw in lower for kw in vendor_keywords):
                snippets.append(text)
            if len(snippets) >= 10:
                break

        if not snippets:
            return ("Competitor References", None)

        return ("Competitor References", "\n\n".join(snippets))
    except Exception as e:
        print(f"scrape_competitor_refs: {e}", file=sys.stderr)
        return ("Competitor References", None)


# ---------------------------------------------------------------------------
# Scraper registry — populated by Tasks 4-6
#
# Each entry maps a source key (matching DEPTH_SOURCES lists) to a function
# with the signature:
#     scraper_fn(company: dict) -> tuple[str, Optional[str]]
# where the tuple is (source_display_name, scraped_text_or_None).
# ---------------------------------------------------------------------------

SCRAPER_REGISTRY: dict = {
    "website": scrape_website,
    "google_news": scrape_google_news,
    "crunchbase": scrape_crunchbase,
    "job_postings": scrape_job_postings,
    "builtwith": scrape_builtwith,
    "g2_trustradius": scrape_g2_trustradius,
    "sec_edgar": scrape_sec_edgar,
    "glassdoor": scrape_glassdoor,
    "industry_news": scrape_industry_news,
    "competitor_refs": scrape_competitor_refs,
}


# ---------------------------------------------------------------------------
# Gemini synthesis
# ---------------------------------------------------------------------------

def load_system_prompt() -> str:
    """Load the system prompt from references/account-research-prompt.md."""
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text()
    # Fallback minimal prompt
    return (
        "You are an expert B2B sales researcher. Given scraped intelligence about a "
        "target account, produce a comprehensive account research brief in markdown format. "
        "Focus on business goals, strategic priorities, pain points, and actionable "
        "insights for a sales or partnership conversation."
    )


def synthesize_with_gemini(
    company: dict,
    scraped_data: dict,
    angle: str,
    depth: str,
    model: str = DEFAULT_MODEL,
    existing_brief: Optional[str] = None,
) -> str:
    """Send scraped data to Gemini for synthesis into an account research brief.

    Args:
        company: Dict with name, domain, query keys from resolve_company().
        scraped_data: Dict mapping source display names to scraped text (or None).
        angle: Research context / angle string (e.g. "expansion opportunity").
        depth: One of quick/deep/full — passed to the prompt for context.
        model: LiteLLM model identifier.
        existing_brief: Optional existing brief content to evolve (update in place).

    Returns:
        Synthesized markdown report string.
    """
    from openai import OpenAI

    api_key = os.environ.get("LITELLM_API_KEY")
    base_url = os.environ.get("LITELLM_BASE_URL")
    if not api_key or not base_url:
        print(
            "Error: LITELLM_API_KEY and LITELLM_BASE_URL required.\n"
            "Configure in ~/.claude-litellm.env",
            file=sys.stderr,
        )
        sys.exit(1)

    base_url = base_url.rstrip("/")
    if not base_url.endswith("/v1"):
        base_url += "/v1"

    client = OpenAI(api_key=api_key, base_url=base_url)
    system_prompt = load_system_prompt()

    # Build context sections from scraped sources
    context_parts = []
    failed_sources = []
    for source_name, data in scraped_data.items():
        if data:
            context_parts.append(f"### {source_name}\n\n{data}")
        else:
            failed_sources.append(source_name)

    context = "\n\n---\n\n".join(context_parts)

    # Build the user message
    company_name = company.get("name", "Unknown Company")
    company_domain = company.get("domain", "")

    task_lines = [
        f"Produce a comprehensive account research brief for **{company_name}**",
        f"(domain: {company_domain}, research depth: {depth}).",
    ]
    if angle:
        task_lines.append(f"\nResearch angle / context: {angle}")
    if failed_sources:
        task_lines.append(
            f"\nNote: The following sources were unavailable: {', '.join(failed_sources)}. "
            "Work with available data and note any gaps."
        )

    task = " ".join(task_lines)

    user_msg_parts = [f"## Scraped Account Intelligence\n\n{context}", f"## Task\n\n{task}"]

    # If an existing brief was found, include it so Gemini can evolve it
    if existing_brief:
        user_msg_parts.insert(
            1,
            (
                "## Existing Brief (update/expand this — do not regress information)\n\n"
                + existing_brief
            ),
        )

    user_msg = "\n\n---\n\n".join(user_msg_parts)

    print(f"Synthesizing with {model}...", file=sys.stderr)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=16000,
            temperature=0.3,
        )
    except Exception as e:
        err_str = str(e).lower()
        if "auth" in err_str or "unauthorized" in err_str or "api key" in err_str:
            print(
                f"Authentication error: {e}\n"
                "Check LITELLM_API_KEY in ~/.claude-litellm.env",
                file=sys.stderr,
            )
        elif "rate" in err_str or "quota" in err_str or "limit" in err_str:
            print(f"Rate limit / quota error: {e}", file=sys.stderr)
        else:
            print(f"Gemini API error: {e}", file=sys.stderr)
        sys.exit(1)

    result = response.choices[0].message.content or ""

    if not result.strip():
        print("Error: Gemini returned an empty response.", file=sys.stderr)
        sys.exit(1)

    # Log token usage
    usage = getattr(response, "usage", None)
    if usage:
        print(
            f"Tokens — prompt: {usage.prompt_tokens:,}, "
            f"completion: {usage.completion_tokens:,}, "
            f"total: {usage.total_tokens:,}",
            file=sys.stderr,
        )

    return result


# ---------------------------------------------------------------------------
# Output formatting helpers
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Convert a company name to a URL-safe slug.

    Examples:
        "Salesforce" -> "salesforce"
        "HubSpot CRM" -> "hubspot-crm"
        "Acme, Inc." -> "acme-inc"
    """
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def format_obsidian_output(
    company: dict,
    report: str,
    depth: str,
    angle: str,
) -> str:
    """Wrap the Gemini report with Obsidian YAML frontmatter and wiki-links.

    Args:
        company: Dict with name, domain, query keys.
        report: Raw markdown report from Gemini.
        depth: Research depth (quick/deep/full).
        angle: Research angle string (may be empty).

    Returns:
        Full markdown string with frontmatter prepended.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    company_name = company.get("name", "Unknown")
    company_slug = slugify(company_name)
    company_domain = company.get("domain", "")

    angle_line = f"angle: {angle}\n" if angle else ""

    frontmatter = (
        f"---\n"
        f"date: {today}\n"
        f"tags:\n"
        f"  - account-research\n"
        f"  - {company_slug}\n"
        f"source: claude-code\n"
        f"project: se-accounts\n"
        f"company: {company_name}\n"
        f"domain: {company_domain}\n"
        f"depth: {depth}\n"
        f"{angle_line}"
        f"---\n\n"
    )

    wiki_links = "> Related: [[account-research-index]] [[se-playbook]]\n\n"

    return frontmatter + wiki_links + report


def output_filename(company: dict) -> Path:
    """Generate the output file path: {slug}-{YYYY-MM}.md in OBSIDIAN_BASE."""
    slug = slugify(company.get("name", "unknown"))
    date_suffix = datetime.now().strftime("%Y-%m")
    return OBSIDIAN_BASE / f"{slug}-{date_suffix}.md"


def find_existing_brief(company: dict) -> Optional[Path]:
    """Check OBSIDIAN_BASE for an existing brief starting with the company slug.

    Returns the Path if found, or None if no existing brief exists.
    """
    slug = slugify(company.get("name", "unknown"))
    if not OBSIDIAN_BASE.exists():
        return None
    for candidate in OBSIDIAN_BASE.iterdir():
        if candidate.is_file() and candidate.name.startswith(slug) and candidate.suffix == ".md":
            return candidate
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Account research — scrapes company intelligence and synthesizes with Gemini."
    )
    parser.add_argument(
        "company",
        help="Company name (e.g. 'Salesforce', 'HubSpot', 'Snowflake')",
    )
    parser.add_argument(
        "--angle", "-a",
        default="",
        help="Research angle / context (e.g. 'expansion opportunity', 'new logo')",
    )
    parser.add_argument(
        "--depth", "-d",
        choices=["quick", "deep", "full"],
        default="deep",
        help="Research depth (default: deep)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Custom output file path (overrides default Obsidian path)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"LLM model to use via LiteLLM (default: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    # --- Resolve company ---
    print(f"Resolving company: {args.company}", file=sys.stderr)
    company = resolve_company(args.company)
    print(f"  Name:   {company['name']}", file=sys.stderr)
    print(f"  Domain: {company['domain']}", file=sys.stderr)

    # --- Select scrapers for requested depth ---
    source_keys = DEPTH_SOURCES[args.depth]
    active_scrapers = []
    for key in source_keys:
        fn = SCRAPER_REGISTRY.get(key)
        if fn is not None:
            active_scrapers.append((key, fn))
        else:
            print(f"  Warning: scraper '{key}' not registered — skipping", file=sys.stderr)

    if not active_scrapers:
        print(
            "Warning: No scrapers are registered yet. "
            "Tasks 4-6 will populate SCRAPER_REGISTRY.",
            file=sys.stderr,
        )

    # --- Check for existing brief (for evolving briefs) ---
    existing_brief_path = find_existing_brief(company)
    existing_brief: Optional[str] = None
    if existing_brief_path:
        print(f"Found existing brief: {existing_brief_path}", file=sys.stderr)
        try:
            existing_brief = existing_brief_path.read_text()
        except Exception as e:
            print(f"Warning: Could not read existing brief: {e}", file=sys.stderr)

    # --- Run scrapers concurrently ---
    print(
        f"Scraping {len(active_scrapers)} sources at depth '{args.depth}'...",
        file=sys.stderr,
    )
    scraped: dict[str, Optional[str]] = {}

    def _run_scraper(item):
        key, fn = item
        print(f"  Scraping {key}...", file=sys.stderr)
        try:
            source_name, data = fn(company)
            return source_name, data
        except Exception as e:
            print(f"  Error in scraper '{key}': {e}", file=sys.stderr)
            return key, None

    if active_scrapers:
        with ThreadPoolExecutor(max_workers=min(len(active_scrapers), 8)) as pool:
            futures = {pool.submit(_run_scraper, s): s[0] for s in active_scrapers}
            for future in as_completed(futures):
                source_name, data = future.result()
                scraped[source_name] = data
                status = "✓" if data else "✗"
                print(f"  {status} {source_name}", file=sys.stderr)

    sources_ok = sum(1 for v in scraped.values() if v)
    sources_total = len(scraped)
    print(
        f"Scraped {sources_ok}/{sources_total} sources ({args.depth} depth)",
        file=sys.stderr,
    )

    if sources_total > 0 and sources_ok == 0:
        print("Error: All scrapers failed. Cannot produce brief.", file=sys.stderr)
        sys.exit(1)

    # --- Synthesize with Gemini ---
    report = synthesize_with_gemini(
        company=company,
        scraped_data=scraped,
        angle=args.angle,
        depth=args.depth,
        model=args.model,
        existing_brief=existing_brief,
    )

    # --- Format output ---
    output = format_obsidian_output(
        company=company,
        report=report,
        depth=args.depth,
        angle=args.angle,
    )

    # --- Write to file ---
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = output_filename(company)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output)

    # Stdout: only the output path (for shell capture / Claude Code to open)
    print(str(out_path))


if __name__ == "__main__":
    main()
