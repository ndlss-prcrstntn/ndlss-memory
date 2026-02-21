from __future__ import annotations

from flask import jsonify


def error_payload(code: str, message: str, details: str | None = None) -> dict:
    payload = {"errorCode": code, "message": message}
    if details:
        payload["details"] = details
    return payload


def json_error(code: str, message: str, status_code: int, details: str | None = None):
    return jsonify(error_payload(code, message, details)), status_code

