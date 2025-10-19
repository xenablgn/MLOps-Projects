import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_fucntions import read_yaml_file

logger = get_logger(__name__)

class DataIngestion:
    """Class for ingesting data from GCS and splitting into train/test sets."""

    def __init__(self, config) -> None:
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]
        self.random_state = self.config["random_state"]

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(
            "DataIngestion instance created with: %s and file is %s",
            self.bucket_name,
            self.bucket_file_name,
        )

    def download_data(self) -> None:
        """Download data from GCS bucket."""
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(
                "Data downloaded from GCS bucket to path: %s", RAW_FILE_PATH
            )
        except Exception as e:
            logger.error("Error downloading data from GCS bucket: %s", str(e))
            raise CustomException("Error downloading data from GCS bucket", e)

    def split_data(self) -> None:
        """Split data into train and test sets."""
        try:
            df = pd.read_csv(RAW_FILE_PATH)
            train_df, test_df = train_test_split(
                df,
                train_size=self.train_ratio,
                test_size=1 - self.train_ratio,
                random_state=self.random_state,
            )
            train_df.to_csv(TRAIN_FILE_PATH, index=False)
            test_df.to_csv(TEST_FILE_PATH, index=False)
            logger.info(
                "Data split into train and test sets at %s and %s",
                TRAIN_FILE_PATH,
                TEST_FILE_PATH,
            )
        except Exception as e:
            logger.error("Error splitting data into train and test sets: %s", str(e))
            raise CustomException("Error splitting data into train and test sets", str(e))

    def run(self) -> None:
        """Run the data ingestion process."""
        try:
            logger.info("Starting data ingestion process")
            self.download_data()
            self.split_data()
            logger.info("Data ingestion process completed successfully")
        except Exception as ce:
            logger.error("Error occurred during data ingestion process: %s", str(ce))
        finally:
            logger.info("Data Ingestion process finished.")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml_file(CONFIG_PATH))
    data_ingestion.run()


