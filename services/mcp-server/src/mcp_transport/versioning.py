from __future__ import annotations

import os


def resolve_service_version(default: str = "unknown") -> str:
    for key in ("NDLSS_VERSION", "NDLSS_IMAGE_TAG", "NDLSS_GIT_REF"):
        value = os.getenv(key, "").strip()
        if value:
            return value
    return default
