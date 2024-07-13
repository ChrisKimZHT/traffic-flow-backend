from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.VideoCrud import VideoCrud
from util.get_db import get_db

get_info_router = APIRouter()


@get_info_router.get("/getInfo")
async def _(videoId: int, db: Session = Depends(get_db)):
    try:
        video = VideoCrud.get_by_id(db, videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if video is None:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video not found"})

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK", "data": {
        "videoId": video.video_id,
        "title": video.title,
        "description": video.description,
        "fileName": video.file_name,
        "fileSize": video.file_size,
        "uploadTime": video.upload_time,
        "statProcessed": video.stat_processed,
        "plateProcessed": video.plate_processed,
        "faceProcessed": video.face_processed,
    }})
