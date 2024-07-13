import os

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

from crud.VideoCrud import VideoCrud
from util.get_db import get_db

get_video_router = APIRouter()


@get_video_router.get("/getVideo")
async def _(videoId: int, db: Session = Depends(get_db)):
    try:
        video = VideoCrud.get_by_id(db, videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if video is None:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video not found"})

    file_path = os.path.join("runs/video", video.file_name)

    return FileResponse(file_path, media_type="video/mp4")
