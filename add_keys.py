import argparse
import sys
from pathlib import Path

import file_utils
from parent_parser import create_parent_parser
from find_key import find_server_dict
from server_parser import create_server_parser, parse
from _logger import logger
from _types import Any


def _print_help(
    add_parser: argparse.ArgumentParser, server_parser: argparse.ArgumentParser
) -> None:
    """Print help message.

    Args:
        add_parser: Parser for add command.
        server_parser: Parser for server groups.
    """
    add_help = add_parser.format_help()

    server_help = server_parser.format_help()
    server_parts = server_help.split("\n\n", 1)
    if len(server_parts) > 1 and server_parts[0].startswith("usage:"):
        server_help = server_parts[1]
    server_help = server_help.strip()

    print(add_help.rstrip())
    print("\nArguments for each --server group:\n")
    print(server_help)


def create_add_parser(
    mcp_parser: argparse.ArgumentParser, argv: list[str]
) -> argparse.Namespace:
    """Create argparse parser for add command.

    Args:
        mcp_parser: Parent parser for add command.
        argv: Command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    add_parser = argparse.ArgumentParser(
        description="Add MCP servers to master MCP Servers file.",
        prog="add",
        parents=[mcp_parser],
        exit_on_error=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    add_parser.add_argument(
        "servers",
        required=True,
        help="One or more server configurations",
        nargs="...",
    )

    args, remaining = add_parser.parse_known_args(argv)
    args.servers = parse(args.servers + remaining)

    return args


def add_keys(
    file: Path, servers: dict[str, dict[str, Any]], dry_run: bool
) -> None:
    """Add MCP servers to master MCP Servers file.

    Args:
        file: Path to master MCP Servers file.
        servers: dictionary of MCP servers to add.
        dry_run: If True, do not write to file.
    """
    master_json = file_utils.read_json(file)
    server_key = find_server_dict(master_json)
    if server_key is not None:
        master_servers = master_json[server_key]
    else:
        master_servers = master_json
        server_key = "top level"

    for server, configs in servers.items():
        master_servers[server] = configs
        logger.info(f"Added '{server}' to {server_key}.")

    if dry_run:
        logger.info("Dry run complete.")
    file_utils.write_json(master_servers, file)
    logger.info(f"Successfully added {servers} into {server_key} in {file}")


def main(argv=None) -> None:
    """Add MCP servers to master MCP Servers file."""
    if not argv:
        argv = sys.argv
    mcp_parser = create_parent_parser()
    args = create_add_parser(mcp_parser, argv)
    if not args or "--help" in args or "-h" in args:
        _print_help(mcp_parser, create_server_parser())
        sys.exit(0)

    add_keys(args.config, args.servers, args.dry_run)


if __name__ == "__main__":
    main()
