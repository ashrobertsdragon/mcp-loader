import argparse
import sys
from pathlib import Path

import file_utils
from find_key import find_server_dict
from _logger import logger
from parent_parser import create_parent_parser


def load_keys(
    src_path: Path, dst_path: Path, keys: list[str], dry_run: bool
) -> None:
    """Load MCP servers from config or master MCP Servers file.

    Args:
        src_path: Path to config or master MCP Servers file.
        dst_path: Path to config or master MCP Servers file.
        keys: List of MCP servers to load.
        dry_run: If True, do not write to file.
    """
    src_json = file_utils.read_json(src_path)
    src_key = find_server_dict(src_json)
    src = src_json[src_key] if src_key is not None else src_json

    dst_json = file_utils.read_json(dst_path)
    dst_key = find_server_dict(dst_json)

    if dst_key is None:
        logger.error(
            "Destination JSON must have a 'servers' or 'mcpServers' dict."
        )
        sys.exit(1)
    dst = dst_json[dst_key]

    for key in keys:
        if key not in src:
            logger.error(f"Key '{key}' not found in source JSON.")
            sys.exit(1)
        dst[key] = src[key]
        if src[key].get("url") is not None and dst_key == "servers":
            dst[key]["httpUrl"] = dst[key].pop("url")
            key = "httpUrl"
        logger.info(f"Added '{key}' to {dst_key}.")

    if dry_run:
        logger.info("Dry run complete.")
    file_utils.write_json(dst, dst_path)
    logger.info(f"Successfully copied {keys} into '{dst}' of {dst_path}")


def create_load_parser(
    mcp_parser: argparse.ArgumentParser, argv: list[str]
) -> argparse.Namespace:
    """Create argparse parser for load command.

    Args:
        mcp_parser: Parent parser for load command.
        argv: Command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    load_parser = argparse.ArgumentParser(
        description="Copy MCP servers from source JSON to config file.",
        prog="load",
        parents=[mcp_parser],
    )

    load_parser.add_argument(
        "src",
        type=Path,
        help="Path to master MCP Servers file.",
        metavar="/PATH/TO/SOURCE.JSON",
    )

    load_parser.add_argument(
        "servers",
        nargs="+",
        help="Servers to copy from source file.",
        metavar="SERVER1 SERVER2 SERVER3",
    )

    return load_parser.parse_args(argv)


def main(argv=None):
    """Copy MCP servers from source JSON to config file."""
    if not argv:
        argv = sys.argv
    mcp_parser = create_parent_parser()
    args = create_load_parser(mcp_parser, argv)

    load_keys(args.src, args.config, args.servers, args.dry_run)


if __name__ == "__main__":
    main()

    sys.exit(0)
