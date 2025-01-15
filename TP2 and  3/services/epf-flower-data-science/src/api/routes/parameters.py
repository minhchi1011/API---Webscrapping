from fastapi import APIRouter, HTTPException
from google.cloud import firestore
from src.services.parameters import create_firestore_parameters, update_or_add_parameters

# Initialize the router
router = APIRouter()

@router.post("/create-parameters", name="Create Firestore Parameters")
def create_parameters():
    """
    Create the Firestore collection 'parameters' and add the document 'parameters'.
    """
    try:
        # Call the service function to create Firestore parameters
        result = create_firestore_parameters()

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/retrieve-parameters", name="Retrieve Firestore Parameters")
def retrieve_parameters():
    """
    Retrieve the parameters from the Firestore collection 'parameters'.
    """
    try:
        # Initialize Firestore client
        db = firestore.Client()

        # Fetch the document from Firestore
        collection_name = "parameters"
        document_name = "parameters"
        doc_ref = db.collection(collection_name).document(document_name)
        doc = doc_ref.get()

        if doc.exists:
            return {"parameters": doc.to_dict()}
        else:
            raise HTTPException(status_code=404, detail=f"Document '{document_name}' not found in collection '{collection_name}'.")

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/update-parameters", name="Update or Add Firestore Parameters")
def update_parameters(parameters: dict):
    """
    Endpoint để cập nhật hoặc thêm các tham số vào Firestore.
    """
    try:
        result = update_or_add_parameters(parameters)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))