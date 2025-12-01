import os
import sys
from src.exception import custom_Exception
from src.logger import logger
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import pandas as pd
from src.components.data_transformation import DataTransform , DataTransformationConfig 
from src.utils import save_obj , evaluateModel
from src.components.model_trainer import ModelTrainer , ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    train_data_path : str = os.path.join('artifacts' , 'train.csv')
    test_data_path : str = os.path.join('artifacts' , 'test.csv')
    raw_data_path : str = os.path.join('artifacts' , 'data.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logger.info("Starting data ingestion process...")
        try:
            logger.info("Loading dataset from 'notebook/data/stud.csv'...")
            df = pd.read_csv('notebook/data/stud.csv')
            logger.info("Dataset successfully loaded. Shape: %s", df.shape)
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path) , exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path , index=False, header=True)
            train_set , test_set = train_test_split(df, test_size=0.2, random_state=42)
            logger.info("Successfully split the dataset into training and testing sets.")
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            logger.info(f"Training dataset saved to {self.ingestion_config.train_data_path}")
            test_set.to_csv(self.ingestion_config.test_data_path , index=False , header=True)
            logger.info(f"Testing dataset saved to {self.ingestion_config.test_data_path}")
            logger.info("Data ingestion process completed successfully.")
            return (
                self.ingestion_config.test_data_path,
                self.ingestion_config.train_data_path
            )
        except Exception as e:
            raise custom_Exception(e , sys)
        

if __name__ == '__main__':
    obj = DataIngestion()
    train_data , test_data = obj.initiate_data_ingestion()
    data_transformation = DataTransform()
    train_arr , test_arr ,_ = data_transformation.initiate_data_transformation(train_path=train_data ,test_path=test_data)
    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_array=train_arr , test_array=test_arr))


