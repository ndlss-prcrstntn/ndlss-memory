from __future__ import annotations

from dataclasses import replace

from watch_mode_models import WatchEvent, now_iso

_PRIORITY = {
    "created": 1,
    "updated": 2,
    "deleted": 3,
}


def _normalize_event(event: WatchEvent) -> list[WatchEvent]:
    if event.event_type != "renamed":
        return [event]
    normalized: list[WatchEvent] = []
    if event.old_path:
        normalized.append(
            WatchEvent(
                event_type="deleted",
                path=event.old_path,
                old_path=event.old_path,
                detected_at=event.detected_at,
            )
        )
    normalized.append(
        WatchEvent(
            event_type="updated",
            path=event.path,
            old_path=event.old_path,
            detected_at=event.detected_at,
        )
    )
    return normalized


def coalesce_events(events: list[WatchEvent]) -> list[WatchEvent]:
    by_path: dict[str, WatchEvent] = {}
    for event in events:
        for normalized in _normalize_event(event):
            current = by_path.get(normalized.path)
            if current is None:
                by_path[normalized.path] = normalized
                continue

            if current.event_type == "deleted" and normalized.event_type in {"created", "updated"}:
                by_path[normalized.path] = replace(normalized, event_type="updated")
                continue

            if _PRIORITY.get(normalized.event_type, 0) >= _PRIORITY.get(current.event_type, 0):
                by_path[normalized.path] = normalized

    coalesced_at = now_iso()
    result: list[WatchEvent] = []
    for event in by_path.values():
        event.coalesced_at = coalesced_at
        result.append(event)
    return result
