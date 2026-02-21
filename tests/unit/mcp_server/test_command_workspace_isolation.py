from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from command_execution_errors import CommandExecutionError
from command_workspace_guard import resolve_workspace_directory


def test_workspace_guard_allows_paths_inside_workspace():
    target = resolve_workspace_directory(workspace_root="/workspace", requested_working_directory="/workspace/docs")
    assert target.parts[-2:] == ("workspace", "docs")


def test_workspace_guard_blocks_paths_outside_workspace():
    with pytest.raises(CommandExecutionError) as exc:
        resolve_workspace_directory(workspace_root="/workspace", requested_working_directory="/etc")
    assert exc.value.code == "WORKSPACE_ISOLATION_VIOLATION"
