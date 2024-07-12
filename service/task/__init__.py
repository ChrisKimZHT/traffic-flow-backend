from fastapi import APIRouter

from .list import list_router

task_router = APIRouter()

task_router.include_router(list_router)
