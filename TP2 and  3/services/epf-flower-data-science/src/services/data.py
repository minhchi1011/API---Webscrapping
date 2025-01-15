import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(file_path, test_size=0.2, random_state=42):
    """
    Split the Iris dataset into training and testing sets.

    Args:
        file_path (str): Path to the processed dataset file (CSV format).
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random state for reproducibility.

    Returns:
        dict: A dictionary containing training and testing data as JSON.
    """
    try:
        # Load the processed dataset
        df = pd.read_csv(file_path)

        # Separate features and target
        X = df.drop(columns=['Species'])
        y = df['Species']

        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        # Combine features and target for train and test sets
        train_data = pd.concat([X_train, y_train], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)

        return {
            "train": train_data.to_dict(orient="records"),
            "test": test_data.to_dict(orient="records")
        }

    except Exception as e:
        raise ValueError(f"An error occurred during dataset splitting: {str(e)}")
