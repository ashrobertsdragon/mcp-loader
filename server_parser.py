import argparse
from typing import Any

from _logger import logger


def split_eq(arg_list: list[str]) -> dict[str, str]:
    """Split a list of key=value arguments into a dictionary.

    Args:
        arg_list (list[str]): List of key=value arguments.

    Returns:
        dict[str, str]: Dictionary of key: value arguments.
    """
    return {arg.split("=", 1)[0]: arg.split("=", 1)[1] for arg in arg_list}


def create_server_parser() -> argparse.ArgumentParser:
    """Create an argparse parser for a single server.

    Returns:
        argparse.ArgumentParser: Parser for a single server.
    """
    server_parser = argparse.ArgumentParser(
        add_help=False,
        exit_on_error=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    server_parser.add_argument("--server", required=True)

    run_group = server_parser.add_mutually_exclusive_group(required=True)
    run_group.add_argument(
        "--command", help="Command to interpreter to run server"
    )
    run_group.add_argument(
        "--url",
        "--http-url",
        help="URL to connect to remote server",
        dest="url",
    )

    server_parser.add_argument(
        "--type", choices=["stdio", "sse", "http"], help="Server transport type"
    )
    server_parser.add_argument(
        "--args", nargs="+", help="Arguments to pass to command/url"
    )
    server_parser.add_argument(
        "--headers", nargs="+", help="Http headers in key=value format"
    )
    server_parser.add_argument(
        "--env",
        nargs="*",
        help="Environment variables in key=value format",
    )
    server_parser.add_argument(
        "--cwd", help="Working directory to run server in"
    )

    server_parser.add_argument(
        "--timeout", type=int, help="Timeout in seconds"
    )
    server_parser.add_argument(
        "--disabled", action="boolean", help="Server set to disabled"
    )
    server_parser.add_argument(
        "--auto-approve", nargs="+", help="Tools to auto approve"
    )

    return server_parser


def _parse_server_group(group: list[str]) -> tuple[str, dict[str, Any]]:
    """Parse a single server group using argparse.

    Args:
        group (list[str]): List of arguments to parse.

    Returns:
        tuple[str, dict[str, Any]]: Tuple containing the server name and args.
    """
    parser = create_server_parser()
    server = parser.parse_args(group)

    env_dict = split_eq(server.env)
    headers_dict = split_eq(server.headers)

    configs = {
        "command": server.command,
        "httpURL": server.url,
        "args": server.args,
        "env": env_dict,
        "cwd": server.cwd,
        "type": server.type,
        "headers": headers_dict,
        "timeout": server.timeout,
        "disabled": server.disabled,
        "autoApprove": server.auto_approve,
    }

    return server.server, {k: v for k, v in configs.items() if v is not None}


def _split_by_server(args: list[str]) -> list[list[str]]:
    """Split the argument list into groups starting with --server.

    Args:
        args (list[str]): List of arguments to split.

    Returns:
        list[list[str]]: List of groups, where each group is a list of arguments.
    """
    groups = []
    current_group = []

    i = 0
    while i < len(args):
        if args[i] == "--server":
            if current_group:
                groups.append(current_group)
                current_group = []

            if i + 1 >= len(args):
                raise ValueError("--server requires a value")
            current_group = [args[i], args[i + 1]]
            i += 2
        else:
            current_group.append(args[i])
            i += 1

    if current_group:
        groups.append(current_group)

    return groups


def parse(args: list[str]) -> dict[str, dict[str, Any]]:
    """
    Parse command line arguments into groups by server.
    Each group is then parsed by its own argparse instance.
    """
    groups = _split_by_server(args)

    servers: dict[str, dict[str, Any]] = {}
    for group in groups:
        try:
            server, config = _parse_server_group(group)
            servers[server] = config
        except SystemExit:
            logger.error(
                f"Error parsing arguments for a server group: {' '.join(group)}"
            )
            continue

    return servers

