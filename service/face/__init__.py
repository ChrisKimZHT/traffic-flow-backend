from fastapi import APIRouter

from .get_image import get_image_router
from .search import search_router
from .search_all import search_all_router

face_router = APIRouter()

face_router.include_router(search_all_router)
face_router.include_router(search_router)
face_router.include_router(get_image_router)
