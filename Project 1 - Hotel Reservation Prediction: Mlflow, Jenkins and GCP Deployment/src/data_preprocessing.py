import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_fucntions import load_data, read_yaml_file
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    """Class for processing hotel reservation data."""

    def __init__(self, train_path: str, test_path: str, processed_dir: str, config_path: str) -> None:
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml_file(config_path)
        self.le = LabelEncoder()
        self.scaler = StandardScaler()
        self.smote = SMOTE(random_state=self.config["data_ingestion"]["random_state"])
        
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the input DataFrame by dropping unnecessary columns and duplicates."""
        try:
            logger.info("Starting data cleaning")
            df = df.drop(columns=["Unnamed: 0", "Booking_ID"], errors="ignore")
            df = df.drop_duplicates()
            logger.info("Data cleaning completed. Shape after cleaning: %s", df.shape)
            return df
        except Exception as e:
            logger.error("Error during data cleaning: %s", str(e))
            raise CustomException("Error during data cleaning", e)

    def preprocess_data(self, df: pd.DataFrame, is_train: bool) -> pd.DataFrame:
        """Preprocess data: encode categoricals and scale numericals."""
        try:
            cat_cols = self.config["data_processing"]["categorical_features"]
            num_cols = self.config["data_processing"]["numerical_features"]

            if is_train:
                logger.info("Fitting LabelEncoders for categorical features")
                self.encoders = {}  # store encoders for each categorical column
                for col in cat_cols:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col])
                    self.encoders[col] = le
            else:
                logger.info("Transforming categorical features using fitted encoders")
                for col in cat_cols:
                    le = self.encoders.get(col)
                    if le is None:
                        raise ValueError(f"No encoder found for column: {col}")
                    
                    # Map unseen categories to -1
                    df[col] = df[col].map(lambda s: le.transform([s])[0] if s in le.classes_ else -1)

            # Scale numerical features
            if is_train:
                df[num_cols] = self.scaler.fit_transform(df[num_cols])
            else:
                df[num_cols] = self.scaler.transform(df[num_cols])

            return df

        except Exception as e:
            logger.error("Error during data preprocessing: %s", str(e))
            raise CustomException("Error during data preprocessing", e)

    def balance_data(self, df: pd.DataFrame, is_train: bool) -> pd.DataFrame:
        """Balance training data using SMOTE. Only applies to training set."""
        try:
            logger.info("Starting data balancing using SMOTE")
            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]

            if is_train:
                X_resampled, y_resampled = self.smote.fit_resample(X, y)
                df_balanced = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled, name="booking_status")], axis=1)
            else:
                # SMOTE should NOT be applied to test data
                df_balanced = df.copy()
                logger.warning("SMOTE skipped for test data")

            logger.info("Data balancing completed. Shape: %s", df_balanced.shape)
            return df_balanced
        except Exception as e:
            logger.error("Error during data balancing: %s", str(e))
            raise CustomException("Error during data balancing", e)

    def select_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Select important features using RandomForest feature importance."""
        try:
            logger.info("Starting feature selection using RandomForestClassifier")
            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]

            rf = RandomForestClassifier(random_state=self.config["data_ingestion"]["random_state"])
            rf.fit(X, y)

            feature_importances_df = pd.DataFrame({
                "feature": X.columns,
                "importance": rf.feature_importances_
            })
            top_feature_importance_df = feature_importances_df.sort_values(by="importance", ascending=False)
            number_features = self.config["data_processing"]["no_of_features"]
            top_features = top_feature_importance_df["feature"].head(number_features).values
            top_features_df = df[list(top_features) + ["booking_status"]]

            logger.info("Selected top features: %s", list(top_features))
            return top_features_df
        except Exception as e:
            logger.error("Error during feature selection: %s", str(e))
            raise CustomException("Error during feature selection", e)

    def save_data(self, df: pd.DataFrame, file_path: str) -> None:
        """Save the processed DataFrame to a CSV file."""
        try:
            df.to_csv(file_path, index=False)
            logger.info("Processed data saved to %s", file_path)
        except Exception as e:
            logger.error("Error saving processed data to %s: %s", file_path, str(e))
            raise CustomException("Error saving processed data", e)

    def process(self) -> None:
        """Run the full data processing pipeline."""
        try:
            logger.info("Starting data processing pipeline")

            # Load data
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            # Clean and merge
            train_df = self.clean_data(train_df)
            test_df = self.clean_data(test_df)

            # Preprocess (encode + scale)
            train_df = self.preprocess_data(train_df, is_train=True)
            test_df = self.preprocess_data(test_df, is_train=False)

            # Balance only train data
            train_df = self.balance_data(train_df, is_train=True)

            # Feature selection before preprocessing
            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns.tolist()]            
            
            # Save processed data
            self.save_data(train_df, PROCESSED_TRAIN_FILE_PATH)
            self.save_data(test_df, PROCESSED_TEST_FILE_PATH)

            logger.info("Data processing pipeline completed successfully")

        except Exception as e:
            logger.error("Error in data processing pipeline: %s", str(e))
            raise CustomException("Error in data processing pipeline", e)


if __name__ == "__main__":
    processor = DataProcessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH
    )
    processor.process()
