import os
import sys
from pathlib import Path


from ..exception import CustomException
from ..logger import logging
# These modules are not implemented yet
# from .data_transformation import DataTransformation, DataTransformationConfig
# from .model_trainer import ModelTrainerConfig, ModelTrainer

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Get the project root directory
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
            data_path = os.path.join(project_root, 'notebook', 'data', 'lead_model_data.csv')
            
            if not os.path.exists(data_path):
                raise FileNotFoundError(f"Data file not found at: {data_path}")
            
            # Try different encodings
            encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
            for encoding in encodings:
                try:
                    df = pd.read_csv(data_path, encoding=encoding)
                    logging.info(f'Successfully read the dataset as dataframe using {encoding} encoding')
                    break
                except UnicodeDecodeError:
                    if encoding == encodings[-1]:  # If this was the last encoding to try
                        raise
                    continue

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Inmgestion of the data iss completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    print(f"Data ingestion completed. Train data: {train_data}, Test data: {test_data}")

    # TODO: Implement these modules
    # data_transformation=DataTransformation()
    # train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    # modeltrainer=ModelTrainer()
    # print(modeltrainer.initiate_model_trainer(train_arr,test_arr))