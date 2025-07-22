import argparse
from pathlib import Path

import file_utils
from _logger import logger
from find_key import find_server_dict
from parent_parser import create_parent_parser
from _types import Any


def enable_key(data: dict[str, Any], key: str) -> dict[str, Any]:
    """Enable a MCP server in VSCode settings.json file.

    Args:
        data: settings.json dictionary
        key: Key to enable.

    Returns:
        dict[str, Any]: Modified data.
    """
    data[key]["disabled"] = False
    return data


def enable_keys(file_path: Path, keys: list[str], dry_run: bool) -> None:
    """Enable MCP servers in VSCode settings.json file.

    Args:
        file_path: Path to VSCode settings.json file.
        keys: List of MCP servers to enable.
        dry_run: If True, do not write to file.
    """
    data = file_utils.read_json(file_path)

    key_name = find_server_dict(data)
    if key_name is None:
        target_dict = data
        key_name = "top-level"
    else:
        target_dict = data[key_name]

    modified = False
    for key in keys:
        if key in target_dict:
            enable_key(target_dict, key)

            logger.info(f"Enabled '{key}' from {key_name}.")
            modified = True
        else:
            logger.warning(f"Key '{key}' not found in {key_name}, skipping.")

    if dry_run:
        logger.info("Dry run complete.")
        return

    if modified:
        file_utils.write_json(data, file_path)
        logger.info(f"Updated {file_path}")
    else:
        logger.info("No changes made.")


def create_enable_parser(
    mcp_parser: argparse.ArgumentParser, argv: list[str]
) -> argparse.Namespace:
    """Create argparse parser for enable command.

    Args:
        mcp_parser: Parent parser for enable command.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    enable_parser = argparse.ArgumentParser(
        description="Enable MCP servers in VSCode settings.json file.",
        prog="unload",
        parents=[mcp_parser],
    )

    enable_parser.add_argument(
        "servers",
        nargs="+",
        help="Servers to enable.",
        metavar="SERVER1 SERVER2 SERVER3",
    )

    return enable_parser.parse_args()


def main(argv=None):
    """Enable MCP servers in VSCode settings.json file."""
    if not argv:
        argv = sys.argv
    mcp_parser = create_parent_parser()
    args = create_enable_parser(mcp_parser, argv)

    enable_keys(args.config, args.servers, args.dry_run)


if __name__ == "__main__":
    import sys

    main()

    sys.exit(0)
