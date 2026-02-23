from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class McpToolDescriptor:
    name: str
    description: str
    input_schema: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


class McpToolRegistry:
    def __init__(self, descriptors: list[McpToolDescriptor]) -> None:
        self._descriptors = {item.name: item for item in descriptors}

    @classmethod
    def default(cls) -> "McpToolRegistry":
        return cls(
            descriptors=[
                McpToolDescriptor(
                    name="semantic_search",
                    description="Search indexed chunks by semantic query.",
                    input_schema={
                        "type": "object",
                        "required": ["query"],
                        "properties": {
                            "query": {"type": "string"},
                            "limit": {"type": "integer", "minimum": 1},
                            "filters": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string"},
                                    "folder": {"type": "string"},
                                    "fileType": {"type": "string"},
                                },
                                "additionalProperties": False,
                            },
                        },
                        "additionalProperties": False,
                    },
                ),
                McpToolDescriptor(
                    name="search_docs",
                    description="Search markdown documentation collection only.",
                    input_schema={
                        "type": "object",
                        "required": ["query"],
                        "properties": {
                            "query": {"type": "string"},
                            "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                            "workspacePath": {"type": "string"},
                        },
                        "additionalProperties": False,
                    },
                ),
                McpToolDescriptor(
                    name="get_source_by_id",
                    description="Resolve full source payload by search result ID.",
                    input_schema={
                        "type": "object",
                        "required": ["resultId"],
                        "properties": {"resultId": {"type": "string"}},
                        "additionalProperties": False,
                    },
                ),
                McpToolDescriptor(
                    name="get_metadata_by_id",
                    description="Resolve metadata payload by search result ID.",
                    input_schema={
                        "type": "object",
                        "required": ["resultId"],
                        "properties": {"resultId": {"type": "string"}},
                        "additionalProperties": False,
                    },
                ),
                McpToolDescriptor(
                    name="start_ingestion",
                    description="Start ingestion run for a workspace.",
                    input_schema={
                        "type": "object",
                        "properties": {"workspacePath": {"type": "string"}},
                        "additionalProperties": False,
                    },
                ),
                McpToolDescriptor(
                    name="get_ingestion_status",
                    description="Get ingestion run status by run ID.",
                    input_schema={
                        "type": "object",
                        "required": ["runId"],
                        "properties": {"runId": {"type": "string"}},
                        "additionalProperties": False,
                    },
                ),
            ]
        )

    def list_tools(self) -> list[dict[str, Any]]:
        return [item.as_dict() for item in self._descriptors.values()]

    def has_tool(self, name: str) -> bool:
        return name in self._descriptors

    def get_tool(self, name: str) -> McpToolDescriptor | None:
        return self._descriptors.get(name)

