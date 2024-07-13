import json
import os

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import config
from crud.VideoCrud import VideoCrud
from util.get_db import get_db

result_stat_router = APIRouter()


@result_stat_router.get("/resultStat")
async def _(videoId: int, db: Session = Depends(get_db)):
    try:
        video = VideoCrud.get_by_id(db, videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if not video:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video Not Found"})

    stat_json_path = os.path.join(video.stat_res_path, config.yolov5_deepsort_result_json)

    try:
        with open(stat_json_path, "r") as f:
            stat = json.load(f)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Read File Error: {e}"})

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK", "data": stat})
