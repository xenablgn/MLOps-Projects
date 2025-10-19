import os

import pandas as pd
import joblib
from scipy.stats import randint
from sklearn.metrics import (
    f1_score,
    accuracy_score,
    recall_score,
    precision_score,
)
from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBClassifier

import mlflow
import mlflow.sklearn

from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_fucntions import load_data, read_yaml_file

logger = get_logger(__name__)


class ModelTraining:
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        if not os.path.exists(os.path.dirname(self.model_output_path)):
            os.makedirs(os.path.dirname(self.model_output_path))

        self.params_distribution = XGBOOST_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_split_data(self):
        """Load training and testing data."""
        try:
            logger.info("Loading training and testing data")
            self.train_df = load_data(self.train_path)
            self.test_df = load_data(self.test_path)

            logger.info("Splitting features and target variable")
            X_train = self.train_df.drop("booking_status", axis=1)
            y_train = self.train_df["booking_status"]

            X_test = self.test_df.drop("booking_status", axis=1)
            y_test = self.test_df["booking_status"]

            return X_train, y_train, X_test, y_test

        except Exception as e:
            logger.error("Error loading & splitting data: %s", str(e))
            raise CustomException("Error loading & splitting data", e)

    def train_model(self, X_train, y_train):
        """Train XGBoost model with RandomizedSearchCV."""
        try:
            logger.info("Starting model training with RandomizedSearchCV")
            xgb = XGBClassifier(
                objective="binary:logistic",
                eval_metric="logloss",
                use_label_encoder=False
            )
            logger.info("XGBoost Classifier instance created")
            logger.info("RandomizedSearchCV parameters: %s", self.random_search_params)
            rand_search = RandomizedSearchCV(
                estimator=xgb,
                param_distributions=self.params_distribution,
                n_iter=self.random_search_params["n_iter"],
                scoring=self.random_search_params["scoring"],
                cv=self.random_search_params["cv"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                n_jobs=self.random_search_params["n_jobs"],
            )
            logger.info("Fitting RandomizedSearchCV")
            rand_search.fit(X_train, y_train)
            logger.info("Hyperparameter Tuning completed")

            best_params = rand_search.best_params_
            best_xgb_model = rand_search.best_estimator_

            logger.info("Best Hyperparameters: %s", best_params)

            return best_xgb_model
        except Exception as e:
            logger.error("Error during model training: %s", str(e))
            raise CustomException("Error during model training", e)

    def evaluate_model(self, model, X_test, y_test):
        """Evaluate the trained model on test data."""
        try:
            logger.info("Evaluating the trained model")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(
                "Model Evaluation Metrics: Accuracy: %.4f, Precision: %.4f, Recall: %.4f, F1 Score: %.4f",
                accuracy, precision, recall, f1,
            )

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
            }
        except Exception as e:
            logger.error("Error during model evaluation: %s", str(e))
            raise CustomException("Error during model evaluation", e)

    def save_model(self, model):
        """Save the trained model to disk."""
        try:
            logger.info("Saving the trained model to %s", self.model_output_path)
            joblib.dump(model, self.model_output_path)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error("Error saving the model: %s", str(e))
            raise CustomException("Error saving the model", e)

    def run(self):
        """Run the full model training pipeline."""
        try:
            with mlflow.start_run():
                logger.info("Starting model training pipeline")
                logger.info("MLflow run ID started")

                logger.info("Logging datasets as MLflow artifacts")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_split_data()
                best_model = self.train_model(X_train, y_train)
                metrics = self.evaluate_model(best_model, X_test, y_test)
                self.save_model(best_model)

                logger.info("Logging model to MLflow")
                mlflow.log_artifact(self.model_output_path, artifact_path="model")

                logger.info("Model training pipeline completed successfully")

                logger.info("Logging model parameters and metrics to MLflow")
                mlflow.log_params(best_model.get_params())
                mlflow.log_metrics(metrics)

        except Exception as e:
            logger.error("Error in model training pipeline: %s", str(e))
            raise CustomException("Error in model training pipeline", e)


if __name__ == "__main__":
    model_trainer = ModelTraining(
        train_path=PROCESSED_TRAIN_FILE_PATH,
        test_path=PROCESSED_TEST_FILE_PATH,
        model_output_path=os.path.join(MODEL_OUTPUT_DIR, "xgboost_model.joblib"),
    )
    model_trainer.run()