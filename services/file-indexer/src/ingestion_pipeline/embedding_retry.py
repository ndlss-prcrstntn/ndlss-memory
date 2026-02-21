from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from ingestion_pipeline.embedding_models import EmbeddingTask
from ingestion_pipeline.embedding_provider import EmbeddingError, EmbeddingFatalError, EmbeddingProvider, EmbeddingTransientError


@dataclass(frozen=True)
class EmbeddingRetryResult:
    task: EmbeddingTask
    embedding: list[float] | None
    retries_used: int


def generate_embedding_with_retry(
    *,
    task: EmbeddingTask,
    content: str,
    provider: EmbeddingProvider,
    max_attempts: int,
    backoff_seconds: float,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> EmbeddingRetryResult:
    retries_used = 0
    for attempt in range(1, max_attempts + 1):
        task.mark_running()
        try:
            embedding = provider.generate_embedding(content)
            task.mark_success()
            return EmbeddingRetryResult(task=task, embedding=embedding, retries_used=retries_used)
        except EmbeddingTransientError as exc:
            task.mark_failed("EMBEDDING_TRANSIENT_ERROR", str(exc))
            if attempt >= max_attempts:
                return EmbeddingRetryResult(task=task, embedding=None, retries_used=retries_used)
            retries_used += 1
            sleep_fn(backoff_seconds)
        except EmbeddingFatalError as exc:
            task.mark_failed("EMBEDDING_FATAL_ERROR", str(exc))
            return EmbeddingRetryResult(task=task, embedding=None, retries_used=retries_used)
        except EmbeddingError as exc:
            task.mark_failed("EMBEDDING_PROVIDER_ERROR", str(exc))
            return EmbeddingRetryResult(task=task, embedding=None, retries_used=retries_used)
        except Exception as exc:  # pragma: no cover
            task.mark_failed("EMBEDDING_UNKNOWN_ERROR", str(exc))
            return EmbeddingRetryResult(task=task, embedding=None, retries_used=retries_used)

    task.mark_failed("EMBEDDING_UNKNOWN_ERROR", "No embedding attempts executed")
    return EmbeddingRetryResult(task=task, embedding=None, retries_used=retries_used)

