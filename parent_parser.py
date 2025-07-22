import argparse
from pathlib import Path

from _logger import set_log_level


class LoggerAction(argparse.Action):
    """Custom action to set logging level based on verbosity count."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Set logging level based on verbosity count."""
        count = getattr(namespace, self.dest, 0)
        if values is not None:
            count = len(values)
        setattr(namespace, self.dest, count)
        verbosity = {0: "ERROR", 1: "WARNING", 2: "INFO"}

        level = verbosity.get(min(count, max(verbosity)), "INFO")
        set_log_level(level)


def create_parent_parser() -> argparse.ArgumentParser:
    """Create parent parser for all commands.

    Returns:
        argparse.ArgumentParser: Parent parser.
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "config",
        type=Path,
        help="Path to destination file.",
        metavar="/PATH/TO/CLAUDE_DESKTOP_CONFIG.JSON",
    )

    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Run in dry-run mode to preview changes",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action=LoggerAction,
        default=0,
        help="Set logging level",
    )

    return parser
