from fastapi import APIRouter

from .get_image import get_image_router
from .search import search_router

plate_router = APIRouter()

plate_router.include_router(search_router)
plate_router.include_router(get_image_router)
