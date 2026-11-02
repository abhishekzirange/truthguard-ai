from typing import Dict, Any, Optional
from urllib.parse import urlparse

# Trusted domain score map
KNOWN_DOMAIN_RELIABILITY: Dict[str, tuple[str, float]] = {
    # Primary documentation & registries (1.0)
    "python.org": ("primary", 1.0),
    "docs.python.org": ("primary", 1.0),
    "pypi.org": ("primary", 1.0),
    "fastapi.tiangolo.com": ("primary", 1.0),
    "postgresql.org": ("primary", 1.0),
    "docs.postgresql.org": ("primary", 1.0),
    "react.dev": ("primary", 1.0),
    "nodejs.org": ("primary", 1.0),
    "openai.com": ("primary", 0.98),
    "platform.openai.com": ("primary", 1.0),
    "aws.amazon.com": ("primary", 0.98),
    "github.com": ("primary", 0.95),

    # Government and official bodies (1.0)
    "sec.gov": ("primary", 1.0),
    "irs.gov": ("primary", 1.0),
    "gov.uk": ("primary", 1.0),
    "europa.eu": ("primary", 1.0),

    # Authoritative news publishers (0.85 - 0.90)
    "reuters.com": ("authoritative", 0.90),
    "bloomberg.com": ("authoritative", 0.90),
    "techcrunch.com": ("authoritative", 0.85),
    "theverge.com": ("authoritative", 0.82),
    "arstechnica.com": ("authoritative", 0.85),

    # Community forums & aggregators (0.50 - 0.65)
    "stackoverflow.com": ("community", 0.65),
    "github.community": ("community", 0.60),
    "reddit.com": ("community", 0.40),

    # General blogging / unverified (0.30 - 0.50)
    "medium.com": ("blog", 0.45),
    "dev.to": ("blog", 0.50),
    "substack.com": ("blog", 0.50),
}


class ReliabilityEngine:
    """
    Evaluates source reliability score S in [0.0, 1.0] and categorizes source type.
    """
    @staticmethod
    def evaluate_source(url: str, title: str = "") -> tuple[str, float]:
        if not url:
            return "unverified", 0.2

        try:
            domain = urlparse(url).netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
        except Exception:
            return "unverified", 0.2

        # Check known domains
        if domain in KNOWN_DOMAIN_RELIABILITY:
            return KNOWN_DOMAIN_RELIABILITY[domain]

        # Check TLD heuristics
        if domain.endswith(".gov") or domain.endswith(".edu"):
            return "primary", 0.95

        # Check title indicators for official documentation
        title_lower = title.lower()
        if "official documentation" in title_lower or "release notes" in title_lower:
            return "authoritative", 0.85

        # General web secondary
        return "secondary", 0.50
