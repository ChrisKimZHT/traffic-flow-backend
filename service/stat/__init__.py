from fastapi import APIRouter

from .result_stat import result_stat_router

stat_router = APIRouter()

stat_router.include_router(result_stat_router)
