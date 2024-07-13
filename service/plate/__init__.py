from fastapi import APIRouter

from .search import search_router

plate_router = APIRouter()

plate_router.include_router(search_router)
