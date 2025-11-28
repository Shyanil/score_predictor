import os
import sys
from src.exception import custom_Exception
from src.logger import logger
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import pandas as pd

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
        except:
            pass

