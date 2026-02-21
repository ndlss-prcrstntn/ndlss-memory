from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from ingestion_pipeline.embedding_models import EmbeddingTask
from ingestion_pipeline.embedding_provider import EmbeddingProvider
from ingestion_pipeline.embedding_retry import generate_embedding_with_retry


def test_embedding_retry_succeeds_after_transient_error():
    provider = EmbeddingProvider(vector_size=4)
    task = EmbeddingTask(task_id="task-1", chunk_id="chunk-1")
    result = generate_embedding_with_retry(
        task=task,
        content="retry me [[EMBEDDING_TRANSIENT]]",
        provider=provider,
        max_attempts=2,
        backoff_seconds=0.0,
        sleep_fn=lambda _: None,
    )
    assert result.embedding is not None
    assert result.retries_used == 1
    assert task.status == "success"
    assert task.attempt_count == 2


def test_embedding_retry_stops_on_fatal_error():
    provider = EmbeddingProvider(vector_size=4)
    task = EmbeddingTask(task_id="task-2", chunk_id="chunk-2")
    result = generate_embedding_with_retry(
        task=task,
        content="fatal [[EMBEDDING_FATAL]]",
        provider=provider,
        max_attempts=3,
        backoff_seconds=0.0,
        sleep_fn=lambda _: None,
    )
    assert result.embedding is None
    assert result.retries_used == 0
    assert task.status == "failed"
    assert task.last_error_code == "EMBEDDING_FATAL_ERROR"

