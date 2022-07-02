import logging
import sys

logger = logging.getLogger("pinata")
logger.addHandler(logging.StreamHandler(sys.stderr))


__all__ = ["logger"]
