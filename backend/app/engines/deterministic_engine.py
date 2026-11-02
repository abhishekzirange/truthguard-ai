import re
import logging
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple
from packaging import version as pkg_version

logger = logging.getLogger("truthguard.deterministic")

_VERSION_EXTRACTION_REGEX = re.compile(r"\b(?:v|version\s*)?(\d+(?:\.\d+)*([a-zA-Z0-9_\-\.]+)?)\b", re.IGNORECASE)
_PRICE_EXTRACTION_REGEX = re.compile(r"\$(\d+(\.\d+)?)|(\d+(\.\d+)?)\s*(USD|dollars|cents)", re.IGNORECASE)

# Intent classification regexes
_LATEST_INTENT_REGEX = re.compile(
    r"\b(latest|newest|current|currently|most\s+recent|active\s+(lts\s+)?(release|version)?|active\s+lts|lts\s+release|modern\s+version|primary\s+(recommended\s+)?(release|version)?|recommended\s+(release|version)?|standard\s+public\s+support|actively\s+supported|up\s+to\s+date|latest\s+stable)\b",
    re.IGNORECASE
)

_HISTORICAL_INTENT_REGEX = re.compile(
    r"\b(deprecated|deprecated\s+in|removed\s+in|introduced\s+in|first\s+released|originally|was\s+released|released\s+in\s+20\d\d|added\s+in|became|retired\s+in)\b",
    re.IGNORECASE
)

_COMPATIBILITY_INTENT_REGEX = re.compile(
    r"\b(supports|supported|compatible\s+with|compatibility|requires|works\s+with|runs\s+on)\b",
    re.IGNORECASE
)


class VersionIntent(str, Enum):
    LATEST_ASSERTION = "LATEST_ASSERTION"
    HISTORICAL_MILESTONE = "HISTORICAL_MILESTONE"
    COMPATIBILITY_ASSERTION = "COMPATIBILITY_ASSERTION"
    AMBIGUOUS = "AMBIGUOUS"


