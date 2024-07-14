from fastapi import APIRouter

from .search_all import search_all_router

face_router = APIRouter()

face_router.include_router(search_all_router)
