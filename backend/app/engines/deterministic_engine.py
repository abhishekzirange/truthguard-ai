import re
import logging
from typing import Optional, Dict, Any, List
from packaging import version as pkg_version

logger = logging.getLogger("truthguard.deterministic")

_VERSION_EXTRACTION_REGEX = re.compile(r"\b(\d+\.\d+(\.\d+)?([a-zA-Z0-9_\-\.]+)?)\b")
_PRICE_EXTRACTION_REGEX = re.compile(r"\$(\d+(\.\d+)?)|(\d+(\.\d+)?)\s*(USD|dollars|cents)", re.IGNORECASE)


class DeterministicEngine:
    """
    Executes deterministic checks: semantic version comparison, numeric price verification,
    and structured date logic.
    """
    @staticmethod
    def compare_software_versions(
        claimed_version_str: str,
        retrieved_texts: List[str],
        claim_asserts_latest: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Parses versions using packaging.version.Version and determines if claimed version is superseded.
        """
        try:
            clean_claimed = claimed_version_str.lstrip("v").strip()
            v_claim = pkg_version.parse(clean_claimed)
        except Exception:
            return None

        highest_found: Optional[pkg_version.Version] = None
        highest_found_str: Optional[str] = None

        for text in retrieved_texts:
            matches = _VERSION_EXTRACTION_REGEX.findall(text)
            for match in matches:
                candidate_str = match[0].lstrip("v").strip()
                try:
                    candidate = pkg_version.parse(candidate_str)
                    if candidate.base_version and not candidate.is_prerelease:
                        # Avoid treating years (like 2024) as patch versions unless candidate version is reasonable
                        if candidate.major < 2000:
                            if highest_found is None or candidate > highest_found:
                                highest_found = candidate
                                highest_found_str = candidate_str
                except Exception:
                    continue

        if highest_found and claim_asserts_latest:
            # Check if claimed version is in the same major.minor release line
            is_same_minor_line = (
                v_claim.major == highest_found.major and
                hasattr(v_claim, "minor") and hasattr(highest_found, "minor") and
                v_claim.minor == highest_found.minor
            )
            
            if is_same_minor_line or v_claim == highest_found:
                return {
                    "verdict": "CURRENT",
                    "reasoning": f"Claimed version {claimed_version_str} belongs to current official release {highest_found_str}.",
                    "claimed_version": claimed_version_str,
                    "latest_version": highest_found_str,
                    "is_outdated": False
                }
            elif v_claim < highest_found:
                return {
                    "verdict": "OUTDATED",
                    "reasoning": f"Claimed version {claimed_version_str} is superseded by official release {highest_found_str}.",
                    "claimed_version": claimed_version_str,
                    "latest_version": highest_found_str,
                    "is_outdated": True
                }

        return None

    @staticmethod
    def compare_prices(
        claimed_text: str,
        retrieved_snippets: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Compares numeric price mentions.
        """
        claim_match = _PRICE_EXTRACTION_REGEX.search(claimed_text)
        if not claim_match:
            return None

        claim_price = float(claim_match.group(1) or claim_match.group(3))

        retrieved_prices = []
        for snip in retrieved_snippets:
            # Strip out legacy price statements like "Legacy GPT-4 pricing was $30"
            clean_snip = re.sub(r"\b(legacy|was|previously|former|historical|old)\b[^.]*?\$(\d+(\.\d+)?)", "", snip, flags=re.IGNORECASE)
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
