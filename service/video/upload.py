import time
import uuid

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.VideoCrud import VideoCrud
from util.get_db import get_db

upload_router = APIRouter()


@upload_router.post("/upload")
async def _(file: UploadFile, db: Session = Depends(get_db)):
    if not file.filename:
        return JSONResponse(status_code=400, content={"status": 1, "message": "No File Uploaded"})

    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{file_ext}"
    video = await file.read()

    try:
        with open(f"./runs/video/{filename}", "wb") as f:
            f.write(video)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Write File Error: {e}"})

    title = "未命名视频"
    description = "无描述"
    file_size = len(video)
    upload_time = int(time.time())

    try:
        video = VideoCrud.create(db, title, description, filename, file_size, upload_time)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK", "videoId": video.video_id})
