import os
from datetime import datetime, timezone
from flask import Flask, jsonify
import yaml

SERVICE_NAMES = ("qdrant", "file-indexer", "mcp-server")
STATUS_ENV_MAP = {
    "qdrant": "SERVICE_QDRANT_STATUS",
    "file-indexer": "SERVICE_FILE_INDEXER_STATUS",
    "mcp-server": "SERVICE_MCP_SERVER_STATUS",
}

app = Flask(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _split_csv(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def load_security_policy() -> dict:
    path = "/app/config/security-policy.yaml"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def build_runtime_config() -> dict:
    policy = load_security_policy()
    timeout_value = os.getenv("COMMAND_TIMEOUT_SECONDS", str(policy.get("command_timeout_seconds", 20)))
    allowlist_env = os.getenv("COMMAND_ALLOWLIST", "")
    allowlist_cfg = policy.get("command_allowlist", [])
    allowlist = _split_csv(allowlist_env) if allowlist_env else allowlist_cfg
    return {
        "projectName": os.getenv("COMPOSE_PROJECT_NAME", "ndlss-memory"),
        "qdrantPort": int(os.getenv("QDRANT_PORT", "6333")),
        "mcpPort": int(os.getenv("MCP_PORT", "8080")),
        "indexMode": os.getenv("INDEX_MODE", "full-scan"),
        "indexFileTypes": _split_csv(os.getenv("INDEX_FILE_TYPES", ".md,.txt,.json,.yml,.yaml")),
        "indexExcludePatterns": _split_csv(os.getenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build")),
        "commandAllowlist": allowlist,
        "commandTimeoutSeconds": int(timeout_value),
    }


def build_service_status(name: str) -> dict:
    env_key = STATUS_ENV_MAP[name]
    status = os.getenv(env_key, "healthy")
    return {
        "name": name,
        "status": status,
        "lastCheck": _now_iso(),
        "details": f"Service '{name}' reported by runtime status map",
    }


def build_system_status() -> dict:
    services = [build_service_status(name) for name in SERVICE_NAMES]
    statuses = {item["status"] for item in services}
    if statuses == {"healthy"}:
        overall = "healthy"
        issues = []
    elif "healthy" in statuses:
        overall = "degraded"
        issues = ["One or more services are not healthy"]
    else:
        overall = "down"
        issues = ["No healthy services detected"]
    return {
        "timestamp": _now_iso(),
        "overallStatus": overall,
        "services": services,
        "issues": issues,
    }


@app.get("/health")
def get_health():
    return jsonify({"status": "ok", "timestamp": _now_iso()})


@app.get("/v1/system/status")
def get_system_status():
    return jsonify(build_system_status())


@app.get("/v1/system/config")
def get_runtime_config():
    return jsonify(build_runtime_config())


@app.get("/v1/system/services/<service_name>")
def get_service_status(service_name: str):
    if service_name not in SERVICE_NAMES:
        return (
            jsonify(
                {
                    "errorCode": "SERVICE_NOT_FOUND",
                    "message": f"Service '{service_name}' is not registered",
                    "details": "Available services: qdrant, file-indexer, mcp-server",
                }
            ),
            404,
        )
    return jsonify(build_service_status(service_name))


if __name__ == "__main__":
    port = int(os.getenv("MCP_PORT", "8080"))
    app.run(host="0.0.0.0", port=port)

