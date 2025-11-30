import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from src.logger import logger
from src.exception import custom_Exception

@dataclass
class DataTransformationConfig:
    preprocessor_obj_path = os.path.join('artifacts' , 'preprocessor.pkl')

class DataTransform:
    def __init__(self):
        self.data_transform_config = DataTransformationConfig()
    
    def get_data_transformer_obj(self):
        """
        This function is responsible for creating the data transformation pipeline.
        It logs every important step for clear debugging and traceability.

        """
        try:
            logger.info("Initializing Data Transformation process")
            numerical_features = ["reading_score" , "writing_score"]
            categorical_feature = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            logger.info(f"Numerical columns identified: {numerical_features}")
            logger.info(f"Categorical columns identified: {categorical_feature}")

            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer" , SimpleImputer(strategy="median")),
                    ("scaler" , StandardScaler())
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer" , SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder" , OneHotEncoder()),
                    ("scaler" , StandardScaler())
                ]
            )
            logger.info("Combining numerical and categorical pipelines using ColumnTransformer")


            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline" , numerical_pipeline , numerical_features),
                    ("categorical_pipeline" , categorical_pipeline , categorical_feature)
                ]
            )
            logger.info("Data Transformation object (preprocessor) created successfully")
            return preprocessor
        except Exception as e:
            raise custom_Exception(e , sys)
    
    def initiate_data_transformation(self , train_path , test_path):
        try:
            logger.info(f"Loading training data from: {train_path}")
            train_df = pd.read_csv(train_path)
            logger.info(f"Loading testing data from: {test_path}")
            test_df = pd.read_csv(test_path)

            logger.info("Successfully read both train and test datasets.")
            logger.info(f"Train Data Shape: {train_df.shape}")
            logger.info(f"Test Data Shape: {test_df.shape}")

            logger.info("Obtaining preprocessing object...")
            preprocessing_obj = self.get_data_transformer_obj()

            target_column = ["math_score"]
            numerical_features = ["reading_score" , "writing_score"]

            logger.info(f"Target column identified: {target_column}")
            logger.info(f"Numerical columns identified: {numerical_features}")

            input_feature_train_df = train_df.drop(columns=[target_column] , axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column] , axis=1)
            target_feature_test_df = test_df[target_column]

            logger.info(f"Training Input Shape: {input_feature_train_df.shape}")
            logger.info(f"Training Target Shape: {target_feature_train_df.shape}")
            logger.info(f"Testing Input Shape: {input_feature_test_df.shape}")
            logger.info(f"Testing Target Shape: {target_feature_test_df.shape}")

            logger.info("Applying preprocessing pipeline on training data (fit_transform).")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            
            logger.info("Applying preprocessing pipeline on testing data (transform only).")
            input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)


        except Exception as e:
            raise custom_Exception(e , sys)

