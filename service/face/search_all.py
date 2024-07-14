import os

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import config
from crud.VideoCrud import VideoCrud
from util.get_db import get_db

search_all_router = APIRouter()


@search_all_router.get("/searchAll")
async def _(videoId: int, db: Session = Depends(get_db)):
    try:
        video = VideoCrud.get_by_id(db, videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if not video:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video Not Found"})

    if video.face_processed != 2:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Face Not Processed"})

    result_path = video.face_res_path
    result_face_id = os.path.join(result_path, config.face_detection_face_id)

    with open(result_face_id, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []

    for line in lines:
        face_id, person_id, frame_id, x1, y1, x2, y2 = map(int, line.strip().split(','))
        data.append({
            "face_id": face_id,
            "person_id": person_id,
            "frame_id": frame_id,
            "box": [x1, y1, x2, y2]
        })

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK", "data": data})
