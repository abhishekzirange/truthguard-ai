import re
import uuid
import logging
from typing import List, Dict, Any, Optional
from app.integrations.bifrost_adapter import BifrostAdapter
from app.engines.classification_engine import ClassificationEngine

logger = logging.getLogger("truthguard.extraction")

_VERSION_MENTION_REGEX = re.compile(r"\b(\d+(\.\d+)+[a-zA-Z0-9_\-\.]*)\b")
_DATE_MENTION_REGEX = re.compile(r"\b((19|20)\d{2}|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}(,\s+(19|20)\d{2})?)\b", re.IGNORECASE)


class ClaimExtractionEngine:
    """
    Decomposes an AI-generated answer into atomic, independently verifiable factual claims.
    """
    def __init__(self, bifrost_adapter: Optional[BifrostAdapter] = None):
        self.bifrost = bifrost_adapter or BifrostAdapter()

    async def extract_claims(self, text: str, domain: str = "general") -> List[Dict[str, Any]]:
        clean_text = text.strip()
        if not clean_text:
            return []

        # Try LLM extraction if Bifrost is available
        if self.bifrost.api_key:
            try:
                llm_claims = await self._extract_via_bifrost(clean_text, domain)
                if llm_claims and len(llm_claims) > 0:
                    return llm_claims
            except Exception as e:
                logger.warning(f"Bifrost claim extraction failed: {e}. Falling back to deterministic extractor.")

        # Deterministic extraction fallback
        return self._extract_deterministic(clean_text, domain)

    async def _extract_via_bifrost(self, text: str, domain: str) -> List[Dict[str, Any]]:
        system_prompt = (
            "You are TruthGuard's Claim Extraction Engine. Break the provided text into atomic factual claims.\n"
            "An atomic claim is a single independently verifiable assertion.\n"
            "Do NOT extract subjective opinions.\n"
            "Return JSON format:\n"
            "{\n"
            '  "claims": [\n'
            '    {\n'
            '      "claim_text": "Python 3.11 is the latest stable Python release.",\n'
            '      "subject": "Python",\n'
            '      "predicate": "is the latest stable release",\n'
            '      "object": "3.11",\n'
            '      "category": "software_version",\n'
            '      "temporal_sensitivity": "HIGH",\n'
            '      "mentioned_date": null,\n'
            '      "mentioned_version": "3.11",\n'
            '      "verification_query": "Python latest stable release version official python.org",\n'
            '      "extraction_confidence": 0.95\n'
            "    }\n"
            "  ]\n"
            "}"
        )
        user_prompt = f"Domain: {domain}\n\nAI Answer:\n{text}"
        res = await self.bifrost.generate_structured_json(system_prompt, user_prompt, temperature=0.0)
        if res.get("success") and res.get("content"):
            claims_data = res["content"].get("claims", [])
            results = []
            for item in claims_data:
                classification = ClassificationEngine.classify_claim(item.get("claim_text", ""), domain)
                results.append({
                    "id": str(uuid.uuid4()),
                    "claim_text": item.get("claim_text", "").strip(),
                    "subject": item.get("subject"),
                    "predicate": item.get("predicate"),
                    "object": item.get("object"),
                    "category": item.get("category") or classification["category"],
                    "temporal_sensitivity": item.get("temporal_sensitivity") or classification["temporal_sensitivity"],
                    "mentioned_date": item.get("mentioned_date"),
                    "mentioned_version": item.get("mentioned_version"),
                    "verification_query": item.get("verification_query"),
                    "extraction_confidence": float(item.get("extraction_confidence", 0.9)),
                })
            return results
        return []

    def _extract_deterministic(self, text: str, domain: str) -> List[Dict[str, Any]]:
        """
        Regex and heuristic atomic sentence parser.
        Splits on sentence terminators while preserving version numbers and abbreviations.
        """
        # Protect common version patterns from being split by period
        protected = re.sub(r"(\d+)\.(\d+)", r"\1<DOT>\2", text)
        sentences = re.split(r"(?<=[.!?])\s+|\n+", protected)
        
        extracted = []
        for raw in sentences:
            sentence = raw.replace("<DOT>", ".").strip()
            if len(sentence) < 8:
                continue

            # Classify
            classification = ClassificationEngine.classify_claim(sentence, domain)
            
            # Detect version mentions (support semantic versions, CalVer, and major versions like Node.js 12, React 16)
            version_val = None
            for m in re.finditer(r"\b(?:v|version\s*)?(\d+(?:\.\d+)*([a-zA-Z0-9_\-\.]+)?)\b", sentence, re.IGNORECASE):
                cand = m.group(1).lstrip("v").strip()
                # Exclude calendar years (1900-2099) when no minor version exists
                if cand.isdigit() and len(cand) == 4 and (cand.startswith("19") or cand.startswith("20")):
                    continue
                version_val = cand
                break

            # Detect date mentions
            date_match = _DATE_MENTION_REGEX.search(sentence)
            date_val = date_match.group(1) if date_match else None

            # Extract subject / predicate / object heuristics
            subject, predicate, obj = self._parse_spo(sentence)

            # Generate query
            query = f"{subject or ''} {sentence}".strip()
            if version_val:
                query = f"{subject or ''} latest version release notes official"

            extracted.append({
                "id": str(uuid.uuid4()),
                "claim_text": sentence,
                "subject": subject,
                "predicate": predicate,
                "object": obj,
                "category": classification["category"],
                "temporal_sensitivity": classification["temporal_sensitivity"],
                "mentioned_date": date_val,
                "mentioned_version": version_val,
                "verification_query": query.strip(),
                "extraction_confidence": 0.92,
            })

        return extracted

    def _parse_spo(self, sentence: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """Heuristic Subject-Predicate-Object extractor."""
        words = sentence.split()
        if len(words) < 3:
            return None, None, None

        # Look for copula or common predicates
        predicates = ["is the latest", "is latest", "is", "supports", "costs", "released", "announced", "requires"]
        sentence_lower = sentence.lower()
        for p in predicates:
            if f" {p} " in sentence_lower:
                idx = sentence_lower.find(f" {p} ")
                subject = sentence[:idx].strip()
                rest = sentence[idx + len(p) + 2:].strip()
                return subject, p, rest

        # Fallback to first word as subject
        return words[0], " ".join(words[1:3]), " ".join(words[3:])

