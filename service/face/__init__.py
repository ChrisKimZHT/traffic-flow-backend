from fastapi import APIRouter

from .search import search_router
from .search_all import search_all_router

face_router = APIRouter()

face_router.include_router(search_all_router)
face_router.include_router(search_router)
