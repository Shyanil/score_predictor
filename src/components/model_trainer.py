import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import custom_Exception
from src.logger import logger
from src.utils import evaluateModel, save_obj
from sklearn.metrics import r2_score


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts' , 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_array , test_array):
        try:
            X_train , y_train , X_test , y_test = (
                train_array[:, : -1],
                train_array[:, -1],
                test_array[:, : -1],
                test_array[:, -1]
            )

            models = {
                    "Random Forest": RandomForestRegressor(),
                    "Decision Tree": DecisionTreeRegressor(),
                    "Gradient Boosting": GradientBoostingRegressor(),
                    "Linear Regression": LinearRegression(),
                    "XGBRegressor": XGBRegressor(),
                    "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                    "AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            params = {
            "Decision Tree": {
                "criterion": ["squared_error", "friedman_mse", "absolute_error", "poisson"]
            },

            "Random Forest": {
                "n_estimators": [8, 16, 32, 64, 128, 256]
            },

            "Gradient Boosting": {
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
                "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                "n_estimators": [8, 16, 32, 64, 128, 256]
            },

            "Linear Regression": {},

            "XGBRegressor": {
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
                "n_estimators": [8, 16, 32, 64, 128, 256]
            },

            "CatBoosting Regressor": {
                "depth": [6, 8, 10],
                "learning_rate": [0.01, 0.05, 0.1],
                "iterations": [30, 50, 100]
            },

            "AdaBoost Regressor": {
                "learning_rate": [0.1, 0.01, 0.5, 0.001],
                "n_estimators": [8, 16, 32, 64, 128, 256]
            }
            }

            model_report : dict = evaluateModel(X_train=X_train , y_train=y_train, X_test=X_test, y_test=y_test, models=models, params=params)

            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]


            best_model = models[best_model_name]

            if best_model_score < 0.6 :
                raise custom_Exception("No best Model is found on the given range")
            logger.info(f"Best found model The Model name {best_model_name} and score is {best_model_score} on both training and testing dataset")
            

            save_obj(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted_value = best_model.predict(X_test)
            r2 = r2_score(y_test , predicted_value)
            return r2
        
        except Exception as e:
            raise custom_Exception(e , sys)
