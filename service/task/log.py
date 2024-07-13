from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.TaskCrud import TaskCrud
from util.get_db import get_db

log_router = APIRouter()


@log_router.get("/log")
async def _(taskId: int, db: Session = Depends(get_db)):
    try:
        task = TaskCrud.get_by_id(db, taskId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if task is None:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Task not found"})

    output_file = task.output_file

    with open(output_file, "r", encoding="utf-8") as f:
        log = f.read()

    return JSONResponse(status_code=200, content={"status": 0, "message": "OK", "data": log, "taskStatus": task.status})
