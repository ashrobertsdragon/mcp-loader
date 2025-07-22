import json
import sys
from pathlib import Path
from typing import Any

from _logger import logger


def read_json(path: Path, encoding: str = "utf-8") -> dict[str, Any]:
    """Reads a JSON file from the specified path and returns its contents.

    This function loads and parses a JSON file, returning the resulting data
    structure.

    Args:
        path (Path): The path to the JSON file.
        encoding (str): The encoding to use when reading the file. Defaults
            to "utf-8".

    Returns:
        The parsed JSON data as a dictionary.

    Raises:
        SystemExit: If the file cannot be read due to an OSError or JSON
            encoding error.
    """
    try:
        with path.open("r", encoding=encoding) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logger.error(f"Unable to read {path}: {e}")
        sys.exit(1)


def write_json(
    data: dict[str, Any], path: Path, encoding: str = "utf-8"
) -> None:
    """Writes data to a JSON file at the specified path.

    This function serializes the given data as JSON and writes it to the
    specified file path.

    Args:
        path (Path): he path to the JSON file.
        data (dict): The data to write to the file, as a dictionary or list.
        encoding (str): The encoding to use when writing the file. Defaults
            to "utf-8".

    Raises:
        SystemExit: If the file cannot be written due to an OSError or JSON
            encoding error.
    """

    try:
        with path.open("w", encoding=encoding) as f:
            json.dump(data, f, indent=4)
    except (OSError, json.JSONDecodeError) as e:
        logger.error(f"Unable to write {path}: {e}")
        sys.exit(1)
