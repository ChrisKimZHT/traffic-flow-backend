from fastapi import APIRouter

from .list import list_router
from .upload import upload_router

video_router = APIRouter()

video_router.include_router(upload_router)
video_router.include_router(list_router)
