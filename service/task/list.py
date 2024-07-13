from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.TaskCrud import TaskCrud
from util.get_db import get_db

list_router = APIRouter()


@list_router.get("/list")
async def _(db: Session = Depends(get_db)):
    try:
        tasks = TaskCrud.get_all(db)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    tasks = reversed(tasks)

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK", "data": [{
        "taskId": task.task_id,
        "videoId": task.video_id,
        "description": task.description,
        "startTime": task.start_time,
        "status": task.status,
    } for task in tasks]})
