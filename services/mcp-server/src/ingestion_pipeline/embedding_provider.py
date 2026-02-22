from __future__ import annotations

import hashlib
import os


class EmbeddingError(RuntimeError):
    pass


class EmbeddingTransientError(EmbeddingError):
    pass


class EmbeddingFatalError(EmbeddingError):
    pass


class EmbeddingProvider:
    def __init__(self, vector_size: int = 16) -> None:
        if vector_size < 1:
            raise ValueError("vector_size must be >= 1")
        self.vector_size = vector_size
        self._transient_seen: set[str] = set()

    def generate_embedding(self, content: str) -> list[float]:
        if not content.strip():
            raise EmbeddingFatalError("Chunk content is empty")

        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if "[[EMBEDDING_FATAL]]" in content:
            raise EmbeddingFatalError("Provider returned fatal error")
        if "[[EMBEDDING_TRANSIENT]]" in content and digest not in self._transient_seen:
            self._transient_seen.add(digest)
            raise EmbeddingTransientError("Provider transient error")

        vector: list[float] = []
        for index in range(self.vector_size):
            offset = (index * 4) % len(digest)
            sample = digest[offset : offset + 4]
            vector.append(int(sample, 16) / 65535.0)
        return vector


def provider_from_env() -> EmbeddingProvider:
    return EmbeddingProvider(vector_size=int(os.getenv("INGESTION_EMBEDDING_VECTOR_SIZE", "16")))

