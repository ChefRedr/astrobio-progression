import re
import math
import unicodedata
from typing import Iterable, List, Any

# Rough, conservative char cap so inputs won't exceed embedding token limits.
# (OpenAI counts tokens, not chars; this cap errs on the safe side.)
_DEFAULT_MAX_CHARS = 24000

# Precompiled regexes
_CTRL_CHARS = re.compile(r"[\x00-\x1F\x7F]")  # ASCII control chars
_HSPACE     = re.compile(r"[ \t\f\v]+")       # horizontal whitespace runs
_DBLSPACE   = re.compile(r" {2,}")            # multiple spaces

def _to_text(x: Any) -> str:
    """Coerce various input types to str safely."""
    if x is None:
        return ""
    if isinstance(x, bytes):
        # try utf-8; replace undecodable bytes
        return x.decode("utf-8", errors="replace")
    # protect against numpy/pandas NaN
    try:
        if isinstance(x, float) and math.isnan(x):
            return ""
    except Exception:
        pass
    s = str(x)
    return s if s != "nan" else ""  # pandas str(NaN) -> 'nan'

def clean_documents(
    documents: Iterable[Any],
    *,
    max_chars: int = _DEFAULT_MAX_CHARS
) -> List[str]:
    """
    Make documents safe for OpenAI embeddings:
      - Coerce to string; handle None/NaN/bytes
      - Unicode NFC normalize
      - Replace newlines with spaces (per OpenAI examples)
      - Remove ASCII control characters
      - Collapse whitespace; trim ends
      - Ensure non-empty (fallback ".")
      - Cap length to avoid token-limit errors
    """
    cleaned: List[str] = []
    for doc in documents:
        s = _to_text(doc)

        # Normalize unicode
        s = unicodedata.normalize("NFC", s)

        # Per OpenAI example: replace newlines with spaces
        s = s.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ")

        # Strip control chars (except we already removed newlines above)
        s = _CTRL_CHARS.sub(" ", s)

        # Collapse excessive whitespace
        s = _HSPACE.sub(" ", s)
        s = _DBLSPACE.sub(" ", s).strip()

        # Ensure non-empty (OpenAI rejects empty inputs)
        if not s:
            s = "."

        # Conservative length cap (char proxy for token budget)
        if len(s) > max_chars:
            s = s[:max_chars].rstrip()

        cleaned.append(s)

    return cleaned
