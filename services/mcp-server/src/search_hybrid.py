from __future__ import annotations

import math
import re
from collections import Counter

_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in _TOKEN_PATTERN.finditer(text or "")]


def bm25_scores(
    *,
    query: str,
    documents: dict[str, str],
    k1: float = 1.5,
    b: float = 0.75,
) -> dict[str, float]:
    if not documents:
        return {}

    query_tokens = tokenize(query)
    if not query_tokens:
        return {doc_id: 0.0 for doc_id in documents}

    tokenized_docs: dict[str, list[str]] = {doc_id: tokenize(text) for doc_id, text in documents.items()}
    doc_lengths: dict[str, int] = {doc_id: len(tokens) for doc_id, tokens in tokenized_docs.items()}
    avgdl = sum(doc_lengths.values()) / max(len(doc_lengths), 1)
    avgdl = max(avgdl, 1.0)

    document_frequency: Counter[str] = Counter()
    for tokens in tokenized_docs.values():
        document_frequency.update(set(tokens))

    total_docs = max(len(tokenized_docs), 1)
    query_term_counts = Counter(query_tokens)
    scores: dict[str, float] = {}

    for doc_id, tokens in tokenized_docs.items():
        if not tokens:
            scores[doc_id] = 0.0
            continue
        tf = Counter(tokens)
        dl = max(float(doc_lengths[doc_id]), 1.0)
        score = 0.0
        for token, query_weight in query_term_counts.items():
            freq = tf.get(token, 0)
            if freq == 0:
                continue
            df = document_frequency.get(token, 0)
            idf = math.log(1.0 + ((total_docs - df + 0.5) / (df + 0.5)))
            denom = freq + (k1 * (1.0 - b + b * (dl / avgdl)))
            score += idf * ((freq * (k1 + 1.0)) / max(denom, 1e-9)) * float(query_weight)
        scores[doc_id] = score

    return scores


def normalize_scores(scores: dict[str, float]) -> dict[str, float]:
    if not scores:
        return {}
    minimum = min(scores.values())
    maximum = max(scores.values())
    if math.isclose(minimum, maximum):
        if maximum <= 0.0:
            return {key: 0.0 for key in scores}
        return {key: 1.0 for key in scores}
    scale = maximum - minimum
    return {key: max((value - minimum) / scale, 0.0) for key, value in scores.items()}


def blend_scores(
    *,
    vector_scores: dict[str, float],
    lexical_scores: dict[str, float],
    vector_weight: float,
    lexical_weight: float,
) -> tuple[dict[str, float], dict[str, float], dict[str, float]]:
    normalized_vector = normalize_scores(vector_scores)
    normalized_lexical = normalize_scores(lexical_scores)

    total_weight = max(vector_weight, 0.0) + max(lexical_weight, 0.0)
    if total_weight <= 0.0:
        vector_weight = 1.0
        lexical_weight = 0.0
        total_weight = 1.0

    vector_ratio = max(vector_weight, 0.0) / total_weight
    lexical_ratio = max(lexical_weight, 0.0) / total_weight

    blended: dict[str, float] = {}
    for candidate_id in set(normalized_vector) | set(normalized_lexical):
        blended[candidate_id] = (
            (normalized_vector.get(candidate_id, 0.0) * vector_ratio)
            + (normalized_lexical.get(candidate_id, 0.0) * lexical_ratio)
        )

    return blended, normalized_vector, normalized_lexical


def rerank_scores(
    *,
    query: str,
    documents: dict[str, str],
    blended_scores: dict[str, float],
    lexical_scores: dict[str, float],
    semantic_scores: dict[str, float],
) -> dict[str, float]:
    if not documents:
        return {}

    normalized_blended = normalize_scores(blended_scores)
    normalized_lexical = normalize_scores(lexical_scores)
    normalized_semantic = normalize_scores(semantic_scores)

    query_tokens = set(tokenize(query))
    coverage_scores: dict[str, float] = {}
    for doc_id, text in documents.items():
        if not query_tokens:
            coverage_scores[doc_id] = 0.0
            continue
        doc_tokens = set(tokenize(text))
        if not doc_tokens:
            coverage_scores[doc_id] = 0.0
            continue
        overlap = len(query_tokens.intersection(doc_tokens))
        coverage_scores[doc_id] = overlap / max(len(query_tokens), 1)

    reranked: dict[str, float] = {}
    for candidate_id in documents:
        reranked[candidate_id] = (
            (normalized_blended.get(candidate_id, 0.0) * 0.5)
            + (normalized_lexical.get(candidate_id, 0.0) * 0.2)
            + (normalized_semantic.get(candidate_id, 0.0) * 0.2)
            + (coverage_scores.get(candidate_id, 0.0) * 0.1)
        )
    return reranked
