import os
import time

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import config
from crud.TaskCrud import TaskCrud
from crud.VideoCrud import VideoCrud
from util.get_db import get_db
from util.run_subprocess import run_subprocess_with_callback

run_statistic_router = APIRouter()


@run_statistic_router.get("/runStatistic")
async def _(videoId: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        video = VideoCrud.get_by_id(db, videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if not video:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video Not Found"})

    file_name = video.file_name
    file_name_no_ext = file_name.split(".")[0]

    cur_work_dir = os.getcwd()
    input_video = os.path.join(cur_work_dir, f"runs/video/{file_name}")
    output_path = os.path.join(cur_work_dir, f"runs/stat/{file_name_no_ext}")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    cmd = (f"cd \"{config.yolov5_deepsort_path}\" && "
           f"\"{config.yolov5_deepsort_interpreter}\" \"{config.yolov5_deepsort_main}\" "
           f"--input_video \"{input_video}\" "
           f"--output_path \"{output_path}\" "
           f"--headless 1 "
           f"--log_file log.txt")

    try:
        task = TaskCrud.create(db, videoId, f"流量分析", int(time.time()), os.path.join(output_path, "log.txt"), 1)
        video.stat_processed = 1
        video.stat_res_path = output_path
        VideoCrud.update(db, video)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    task_id = task.task_id

    def callback(return_value):
        try:
            cb_task = TaskCrud.get_by_id(db, task_id)
            cb_video = VideoCrud.get_by_id(db, videoId)
            if return_value == 0:
                cb_task.status = 2
                TaskCrud.update(db, cb_task)
            else:
                cb_task.status = 3
                TaskCrud.update(db, cb_task)
            cb_video.stat_processed = 2
            VideoCrud.update(db, cb_video)
        except Exception as err:
            print(f"Database Error: {err}")

    background_tasks.add_task(run_subprocess_with_callback, cmd, callback)

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK", "taskId": task.task_id})
