from __future__ import annotations

from flask import jsonify

KNOWN_REASON_CODES = {
    "GIT_DIFF_FAILED",
    "BASE_REF_NOT_FOUND",
    "GIT_NOT_AVAILABLE",
    "DELTA_FALLBACK_UNEXPECTED_ERROR",
    "SOURCE_DELETED",
    "RENAMED_SOURCE_REMOVED",
    "DELETE_NO_RECORDS",
    "CHANGED_INPUT",
    "SKIPPED_UNCHANGED",
    "EXCLUDED_BY_PATTERN",
    "UNSUPPORTED_TYPE",
    "READ_ERROR",
    "EMPTY_FILE",
    "FILE_TOO_LARGE",
    "SOURCE_MISSING",
    "INDEXED",
    "DELETED_STALE",
    "UPSERT_FAILED",
    "EMBEDDING_FAILED",
    "FULL_SCAN_FALLBACK_APPLIED",
}


def error_payload(code: str, message: str, details: str | None = None) -> dict:
    payload = {"errorCode": code, "message": message}
    if details:
        payload["details"] = details
    return payload


def json_error(code: str, message: str, status_code: int, details: str | None = None):
    return jsonify(error_payload(code, message, details)), status_code


def is_known_reason_code(code: str) -> bool:
    return code in KNOWN_REASON_CODES
