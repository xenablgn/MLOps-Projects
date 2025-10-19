
import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml_file(file_path: str) -> dict:
    """Read a YAML file and return its contents as a dictionary."""
    try:
        if not os.path.exists(file_path):
            raise CustomException(f"Conf YAML file not found at path: {file_path}")
        with open(file_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(
                "YAML file loaded successfully from %s", file_path
            )
            return config
    except Exception as e:
        logger.error(
            "Error reading YAML file at %s: %s", file_path, str(e)
        )
        raise CustomException("Failed to read YAML file", e)

def load_data(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    try:
        logger.info("Loading data from %s", file_path)
        if not os.path.exists(file_path):
            logger.error("Data file not found at path: %s", file_path)
            raise CustomException(f"Data file not found at path: {file_path}")
        df = pd.read_csv(file_path)
        logger.info(
            "Data loaded successfully from %s, shape: %s", file_path, df.shape
        )
        return df
    except Exception as e:
        logger.error("Error loading data from %s: %s", file_path, str(e))
        raise CustomException("Failed to load data", e)
