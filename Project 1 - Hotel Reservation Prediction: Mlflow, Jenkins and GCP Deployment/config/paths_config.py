import os

CONFIG_PATH = "config/config.yaml"

# Data Ingestion Paths:
RAW_DIR = "artifacts/raw_data"
RAW_FILE_PATH = os.path.join(RAW_DIR, "Hotel_Reservations_raw.csv")
TRAIN_FILE_PATH= os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

# Data processing
PROCESSED_DIR = "artifacts/processed_data"
PROCESSED_TRAIN_FILE_PATH = os.path.join(PROCESSED_DIR, "Hotel_Reservations_train_processed_data.csv")
PROCESSED_TEST_FILE_PATH = os.path.join(PROCESSED_DIR, "Hotel_Reservations_test_processed_data.csv")

# Model Training
MODEL_OUTPUT_DIR = "artifacts/models/xgboost"
