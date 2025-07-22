import logging

__all__ = ["logger", "set_log_level"]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def set_log_level(level):
    logger.setLevel(level)
