import re
from typing import Dict, Any

# Category half-lives in days
CATEGORY_HALF_LIVES = {
    "pricing": 7.0,
    "software_version": 30.0,
    "api_version": 30.0,
    "regulation": 90.0,
    "company_info": 90.0,
    "statistics": 90.0,
    "time_sensitive_news": 14.0,
    "technical_docs": 180.0,
    "general_technical": 365.0,
    "general_fact": 730.0,
}

# Regex patterns for deterministic classification
_VERSION_REGEX = re.compile(r"\b(v(ersion)?\s*\d+(\.\d+)+|\d+\.\d+(\.\d+)?|latest\s+(stable\s+)?(version|release))\b", re.IGNORECASE)
_PRICE_REGEX = re.compile(r"(\$|€|£|¥|\bUSD\b|\bEUR\b|\bcost(s)?\b|\bprice(s)?\b|\bpricing\b|\bper\s+(token|month|user|call)\b)", re.IGNORECASE)
_REGULATION_REGEX = re.compile(r"\b(act|law|regulation|compliance|gdpr|sec|irs|directive|mandate|effective\s+date|rule)\b", re.IGNORECASE)
_COMPANY_REGEX = re.compile(r"\b(ceo|cto|founder|acquired|acquisition|valuation|headquarters|board|revenue|subsidiary)\b", re.IGNORECASE)
_API_REGEX = re.compile(r"\b(api|endpoint|sdk|deprecated|rest|graphql|payload|parameters)\b", re.IGNORECASE)
_DATE_REGEX = re.compile(r"\b(19\d\d|20\d\d|january|february|march|april|may|june|july|august|september|october|november|december)\b", re.IGNORECASE)


class ClassificationEngine:
    """
    Classifies atomic claims into verification categories and assigns temporal sensitivity.
    """
    @staticmethod
    def classify_claim(claim_text: str, default_domain: str = "general") -> Dict[str, Any]:
        text_lower = claim_text.lower()
        
        # Check software version
        if _VERSION_REGEX.search(claim_text) and any(kw in text_lower for kw in ["version", "release", "latest", "python", "fastapi", "postgres", "node", "react", "django", "v1", "v2"]):
            return {
                "category": "software_version",
                "temporal_sensitivity": "HIGH",
                "half_life_days": CATEGORY_HALF_LIVES["software_version"]
            }

        # Check API version or documentation
        if _API_REGEX.search(claim_text) and (_VERSION_REGEX.search(claim_text) or "deprecated" in text_lower or "endpoint" in text_lower):
            return {
                "category": "api_version",
                "temporal_sensitivity": "HIGH",
                "half_life_days": CATEGORY_HALF_LIVES["api_version"]
            }

        # Check Pricing
        if _PRICE_REGEX.search(claim_text) and any(c.isdigit() for c in claim_text):
            return {
                "category": "pricing",
                "temporal_sensitivity": "HIGH",
                "half_life_days": CATEGORY_HALF_LIVES["pricing"]
            }

        # Check Regulation
        if _REGULATION_REGEX.search(claim_text):
            return {
                "category": "regulation",
                "temporal_sensitivity": "MEDIUM",
                "half_life_days": CATEGORY_HALF_LIVES["regulation"]
            }

        # Check Company leadership / M&A
        if _COMPANY_REGEX.search(claim_text):
            return {
                "category": "company_info",
                "temporal_sensitivity": "MEDIUM",
                "half_life_days": CATEGORY_HALF_LIVES["company_info"]
            }

        # Check Statistics
        if any(kw in text_lower for kw in ["percent", "%", "million", "billion", "growth rate", "inflation"]):
            return {
                "category": "statistics",
                "temporal_sensitivity": "MEDIUM",
                "half_life_days": CATEGORY_HALF_LIVES["statistics"]
            }

        # Check Tech docs
        if any(kw in text_lower for kw in ["supports", "implements", "protocol", "architecture", "algorithm", "jsonb", "sql"]):
            return {
                "category": "technical_docs",
                "temporal_sensitivity": "LOW",
                "half_life_days": CATEGORY_HALF_LIVES["technical_docs"]
            }

        # Default fallback based on domain
        if default_domain in ["software", "technology"]:
            return {
                "category": "general_technical",
                "temporal_sensitivity": "MEDIUM",
                "half_life_days": CATEGORY_HALF_LIVES["general_technical"]
            }

        return {
            "category": "general_fact",
            "temporal_sensitivity": "LOW",
            "half_life_days": CATEGORY_HALF_LIVES["general_fact"]
        }

