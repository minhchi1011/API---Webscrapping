import os
from fastapi import APIRouter, HTTPException
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from src.services.cleaning import preprocess_iris_dataset
from src.services.data import split_dataset
from src.services.utils import train_classification_model, make_predictions
router = APIRouter()

# Thư mục để lưu dataset
DATA_FOLDER = "src/data"
MODEL_FOLDER = os.path.join("src", "models")
CONFIG_PATH = os.path.join("src", "config", "model_parameters.json")

# Đảm bảo thư mục tồn tại
os.makedirs(DATA_FOLDER, exist_ok=True)

@router.get("/download-dataset", name="Download Iris Dataset")
def download_dataset():
    """
    Load dataset Iris from Kaggle and store at src/data
    """
    try:
        # Set Kaggle API
        api = KaggleApi()
        api.authenticate()

        # Dataset Kaggle (url: https://www.kaggle.com/datasets/uciml/iris)
        dataset_name = "uciml/iris"

        # Download dataset
        api.dataset_download_files(dataset_name, path=DATA_FOLDER, unzip=True)

        # Check file has been download
        file_path = os.path.join(DATA_FOLDER, "Iris.csv")
        if os.path.exists(file_path):
            return {"message": f"Dataset downloaded successfully to {file_path}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to download the dataset")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/load-dataset", name="Load Iris Dataset")
def load_dataset():
    """
    Load the Iris dataset from the src/data folder and return it as JSON.
    """
    try:
        # Path to the dataset file
        file_path = os.path.join(DATA_FOLDER, "Iris.csv")

        # Check if the file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Dataset file not found. Please download it first.")

        # Load the dataset using pandas
        df = pd.read_csv(file_path)

        # Convert DataFrame to JSON
        return df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/process-dataset", name="Process Iris Dataset")
def process_dataset():
    """
    Process the Iris dataset for model training. This includes encoding categorical variables,
    handling missing values, and any other preprocessing steps.
    """
    try:
        # Path to the dataset file
        file_path = os.path.join(DATA_FOLDER, "Iris.csv")

        # Check if the file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Dataset file not found. Please download it first.")

        # Call the preprocessing function
        processed_file_path = preprocess_iris_dataset(file_path, DATA_FOLDER)

        return {"message": f"Dataset processed successfully. Processed file saved to {processed_file_path}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/split-dataset", name="Split Iris Dataset")
def split_iris_dataset():
    """
    Split the processed Iris dataset into training and testing sets and return them as JSON.
    """
    try:
        # Path to the processed dataset file
        processed_file_path = os.path.join(DATA_FOLDER, "Processed_Iris.csv")

        # Check if the file exists
        if not os.path.exists(processed_file_path):
            raise HTTPException(status_code=404, detail="Processed dataset file not found. Please process it first.")

        # Call the split function
        split_data = split_dataset(processed_file_path)
        print("Test data:", split_data["test"])
        return split_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/train-model", name="Train Classification Model")
def train_model():
    """
    Train a classification model on the training dataset and save the model.
    """
    try:
        # Path to the processed dataset file
        processed_file_path = os.path.join(DATA_FOLDER, "Processed_Iris.csv")

        # Path to save the model
        model_save_path = os.path.join(MODEL_FOLDER, "classification_model.pkl")

        # Check if the file exists
        if not os.path.exists(processed_file_path):
            raise HTTPException(status_code=404, detail="Processed dataset file not found. Please process it first.")

        # Load the split dataset
        split_data = split_dataset(processed_file_path)
        train_data = split_data["train"]

        # Train the model
        saved_model_path = train_classification_model(train_data, model_save_path, CONFIG_PATH)

        return {"message": f"Model trained and saved successfully to {saved_model_path}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict", name="Make Predictions")
def predict(input_data: list):
    """
    Make predictions using the trained classification model.

    Args:
        input_data (list): Input data for prediction.

    Returns:
        JSON: Predictions made by the model.
    """
    try:
        # Path to the saved model and processed dataset
        model_path = os.path.join(MODEL_FOLDER, "classification_model.pkl")
        processed_file_path = os.path.join(DATA_FOLDER, "Processed_Iris.csv")

        # Check if the model exists
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model file not found. Please train the model first.")

        # Load test set if input_data is not provided
        if input_data is None:
            # Ensure the processed dataset exists
            if not os.path.exists(processed_file_path):
                raise HTTPException(status_code=404, detail="Processed dataset file not found. Please process it first.")

            # Load the split dataset and use the test set
            split_data = split_dataset(processed_file_path)
            input_data = split_data["test"]

        # Make predictions
        predictions = make_predictions(model_path, input_data)

        return {"test_data": input_data, "predictions": predictions}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



