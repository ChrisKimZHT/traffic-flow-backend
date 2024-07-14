import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

get_image_router = APIRouter()


@get_image_router.get("/getImage")
async def _(image: str):
    cur_work_dir = os.getcwd()
    image_path = os.path.join(cur_work_dir, "runs/face", image)
    return FileResponse(image_path)
