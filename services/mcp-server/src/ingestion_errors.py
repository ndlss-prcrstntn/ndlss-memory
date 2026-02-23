from __future__ import annotations

from flask import jsonify

INVALID_LIMIT_VALUE = "INVALID_LIMIT_VALUE"
DOCS_INDEXING_FAILED = "DOCS_INDEXING_FAILED"
DOCS_COLLECTION_UNAVAILABLE = "DOCS_COLLECTION_UNAVAILABLE"


def classify_pipeline_exception(exc: Exception) -> tuple[str, str]:
    message = str(exc).strip() or exc.__class__.__name__
    class_name = exc.__class__.__name__
    normalized = message.lower()
    if "docs" in normalized:
        return DOCS_INDEXING_FAILED, message
    if class_name == "UpsertError" or "qdrant" in normalized or "upsert" in normalized:
        return "INGESTION_PERSISTENCE_FAILED", message
    return "INGESTION_PIPELINE_FAILED", message


def error_payload(code: str, message: str, details: str | None = None) -> dict:
    payload = {"errorCode": code, "message": message}
    if details:
        payload["details"] = details
    return payload


def json_error(code: str, message: str, status_code: int, details: str | None = None):
    return jsonify(error_payload(code, message, details)), status_code

