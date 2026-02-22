from __future__ import annotations

import re

from search_errors import invalid_request

RESULT_ID_PREFIX = "chunk:"
HEX64_RE = re.compile(r"^[0-9a-fA-F]{64}$")
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def build_result_id(point_id: str) -> str:
    normalized = str(point_id).strip()
    return f"{RESULT_ID_PREFIX}{normalized}"


def parse_result_id(result_id: str) -> str:
    raw = str(result_id).strip()
    if not raw:
        raise invalid_request("resultId must not be empty")

    if raw.startswith(RESULT_ID_PREFIX):
        point_id = raw[len(RESULT_ID_PREFIX) :]
    else:
        point_id = raw

    if not HEX64_RE.match(point_id) and not UUID_RE.match(point_id):
        raise invalid_request("resultId has invalid format")
    return point_id.lower()

