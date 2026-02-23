from __future__ import annotations

class SearchApiError(RuntimeError):
    def __init__(self, code: str, message: str, status_code: int, details: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


def error_payload(code: str, message: str, details: str | None = None) -> dict:
    payload = {"errorCode": code, "message": message}
    if details:
        payload["details"] = details
    return payload


def json_error(code: str, message: str, status_code: int, details: str | None = None):
    from flask import jsonify

    return jsonify(error_payload(code, message, details)), status_code


def json_error_from_exception(exc: SearchApiError):
    return json_error(exc.code, exc.message, exc.status_code, exc.details)


def invalid_request(message: str, details: str | None = None) -> SearchApiError:
    return SearchApiError("INVALID_REQUEST", message, 400, details)


def search_query_empty() -> SearchApiError:
    return SearchApiError("SEARCH_QUERY_EMPTY", "query must not be empty", 400)


def result_not_found(result_id: str) -> SearchApiError:
    return SearchApiError("RESULT_NOT_FOUND", f"Result '{result_id}' is not found", 404)


def backend_error(message: str, details: str | None = None) -> SearchApiError:
    return SearchApiError("SEARCH_BACKEND_ERROR", message, 502, details)


def docs_collection_unavailable(details: str | None = None) -> SearchApiError:
    return SearchApiError(
        "DOCS_COLLECTION_UNAVAILABLE",
        "Docs collection is temporarily unavailable",
        503,
        details,
    )


def docs_reranking_unavailable(details: str | None = None) -> SearchApiError:
    return SearchApiError(
        "DOCS_RERANKING_UNAVAILABLE",
        "Docs reranking stage is temporarily unavailable",
        503,
        details,
    )


def collection_not_found(collection_name: str) -> SearchApiError:
    return SearchApiError(
        "SEARCH_COLLECTION_NOT_FOUND",
        f"Collection '{collection_name}' is not found",
        404,
    )
