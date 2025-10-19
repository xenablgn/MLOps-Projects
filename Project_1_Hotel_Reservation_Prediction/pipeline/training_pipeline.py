import os

from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_fucntions import read_yaml_file
from config.paths_config import *


def main():
    """Main function to run the training pipeline."""
    # 1: Data Ingestion
    data_ingestion = DataIngestion(read_yaml_file(CONFIG_PATH))
    data_ingestion.run()

    # 2: Data Processing
    processor = DataProcessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH,
    )
    processor.process()

    # 3: Model Training
    model_trainer = ModelTraining(
        train_path=PROCESSED_TRAIN_FILE_PATH,
        test_path=PROCESSED_TEST_FILE_PATH,
        model_output_path=os.path.join(MODEL_OUTPUT_DIR, "xgboost_model.joblib"),
    )
    model_trainer.run()


if __name__ == "__main__":
    main()