import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the data ingestion
from src.Classifier.components.data_ingestion import DataIngestion

if __name__ == "__main__":
    try:
        obj = DataIngestion()
        train_data, test_data = obj.initiate_data_ingestion()
        
        from src.Classifier.components.data_transformation import DataTransformation
        data_transformation = DataTransformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)
        
        from src.Classifier.components.model_trainer import ModelTrainer
        modeltrainer = ModelTrainer()
        print(modeltrainer.initiate_model_trainer(train_arr, test_arr))
        
    except Exception as e:
        print(f"Error: {str(e)}")