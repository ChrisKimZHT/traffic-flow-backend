from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from crud.VideoCrud import VideoCrud
from util.get_db import get_db

update_info_router = APIRouter()


class BodySchema(BaseModel):
    videoId: int
    title: str
    description: str


@update_info_router.post("/updateInfo")
async def _(body: BodySchema, db: Session = Depends(get_db)):
    try:
        video = VideoCrud.get_by_id(db, body.videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if video is None:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video not found"})

    video.title = body.title
    video.description = body.description

    try:
        VideoCrud.update(db, video)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK"})
