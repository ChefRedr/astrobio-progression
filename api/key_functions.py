from __future__ import annotations

from typing import Dict, List, Literal, Tuple
from dataclasses import dataclass
import math
import os
import json
from dotenv import load_dotenv

load_dotenv()

from embeddings_create import data_export

# ---- OpenAI client (no hardcoded keys) ----
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Do `export OPENAI_API_KEY='...'` before running."
    )
client = OpenAI(api_key=OPENAI_API_KEY)
CHROMA_OPENAI_API_KEY = OPENAI_API_KEY

# Models (feel free to change if you prefer different SKUs)
CHAT_MODEL = "gpt-4o-mini"
EMBED_MODEL = "text-embedding-3-small"

# ---- In-memory indices and caches ----

_TITLE_TO_IDX: Dict[str, int] = {}
_ID_TO_IDX: Dict[str, int] = {}

# Caches for synthesized sections
_SYNTH_ABSTRACT: Dict[int, str] = {}
_SYNTH_METHODS: Dict[int, str] = {}
_SYNTH_RESULTS: Dict[int, str] = {}

# Embeddings cache
_EMBED_CACHE: Dict[int, List[float]] = {}

ids, titles, keywords, paragraphs = data_export()

@dataclass(frozen=True)
class ArticleView:
    idx: int
    paper_id: str
    title: str
    keyword_text: str
    flat_text: str


def _normalize_title(s: str) -> str:
    return (s or "").strip().lower()


def _init_indices_once() -> None:
    if _TITLE_TO_IDX:
        return
    for i, t in enumerate(titles):
        _TITLE_TO_IDX[_normalize_title(t)] = i
    for i, pid in enumerate(ids):
        _ID_TO_IDX[(pid or "").strip()] = i


def _flatten_paragraphs(paras: List[dict]) -> str:
    """
    paragraphs[i] looks like: [{'text': 'para1'}, {'text':'para2'}, ...] or a mix.
    This extracts text safely and concatenates with spaces.
    """
    out: List[str] = []
    if isinstance(paras, list):
        for p in paras:
            if isinstance(p, dict) and "text" in p and isinstance(p["text"], str):
                out.append(p["text"].strip())
            elif isinstance(p, str):
                out.append(p.strip())
    return " ".join(out)


def _article_view_by_idx(i: int) -> ArticleView:
    flat = _flatten_paragraphs(paragraphs[i])
    return ArticleView(
        idx=i,
        paper_id=ids[i],
        title=titles[i],
        keyword_text=(keywords[i] or ""),
        flat_text=f"{titles[i]}. {keywords[i] or ''}. {flat}",
    )


def _find_article_idx_by_title(title: str) -> int | None:
    _init_indices_once()
    return _TITLE_TO_IDX.get(_normalize_title(title))


def _cosine(u: List[float], v: List[float]) -> float:
    if not u or not v or len(u) != len(v):
        return 0.0
    dot = 0.0
    nu = 0.0
    nv = 0.0
    for a, b in zip(u, v):
        dot += a * b
        nu += a * a
        nv += b * b
    if nu == 0.0 or nv == 0.0:
        return 0.0
    return dot / (math.sqrt(nu) * math.sqrt(nv))


def _embed(text: str) -> List[float]:
    resp = client.embeddings.create(model=EMBED_MODEL, input=text[:6000])
    return resp.data[0].embedding


def _embedding_for_idx(i: int) -> List[float]:
    if i in _EMBED_CACHE:
        return _EMBED_CACHE[i]
    emb = _embed(_article_view_by_idx(i).flat_text)
    _EMBED_CACHE[i] = emb
    return emb


def _synthesize_sections_for_idx(i: int) -> Tuple[str, str, str]:
    """
    Returns (abstract, methodology, results) — synthesized by LLM.
    Caches results in-memory to avoid repeat calls.
    """
    if i in _SYNTH_ABSTRACT and i in _SYNTH_METHODS and i in _SYNTH_RESULTS:
        return _SYNTH_ABSTRACT[i], _SYNTH_METHODS[i], _SYNTH_RESULTS[i]

    av = _article_view_by_idx(i)

    # Prompt asks model to carve abstract/methods/results from noisy text
    sys = (
        "You extract clean scientific sections from messy article text. "
        "Return strict JSON with keys: abstract, methodology, results."
    )
    user = f"""Title: {av.title}

Keywords: {av.keyword_text}

FullText:
{av.flat_text[:12000]}

Task:
1) Summarize a concise abstract (2–4 sentences).
2) Infer a plausible methodology section from the text (what was done, how, materials, sample/subjects, measurements).
3) Summarize a results section (key findings, quantitative trends if present).

Return ONLY compact JSON like:
{{"abstract": "...", "methodology": "...", "results": "..."}}"""

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
        max_tokens=700,
    )
    content = resp.choices[0].message.content.strip()

    # Be resilient to fenced code blocks
    cleaned = content.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(cleaned)
    except Exception:
        # Fallback: try to coerce a minimal JSON if model deviates
        data = {"abstract": "", "methodology": "", "results": ""}
        # a crude parse: not perfect, but avoids hard failure
        for key in ("abstract", "methodology", "results"):
            start = cleaned.lower().find(key)
            if start != -1:
                # take the next 1200 characters as a rough slice
                data[key] = cleaned[start : start + 1200]

    abs_text = (data.get("abstract") or "").strip()
    met_text = (data.get("methodology") or "").strip()
    res_text = (data.get("results") or "").strip()

    _SYNTH_ABSTRACT[i] = abs_text
    _SYNTH_METHODS[i] = met_text
    _SYNTH_RESULTS[i] = res_text
    return abs_text, met_text, res_text


