# Chunking Embeddings Fixture Manifest

## Purpose

Fixture set for deterministic chunking, embedding retry, metadata coverage, and
pipeline idempotency checks.

## Structure

- `valid/docs/readme.md`: markdown content with multiple paragraphs.
- `valid/text/sample.txt`: plain text for overlap checks.
- `retry/transient.txt`: contains marker `[[EMBEDDING_TRANSIENT]]`.
- `retry/fatal.txt`: contains marker `[[EMBEDDING_FATAL]]`.
- `empty/blank.txt`: empty file for skip handling.
- `oversized/big.txt`: file larger than `INDEX_MAX_FILE_SIZE_BYTES`.

## Validation Rules

- Content files must be UTF-8 encoded.
- `retry/transient.txt` should eventually succeed with retry policy.
- `retry/fatal.txt` should fail without transient retries.
- Manifest updates must preserve deterministic relative paths.
