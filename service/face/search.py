import os
import uuid

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import config
from crud.VideoCrud import VideoCrud
from util.get_db import get_db
from util.run_subprocess import run_subprocess

search_router = APIRouter()


@search_router.post("/search")
async def _(file: UploadFile, videoId: int, db: Session = Depends(get_db)):
    try:
        video = VideoCrud.get_by_id(db, videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if not video:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video Not Found"})

    if video.face_processed != 2:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Face Not Processed"})

    result_path = video.face_res_path

    file_ext = file.filename.split(".")[-1]
    video = await file.read()

    cur_work_dir = os.getcwd()
    run_id = uuid.uuid4().hex

    file_path = os.path.join(cur_work_dir, f"runs/face/{run_id}")
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    try:
        with open(os.path.join(file_path, f"img.{file_ext}"), "wb") as f:
            f.write(video)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Write File Error: {e}"})

    output_path = os.path.join(cur_work_dir, file_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    cmd = (f"cd \"{config.face_detection_path}\" && "
           f"\"{config.face_detection_interpreter}\" \"{config.face_detection_pred}\" "
           f"--predict_img_path \"{file_path}/img.{file_ext}\" "
           f"--input_path \"{result_path}\" "
           f"--output_path \"{output_path}\" "
           f"--log_file log.txt")

    run_subprocess(cmd)

    result_list = os.listdir(output_path)
    result_list = list(filter(lambda x: x != "log.txt" and not x.startswith("img"), result_list))
    result_list = list(map(lambda x: os.path.join(run_id, x), result_list))

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK", "data": result_list})
