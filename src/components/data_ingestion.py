import os
import sys
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import pandas as pd

from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_training import ModelTrainer, ModelTrainerConfig


@dataclass
class DataIngestionConfig:
    raw_data_path: str=os.path.join('artifacts','data.csv')
    train_data_path: str=os.path.join('artifacts','train.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Start data ingestion method and components")

        try: 
            df = pd.read_csv('notebooks/data/amazon.csv')
            logging.info('dataset have been read')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok = True)
            df.to_csv(self.ingestion_config.raw_data_path,index = False, header = True)

            logging.info("making a copy into train dataset")

            df.to_csv(self.ingestion_config.train_data_path, index=False, header = True)

            logging.info("Ingestion of data has been completed")

            return(
                self.ingestion_config.train_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    obj=DataIngestion()
    train_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    aprio_df = data_transformation.initiate_data_transformation(train_data)

    modeltrainer = ModelTrainer()
    modeltrainer.initiate_model_create(aprio_df)