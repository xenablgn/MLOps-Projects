import logging
import os 
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=LOG_FILE,
    format= "%(asctime)s - %(levelname)s - %(message)s",
    level= logging.INFO,
)

def get_logger(name: str) -> logging.Logger:
    """Function to get a logger instance in different files."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
