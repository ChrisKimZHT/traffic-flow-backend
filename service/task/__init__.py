from fastapi import APIRouter

from .list import list_router
from .log import log_router
from .run_face_detection import run_face_detection_router
from .run_plate_detection import run_plate_detection_router
from .run_statistic import run_statistic_router

task_router = APIRouter()

task_router.include_router(list_router)
task_router.include_router(run_statistic_router)
task_router.include_router(log_router)
task_router.include_router(run_plate_detection_router)
task_router.include_router(run_face_detection_router)
