from fastapi import APIRouter

from .process_statistic import process_statistic_router
from .upload import upload_router

video_router = APIRouter()

video_router.include_router(upload_router)
video_router.include_router(process_statistic_router)
