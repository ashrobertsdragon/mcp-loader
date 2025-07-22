from _types import Any


def find_server_dict(data: dict[str, Any]) -> str | None:
    return next((key for key in ["server", "mcpServers"] if key in data), None)
