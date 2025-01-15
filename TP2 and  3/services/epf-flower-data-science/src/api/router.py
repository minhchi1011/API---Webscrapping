"""API Router for Fast API."""
from fastapi import APIRouter

from src.api.routes import hello
from src.api.routes import data
from src.api.routes import parameters
router = APIRouter()

router.include_router(hello.router, tags=["Hello"])
router.include_router(data.router, tags=["Dataset"])
router.include_router(parameters.router, tags=["Firestore"])