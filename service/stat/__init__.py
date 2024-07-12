from fastapi import APIRouter

from .result_plot import result_plot_router
from .result_stat import result_stat_router
from .result_video import result_video_router

stat_router = APIRouter()

stat_router.include_router(result_stat_router)
stat_router.include_router(result_video_router)
stat_router.include_router(result_plot_router)
