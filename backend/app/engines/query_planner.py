import re
from typing import Dict, Any, List


class QueryPlanner:
    """
    Plans and generates focused search queries based on claim category and entities.
    """
    @staticmethod
    def plan_query(claim: Dict[str, Any]) -> Dict[str, Any]:
        category = claim.get("category", "general_fact")
        subject = claim.get("subject") or ""
        claim_text = claim.get("claim_text", "")
        version = claim.get("mentioned_version")

        # Refine query based on category
        if category in ["software_version", "api_version"]:
            from app.engines.deterministic_engine import DeterministicEngine, VersionIntent
            intent = DeterministicEngine.detect_version_intent(claim_text)
            clean_subject = re.sub(r"\b\d+(\.\d+)+\b", "", subject).strip() if subject else ""
            clean_subject = clean_subject or subject or "software"

            if intent == VersionIntent.LATEST_ASSERTION:
                query = f"{clean_subject} latest stable release version official documentation"
            elif intent == VersionIntent.HISTORICAL_MILESTONE:
                query = f"{clean_subject} {version or ''} {claim_text[:50]} official release notes"
            elif subject and version:
                query = f"{clean_subject} latest release version {version} official"
            elif subject:
                query = f"{clean_subject} latest release version documentation"
            else:
                query = f"{claim_text} official release notes"
            
            # Prefer official documentation domains
            preferred_domains = [
                "python.org", "pypi.org", "github.com",
                "docs.python.org", "fastapi.tiangolo.com",
                "nodejs.org", "react.dev", "postgresql.org"
            ]

        elif category == "pricing":
            query = f"{subject} current pricing cost official rate {claim_text[:40]}"
            preferred_domains = ["openai.com", "aws.amazon.com", "azure.microsoft.com", "google.com"]

        elif category == "regulation":
            query = f"{claim_text} law effective date regulatory update"
            preferred_domains = ["gov", "sec.gov", "irs.gov", "europa.eu"]

        elif category == "company_info":
            query = f"{subject} current leadership announcement news {claim_text[:50]}"
            preferred_domains = ["reuters.com", "bloomberg.com", "sec.gov", "techcrunch.com"]

        else:
            # General query
            query = f"{claim_text}"
            preferred_domains = []

        # Clean query string
        query = re.sub(r'["\']', '', query).strip()

        return {
            "query": query,
            "preferred_domains": preferred_domains,
            "search_depth": "advanced" if claim.get("temporal_sensitivity") == "HIGH" else "basic"
        }

