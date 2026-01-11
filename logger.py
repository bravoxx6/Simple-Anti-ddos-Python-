import logging
from config import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s - %(message)s"
)

def log_attack(message):
    logging.warning(message)
