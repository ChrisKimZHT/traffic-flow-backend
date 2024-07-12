from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.VideoCrud import VideoCrud
from util.get_db import get_db

list_router = APIRouter()


@list_router.get("/list")
async def _(db: Session = Depends(get_db)):
    try:
        videos = VideoCrud.get_all(db)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK", "data": [{
        "videoId": video.video_id,
        "title": video.title,
        "description": video.description,
        "fileName": video.file_name,
        "fileSize": video.file_size,
        "uploadTime": video.upload_time,
        "statProcessed": video.stat_processed,
        "plateProcessed": video.plate_processed,
        "faceProcessed": video.face_processed,
    } for video in videos]})
