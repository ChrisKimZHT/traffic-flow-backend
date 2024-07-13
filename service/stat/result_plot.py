import os

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

from crud.VideoCrud import VideoCrud
from util.get_db import get_db

result_plot_router = APIRouter()


@result_plot_router.get("/resultPlot")
async def _(videoId: int, plotName: str, db: Session = Depends(get_db)):
    if not videoId or not plotName:
        return JSONResponse(status_code=400, content={"status": 1, "message": "Invalid Parameters"})

    try:
        video = VideoCrud.get_by_id(db, videoId)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if not video:
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video Not Found"})

    plot_path = os.path.join(video.stat_res_path, plotName)

    if not os.path.exists(plot_path):
        return JSONResponse(status_code=404, content={"status": 1, "message": "Plot Not Found"})

    return FileResponse(plot_path)
