import json
import os

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import config
from crud.VideoCrud import VideoCrud
from util.get_db import get_db

search_router = APIRouter()


@search_router.get("/search")
async def _(videoId: int, plate: str, db: Session = Depends(get_db)):
    if videoId is None or plate is None:
        return JSONResponse(status_code=400, content={"status": 1, "message": "Invalid request"})

    try:
        video = VideoCrud.get_by_id(db, videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if video is None:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video not found"})

    result_path = video.plate_res_path
    result_json = os.path.join(result_path, config.hyperlpr3_result_json)

    with open(result_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if plate == "*":
        result = []
        for key, value in data['result'].items():
            for ele in value:
                ele['plate'] = key
                ele['frame_time'] = ele['frame_id'] / data['video_fps']
                result.append(ele)
    else:
        result = data['result'].get(plate, None)
        for ele in result:
            ele['plate'] = plate
        if result is None:
            result = []

    for ele in result:
        del ele['confidence']
        ele['frame_time'] = ele['frame_id'] / data['video_fps']

    return JSONResponse(status_code=200,
                        content={"status": 0, "message": "OK", "result": result, "video": video.file_name})