class DeterministicEngine:
    """
    Executes deterministic checks: semantic version comparison, numeric price verification,
    and structured date logic with rigorous linguistic intent detection.
    """

    @staticmethod
    def detect_version_intent(claim_text: str) -> VersionIntent:
        """
        Determines whether a claim asserts that a version is the latest/current release,
        describes a historical milestone/deprecation, or asserts feature compatibility.
        """
        if not claim_text:
            return VersionIntent.AMBIGUOUS

        text = claim_text.strip()

        # Check explicit latest assertion
        if _LATEST_INTENT_REGEX.search(text):
            return VersionIntent.LATEST_ASSERTION

        # Check historical / deprecation / past milestone
        if _HISTORICAL_INTENT_REGEX.search(text):
            return VersionIntent.HISTORICAL_MILESTONE

        # Check compatibility / feature support
        if _COMPATIBILITY_INTENT_REGEX.search(text):
            return VersionIntent.COMPATIBILITY_ASSERTION

        return VersionIntent.AMBIGUOUS

    @classmethod
    def compare_software_versions(
        cls,
        claimed_version_str: str,
        retrieved_texts: List[str],
        claim_text: str = "",
        claim_asserts_latest: Optional[bool] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Parses versions using packaging.version.Version and evaluates whether the claim is valid
        based on the detected linguistic intent.
        """
        if not claimed_version_str:
            return None

        try:
            clean_claimed = claimed_version_str.lstrip("v").strip()
            v_claim = pkg_version.parse(clean_claimed)
        except Exception:
            return None

        # Determine intent if not explicitly passed
        if claim_asserts_latest is not None:
            intent = VersionIntent.LATEST_ASSERTION if claim_asserts_latest else VersionIntent.HISTORICAL_MILESTONE
        else:
            intent = cls.detect_version_intent(claim_text)

        # Collect candidate release versions from authoritative texts
        highest_found: Optional[pkg_version.Version] = None
        highest_found_str: Optional[str] = None
        mentioned_in_evidence = False

        for text in retrieved_texts:
            if clean_claimed in text:
                mentioned_in_evidence = True

            matches = _VERSION_EXTRACTION_REGEX.finditer(text)
            for match in matches:
                candidate_str = match.group(1).lstrip("v").strip()
                try:
                    candidate = pkg_version.parse(candidate_str)
                    if candidate.base_version and not candidate.is_prerelease:
                        # Filter out calendar years (e.g., 2024, 2023) unless genuine CalVer (like 24.04)
                        if 1900 <= candidate.major <= 2100 and getattr(candidate, "minor", 0) == 0:
                            continue
                        if highest_found is None or candidate > highest_found:
                            highest_found = candidate
                            highest_found_str = candidate_str
                except Exception:
                    continue

        # Case 1: Claim explicitly asserts that the version is latest / current
        if intent == VersionIntent.LATEST_ASSERTION:
            if not highest_found:
                return {
                    "verdict": "UNVERIFIED",
                    "reasoning": f"No authoritative release versions found to verify if {claimed_version_str} is the latest.",
                    "claimed_version": claimed_version_str,
                    "latest_version": None,
                    "is_outdated": False,
                    "intent": intent.value
                }

            # If claimed version is in the same major.minor release line (e.g. 3.13 vs 3.13.2)
            is_same_minor_line = (
                v_claim.major == highest_found.major and
                hasattr(v_claim, "minor") and hasattr(highest_found, "minor") and
                v_claim.minor == highest_found.minor
            )

            if is_same_minor_line or v_claim == highest_found:
                return {
                    "verdict": "CURRENT",
                    "reasoning": f"Claimed version {claimed_version_str} belongs to the current official release line ({highest_found_str}).",
                    "claimed_version": claimed_version_str,
                    "latest_version": highest_found_str,
                    "is_outdated": False,
                    "intent": intent.value
                }
            elif v_claim < highest_found:
                return {
                    "verdict": "OUTDATED",
                    "reasoning": f"Claimed version {claimed_version_str} is superseded by official release {highest_found_str}.",
                    "claimed_version": claimed_version_str,
                    "latest_version": highest_found_str,
                    "is_outdated": True,
                    "intent": intent.value
                }
            else:
                return {
                    "verdict": "UNVERIFIED",
                    "reasoning": f"Claimed version {claimed_version_str} exceeds highest known release {highest_found_str}.",
                    "claimed_version": claimed_version_str,
                    "latest_version": highest_found_str,
                    "is_outdated": False,
                    "intent": intent.value
                }

        # Case 2: Historical milestone / deprecation statement (e.g. "Kubernetes 1.20 deprecated dockershim")
        elif intent == VersionIntent.HISTORICAL_MILESTONE:
            # Check if evidence mentions the deprecation/milestone and the claimed version
            combined_evidence = " ".join(retrieved_texts).lower()
            claim_keywords = [
                kw for kw in re.findall(r"\b[a-zA-Z]{4,}\b", claim_text.lower())
                if kw not in ["which", "their", "about", "after", "before", "version"]
            ]
            matches_count = sum(1 for kw in claim_keywords if kw in combined_evidence)

            if mentioned_in_evidence and matches_count >= min(2, len(claim_keywords)):
                return {
                    "verdict": "CURRENT",
                    "reasoning": f"Historical milestone for version {claimed_version_str} is corroborated by documentation.",
                    "claimed_version": claimed_version_str,
                    "latest_version": highest_found_str,
                    "is_outdated": False,
                    "intent": intent.value
                }
            elif not mentioned_in_evidence:
                return {
                    "verdict": "UNVERIFIED",
                    "reasoning": f"Evidence does not contain records verifying the milestone for version {claimed_version_str}.",
                    "claimed_version": claimed_version_str,
                    "latest_version": highest_found_str,
                    "is_outdated": False,
                    "intent": intent.value
                }

        # Case 3: Compatibility assertion (e.g. "supports Python 3.11")
        elif intent == VersionIntent.COMPATIBILITY_ASSERTION:
            combined_evidence = " ".join(retrieved_texts).lower()
            if mentioned_in_evidence and any(kw in combined_evidence for kw in ["support", "compatible", "requires"]):
                return {
                    "verdict": "CURRENT",
                    "reasoning": f"Compatibility with version {claimed_version_str} is confirmed by documentation.",
                    "claimed_version": claimed_version_str,
                    "latest_version": highest_found_str,
                    "is_outdated": False,
                    "intent": intent.value
                }
            return {
                "verdict": "UNVERIFIED",
                "reasoning": f"Documentation is inconclusive regarding compatibility with version {claimed_version_str}.",
                "claimed_version": claimed_version_str,
                "latest_version": highest_found_str,
                "is_outdated": False,
                "intent": intent.value
            }

        # Case 4: Ambiguous intent
        return {
            "verdict": "UNVERIFIED",
            "reasoning": f"Intent for version mention '{claimed_version_str}' is ambiguous; neither latest status nor past milestone was asserted.",
            "claimed_version": claimed_version_str,
            "latest_version": highest_found_str,
            "is_outdated": False,
            "intent": intent.value
        }

    @staticmethod
    def compare_prices(
        claimed_text: str,
        retrieved_snippets: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Compares numeric price mentions with historical filtering and tolerance boundaries.
        """
        claim_match = _PRICE_EXTRACTION_REGEX.search(claimed_text)
        if not claim_match:
            return None

        claim_price = float(claim_match.group(1) or claim_match.group(3))

        retrieved_prices = []
        for snip in retrieved_snippets:
            # Strip out legacy price statements like "Legacy GPT-4 pricing was $30"
            clean_snip = re.sub(
                r"\b(legacy|was|previously|former|historical|old)\b[^.]*?\$(\d+(\.\d+)?)",
                "",
                snip,
                flags=re.IGNORECASE
            )
            matches = _PRICE_EXTRACTION_REGEX.findall(clean_snip)
            for m in matches:
                try:
                    val = float(m[0] or m[2])
                    retrieved_prices.append(val)
                except Exception:
                    continue

        if retrieved_prices:
            # If claim price matches any of the official prices listed
            if any(abs(claim_price - p) < 0.05 for p in retrieved_prices):
                return {
                    "verdict": "CURRENT",
                    "reasoning": f"Claimed price (${claim_price}) matches authoritative pricing documentation.",
                    "claimed_price": claim_price,
                    "current_price": claim_price,
                }

            # If completely different from all listed prices
            return {
                "verdict": "CONTRADICTED",
                "reasoning": f"Claimed price (${claim_price}) conflicts with published pricing (${retrieved_prices[0]}).",
                "claimed_price": claim_price,
                "current_price": retrieved_prices[0],
            }

        return None
