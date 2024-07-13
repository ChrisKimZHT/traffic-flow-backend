import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse

get_image_router = APIRouter()


@get_image_router.get("/getImage")
async def _(video: str, imageType: str, boxId: int):
    video_without_exp = video.split(".")[0]

    if not os.path.exists(os.path.join("./runs/plate/", video_without_exp)):
        return JSONResponse(status_code=404, content={"status": 1, "message": "Video not found"})

    image_path = os.path.join("./runs/plate/", video_without_exp, imageType, f"{boxId}.jpg")

    return FileResponse(image_path)
