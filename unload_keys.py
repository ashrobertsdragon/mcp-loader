import argparse
from pathlib import Path

import file_utils
from _logger import logger
from find_key import find_server_dict
from parent_parser import create_parent_parser
from _types import Any


def disable_key(data: dict[str, Any], key: str) -> dict[str, Any]:
    """Disable a MCP server in VSCode settings.json file.

    Args:
        data: settings.json dictionary
        key: Key to disable.

    Returns:
        dict[str, Any]: Modified data.
    """
    data[key]["disabled"] = True
    return data


def delete_key(data: dict[str, Any], key: str) -> dict[str, Any]:
    """Delete a key from a dictionary.

    Args:
        data: Dictionary to delete key from.
        key: Key to delete.

    Returns:
        dict[str, Any]: Dictionary with key deleted.
    """
    del data[key]
    return data


def unload_keys(
    file_path: Path, keys: list[str], dry_run: bool, disable: bool
) -> None:
    """Unload MCP servers from config or master MCP Servers file.

    Args:
        file_path: Path to config or master MCP Servers file.
        keys: List of MCP servers to unload.
        dry_run: If True, do not write to file.
        disable: If True, disable the MCP server instead of removing it.
            (VSCode only)
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
            disable_key(target_dict, key) if disable else delete_key(
                target_dict, key
            )

            logger.info(
                f"{'Disabled' if disable else 'Unloaded'} {key}' from {key_name}."
            )
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


def create_unload_parser(
    mcp_parser: argparse.ArgumentParser, argv: list[str]
) -> argparse.Namespace:
    """Create argparse parser for unload command.

    Args:
        mcp_parser: Parent parser for unload command.
        argv: Command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    unload_parser = argparse.ArgumentParser(
        description="Unload MCP servers from config or master MCP Servers file.",
        prog="unload",
        parents=[mcp_parser],
    )

    unload_parser.add_argument(
        "servers",
        nargs="+",
        help="Servers to unload from source file.",
        metavar="SERVER1 SERVER2 SERVER3",
    )

    unload_parser.add_argument(
        "--disable",
        action="store_true",
        help="Disable servers but keep in config file (VSCode only)",
    )

    return unload_parser.parse_args(argv)


def main(argv=None):
    """Unload MCP servers from config or master MCP Servers file."""
    if not argv:
        argv = sys.argv
    mcp_parser = create_parent_parser()
    args = create_unload_parser(mcp_parser, argv)

    unload_keys(args.config, args.servers, args.dry_run, args.disable)


if __name__ == "__main__":
    import sys

    main()

    sys.exit(0)
