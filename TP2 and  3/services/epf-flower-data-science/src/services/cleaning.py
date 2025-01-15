import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder,StandardScaler

def preprocess_iris_dataset(file_path, output_folder):
    """
    Preprocess the Iris dataset by handling missing values and encoding categorical variables.

    Args:
        file_path (str): Path to the input dataset file (CSV format).
        output_folder (str): Folder to save the processed dataset.

    Returns:
        str: Path to the processed dataset file.
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
        df = df.drop(columns=["Id"])


        # Handle missing values (if any)
        if df.isnull().sum().sum() > 0:
            df = df.dropna()

        # Encode categorical variables (e.g., species)
        if 'Species' in df.columns:
            label_encoder = LabelEncoder()
            df['Species'] = label_encoder.fit_transform(df['Species'])
        
        # Scale numerical features
        scaler = StandardScaler()
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

        # Save the processed dataset
        processed_file_path = os.path.join(output_folder, "Processed_Iris.csv")
        df.to_csv(processed_file_path, index=False)

        return processed_file_path

    except Exception as e:
        raise ValueError(f"An error occurred during preprocessing: {str(e)}")
