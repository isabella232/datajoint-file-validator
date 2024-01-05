import logging
from .config import config

logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO)
logger = logging.getLogger(__name__)
