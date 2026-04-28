from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("deerflow-learning-repo-reader")
REPO_ROOT = Path(__file__).resolve().parents[2]
ALLOWED_ROOTS = (
    REPO_ROOT / "app",
    REPO_ROOT / "packages",
    REPO_ROOT / "docs",
    REPO_ROOT / "tests",
    REPO_ROOT / "examples",
)


def _resolve_learning_path(relative_path: str) -> Path:
    requested = (REPO_ROOT / relative_path).resolve()
    if not any(requested == root.resolve() or requested.is_relative_to(root.resolve()) for root in ALLOWED_ROOTS):
        raise ValueError("Path is outside the allowed DeerFlow backend learning roots")
    return requested


@mcp.tool()
def list_learning_paths(relative_path: str = "app", max_entries: int = 80) -> str:
    """List files and directories under the read-only learning roots."""
    path = _resolve_learning_path(relative_path)
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {relative_path}")
    if path.is_file():
        return path.relative_to(REPO_ROOT).as_posix()

    entries = []
    for child in sorted(path.iterdir(), key=lambda item: item.name.lower()):
        suffix = "/" if child.is_dir() else ""
        entries.append(f"{child.relative_to(REPO_ROOT).as_posix()}{suffix}")
        if len(entries) >= max_entries:
            entries.append("...")
            break
    return "\n".join(entries)


@mcp.tool()
def read_learning_file(relative_path: str, max_chars: int = 12000) -> str:
    """Read a UTF-8 text file from the DeerFlow backend learning roots."""
    path = _resolve_learning_path(relative_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {relative_path}")
    return path.read_text(encoding="utf-8")[:max_chars]


if __name__ == "__main__":
    mcp.run()
