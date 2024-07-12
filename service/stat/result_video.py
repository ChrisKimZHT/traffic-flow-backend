import os

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

from config import config
from crud.VideoCrud import VideoCrud
from util.get_db import get_db

result_video_router = APIRouter()


@result_video_router.get("/resultVideo")
async def _(videoId: int, db: Session = Depends(get_db)):
    try:
        video = VideoCrud.get_video_by_id(db, videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if not video:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video Not Found"})

    res_video_path = os.path.join(video.stat_res_path, config.yolov5_deepsort_result_video)

    return FileResponse(res_video_path)
