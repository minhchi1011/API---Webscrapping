from google.cloud import firestore

def test_firestore_connection():
    try:
        db = firestore.Client()
        print("Firestore connected successfully!")
    except Exception as e:
        print(f"Error connecting to Firestore: {e}")

import os

file_path = "E:\\CAY\\cogent-treat-447010-v7-9fbabd4002ea.json"

if os.path.exists(file_path):
    print("Tệp JSON tồn tại:", file_path)
else:
    print("Tệp JSON không tồn tại:", file_path)

test_firestore_connection()

