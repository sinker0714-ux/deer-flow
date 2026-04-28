import json
from pathlib import Path

from deerflow.config.extensions_config import McpServerConfig
from deerflow.mcp.client import build_server_params


def test_learning_mcp_example_declares_disabled_stdio_server():
    example_path = Path(__file__).resolve().parents[1] / "examples" / "learning_mcp" / "extensions_config.learning.example.json"
    raw = json.loads(example_path.read_text(encoding="utf-8"))
    server = raw["mcpServers"]["learning-repo-reader"]

    assert server["enabled"] is False

    params = build_server_params("learning-repo-reader", McpServerConfig.model_validate(server))

    assert params["transport"] == "stdio"
    assert params["command"] == "python"
    assert params["args"] == ["backend/examples/learning_mcp/repo_reader_server.py"]
