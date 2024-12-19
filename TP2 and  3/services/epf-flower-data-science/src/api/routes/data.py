import os
from fastapi import APIRouter, HTTPException
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

router = APIRouter()

# Thư mục để lưu dataset
DATA_FOLDER = "src/data"

# Đảm bảo thư mục tồn tại
os.makedirs(DATA_FOLDER, exist_ok=True)

@router.get("/download-dataset", name="Download Iris Dataset")
def download_dataset():
    """
    Download dataset Iris from Kaggle and store at src/data
    """
    try:
        # Thiết lập Kaggle API
        api = KaggleApi()
        api.authenticate()

        # Dataset Kaggle (url: https://www.kaggle.com/datasets/uciml/iris)
        dataset_name = "uciml/iris"

        # Tải xuống dataset
        api.dataset_download_files(dataset_name, path=DATA_FOLDER, unzip=True)

        # Kiểm tra file đã được tải xuống
        file_path = os.path.join(DATA_FOLDER, "Iris.csv")
        if os.path.exists(file_path):
            return {"message": f"Dataset downloaded successfully to {file_path}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to download the dataset")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
