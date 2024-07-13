from fastapi import APIRouter

from .list import list_router
from .log import log_router
from .run_statistic import run_statistic_router

task_router = APIRouter()

task_router.include_router(list_router)
task_router.include_router(run_statistic_router)
task_router.include_router(log_router)
