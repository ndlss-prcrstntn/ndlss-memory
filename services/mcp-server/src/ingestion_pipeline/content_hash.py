from __future__ import annotations

import hashlib


def build_content_hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def build_text_hash(content: str) -> str:
    return build_content_hash(content.encode("utf-8"))

