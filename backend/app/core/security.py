import re
import html
from typing import Tuple, List

# Patterns frequently used in prompt injection attempts embedded in untrusted web pages
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
    r"you\s+are\s+now\s+(a|an)?\s*",
    r"system\s*prompt\s*:",
    r"disregard\s+the\s+above",
    r"new\s+instructions?:",
    r"override\s+system\s+directives?",
    r"output\s+only\s+(verified|current|true)",
    r"mark\s+this\s+claim\s+(as\s+)?(verified|current)",
    r"assistant\s*:",
    r"human\s*:",
    r"eval\(",
    r"<script.*?>",
]

_INJECTION_REGEX = re.compile("|".join(PROMPT_INJECTION_PATTERNS), re.IGNORECASE)


def detect_prompt_injection(text: str) -> Tuple[bool, List[str]]:
    """
    Scans untrusted evidence text for prompt injection keywords/patterns.
    Returns (is_suspicious, matched_patterns).
    """
    if not text:
        return False, []
    
    matches = _INJECTION_REGEX.findall(text)
    if matches:
        # Normalize matches
        detected = [str(m) if isinstance(m, str) else "".join(m) for m in matches]
        return True, [d for d in detected if d.strip()]
    return False, []


def sanitize_untrusted_text(text: str) -> str:
    """
    Sanitizes untrusted web evidence content:
    - Escapes dangerous HTML
    - Defangs raw control tags
    - Limits runaway string lengths
    """
    if not text:
        return ""
    
    clean = text.strip()
    # Defang possible xml/markdown command injection tokens
    clean = clean.replace("```", "'''")
    clean = clean.replace("<script", "&lt;script")
    clean = clean.replace("</script>", "&lt;/script&gt;")
    clean = clean.replace("<system>", "&lt;system&gt;")
    clean = clean.replace("</system>", "&lt;/system&gt;")
    
    # Cap single snippet length to avoid context stuffing
    if len(clean) > 2500:
        clean = clean[:2500] + " [truncated by TruthGuard security filter]"
        
    return clean