# ---------------- Public API ----------------

def get_articles_by_topic(topic: str) -> List[Dict[str, str]]:
    """
    Semantic topic search:
    - Embed the topic
    - Compare to each article embedding
    - Return up to 20 best matches
    Falls back to keyword inclusion if embeddings fail for any reason.
    """
    _init_indices_once()

    try:
        q_emb = _embed(topic)
        scored: List[Tuple[float, int]] = []
        for i in range(len(titles)):
            score = _cosine(q_emb, _embedding_for_idx(i))
            scored.append((score, i))
        scored.sort(reverse=True, key=lambda x: x[0])
        top = scored[:20]
        out: List[Dict[str, str]] = []
        for _, i in top:
            av = _article_view_by_idx(i)
            # author list unknown in this pipeline; show first keyword or Unknown
            first_author = "Unknown Author"
            out.append(
                {
                    "ArticleTitle": av.title,
                    "Author": first_author,
                    "Link": "",  # no URL in this data source
                }
            )
        return out
    except Exception:
        # Keyword fallback
        tl = topic.lower()
        out: List[Dict[str, str]] = []
        for i in range(len(titles)):
            av = _article_view_by_idx(i)
            hay = f"{av.title} {av.keyword_text} {av.flat_text}".lower()
            if tl in hay:
                out.append(
                    {
                        "ArticleTitle": av.title,
                        "Author": "Unknown Author",
                        "Link": "",
                    }
                )
            if len(out) >= 20:
                break
        return out


def compare_articles(article1_title: str, article2_title: str) -> List[int]:
    """
    Returns [methodology_score, results_score] as integers 1–100.
    Since data lacks clean sections, we synthesize sections for each article first.
    """
    i1 = _find_article_idx_by_title(article1_title)
    i2 = _find_article_idx_by_title(article2_title)
    if i1 is None or i2 is None:
        raise ValueError("Could not find one or both articles")

    _, meth1, res1 = _synthesize_sections_for_idx(i1)
    _, meth2, res2 = _synthesize_sections_for_idx(i2)

    prompt = f"""Compare these two research articles on methodology and results. Return ONLY a JSON array with two integers.

Article 1: {titles[i1]}
Methodology: {meth1[:1500]}
Results: {res1[:1500]}

Article 2: {titles[i2]}
Methodology: {meth2[:1500]}
Results: {res2[:1500]}

Scoring criteria (1-100):
- 90-100: Nearly identical approaches/findings
- 70-89: Very similar with minor differences
- 50-69: Moderately similar
- 30-49: Some overlap but substantially different
- 10-29: Minimal similarities
- 1-9: Completely different

Return format: [methodology_score, results_score]
Example: [78, 65]"""

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a scientific paper comparison expert. Return only a JSON array of two integers between 1-100.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=60,
    )
    raw = resp.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    scores = json.loads(raw)
    return [int(scores[0]), int(scores[1])]


def get_comparison_deepdive(
    article1_title: str,
    article2_title: str,
    section: Literal["methodology", "results"],
) -> str:
    """
    Returns a 300–500 word analysis of similarities/differences for the chosen section.
    """
    i1 = _find_article_idx_by_title(article1_title)
    i2 = _find_article_idx_by_title(article2_title)
    if i1 is None or i2 is None:
        raise ValueError("Could not find one or both articles")

    abs1, meth1, res1 = _synthesize_sections_for_idx(i1)
    abs2, meth2, res2 = _synthesize_sections_for_idx(i2)

    if section == "methodology":
        c1 = meth1[:2000]
        c2 = meth2[:2000]
        focus = "experimental design, subjects/samples, materials, instruments, protocols, data collection, and analysis techniques"
    else:
        c1 = res1[:2000]
        c2 = res2[:2000]
        focus = "key findings, statistical significance, quantitative trends, conclusions, and practical implications"

    prompt = f"""Provide a detailed comparison explaining the similarities and differences in the {section} of these two research articles.

Article 1: {article1_title}
Abstract: {abs1[:800]}
{section.capitalize()}: {c1}

Article 2: {article2_title}
Abstract: {abs2[:800]}
{section.capitalize()}: {c2}

Focus on: {focus}

Structure:
1. Key Similarities
2. Notable Differences
3. Significance of differences
4. Overall Assessment

Provide 300-500 words."""

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert at analyzing and comparing scientific research.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=900,
    )
    return resp.choices[0].message.content


def get_related_articles(article_title: str) -> List[Dict[str, str]]:
    """
    Finds semantically related articles to `article_title`.
    - Synthesizes abstract & methodology for the source
    - Builds a search text
    - Uses embedding cosine similarity across all articles
    - Filters out source itself
    - Returns top 10 as {ArticleTitle, Author, Link}
    """
    i_src = _find_article_idx_by_title(article_title)
    if i_src is None:
        raise ValueError(f"Article '{article_title}' not found")

    abs_src, meth_src, _ = _synthesize_sections_for_idx(i_src)
    search_text = f"{titles[i_src]} {abs_src} {meth_src[:600]}"

    q_emb = _embed(search_text)

    scored: List[Tuple[float, int]] = []
    for i in range(len(titles)):
        if i == i_src:
            continue
        score = _cosine(q_emb, _embedding_for_idx(i))
        scored.append((score, i))

    scored.sort(reverse=True, key=lambda x: x[0])

    out: List[Dict[str, str]] = []
    for _, i in scored[:15]:  # query 15
        av = _article_view_by_idx(i)
        out.append(
            {
                "ArticleTitle": av.title,
                "Author": "Unknown Author",
                "Link": "",
            }
        )

    return out[:10]  # return top 10