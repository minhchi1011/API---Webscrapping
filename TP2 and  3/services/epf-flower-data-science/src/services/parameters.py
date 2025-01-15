from google.cloud import firestore

def create_firestore_parameters():
    """
    Tạo bộ sưu tập Firestore 'parameters' và thêm tài liệu 'parameters'.
    """
    try:
        # Kết nối với Firestore
        db = firestore.Client()

        # Tên bộ sưu tập và tài liệu
        collection_name = "parameters"
        document_name = "parameters"

        # Dữ liệu cần lưu
        parameters_data = {
            "n_estimators": 100,  # Giá trị ví dụ
            "criterion": "gini"  # Giá trị ví dụ
        }

        # Thêm tài liệu vào bộ sưu tập
        db.collection(collection_name).document(document_name).set(parameters_data)

        return {"message": f"Tài liệu '{document_name}' đã được tạo trong bộ sưu tập '{collection_name}' với dữ liệu {parameters_data}"}

    except Exception as e:
        return {"error": str(e)}
def update_or_add_parameters(parameters: dict):
    """
    Cập nhật hoặc thêm các tham số trong Firestore.
    :param parameters: Dictionary chứa các tham số để cập nhật hoặc thêm.
    """
    try:
        # Kết nối Firestore
        db = firestore.Client()

        # Tham chiếu đến collection 'parameters' và document 'parameters'
        collection_name = "parameters"
        document_name = "parameters"

        # Cập nhật hoặc thêm document
        doc_ref = db.collection(collection_name).document(document_name)
        doc_ref.set(parameters, merge=True)  # `merge=True` giữ nguyên các field hiện có và chỉ cập nhật các field mới

        return {"message": f"Parameters updated/added successfully: {parameters}"}
    except Exception as e:
        return {"error": str(e)}