import os
import pickle
import json
import pandas as pd
from sklearn.linear_model import LogisticRegression

def train_classification_model(train_data, model_save_path, config_path):
    """
    Train a classification model based on parameters defined in a JSON file.

    Args:
        train_data (dict or DataFrame): Training data containing features and labels.
        model_save_path (str): Path to save the trained model.
        config_path (str): Path to the JSON configuration file.

    Returns:
        str: Path to the saved model file.
    """
    try:
        # Load model parameters from JSON file
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        model_name = config["classification_model"]
        model_params = config["parameters"]

        # Dynamically load the model class
        model_class = getattr(__import__("sklearn.linear_model", fromlist=[model_name]), model_name)

        # Convert train_data to DataFrame if it is a dictionary
        if isinstance(train_data, list):
            train_data = pd.DataFrame(train_data)

        # Separate features and target
        X = train_data.drop(columns=['Species'])
        y = train_data['Species']

        # Initialize the model with parameters
        model = model_class(**model_params)

        # Train the model
        model.fit(X, y)

        # Save the trained model
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        with open(model_save_path, "wb") as model_file:
            pickle.dump(model, model_file)

        return model_save_path

    except Exception as e:
        raise ValueError(f"An error occurred during model training: {str(e)}")



def make_predictions(model_path, input_data):
    """
    Make predictions using the trained model.

    Args:
        model_path (str): Path to the trained model file (pickle format).
        input_data (list or DataFrame): Input data for prediction.

    Returns:
        list: Predictions made by the model.
    """
    try:
        # Load the trained model
        with open(model_path, "rb") as model_file:
            model = pickle.load(model_file)

        # Convert input_data to DataFrame if it is a list
           # Convert input_data to DataFrame if it is a list
        if isinstance(input_data, list):
            input_data = pd.DataFrame(input_data)

        # Get feature columns only
        feature_columns = [col for col in input_data.columns if col != "Species"]
        input_data = input_data[feature_columns]

        # Ensure all columns are numeric
        input_data = input_data.apply(pd.to_numeric, errors="coerce")

        # Drop rows with invalid values
        input_data = input_data.dropna()

        # Make predictions
        predictions = model.predict(input_data)

        return predictions.tolist()

    except Exception as e:
        raise ValueError(f"An error occurred during prediction: {str(e)}")