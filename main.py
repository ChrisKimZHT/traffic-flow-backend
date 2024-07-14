import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import config
from database import Base, engine
from service.face import face_router
from service.plate import plate_router
from service.stat import stat_router
from service.task import task_router
from service.video import video_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_router, prefix="/video")
app.include_router(stat_router, prefix="/stat")
app.include_router(task_router, prefix="/task")
app.include_router(plate_router, prefix="/plate")
app.include_router(face_router, prefix="/face")


@app.get("/")
async def root():
    return {
        "status": 0,
        "message": "OK",
        "version": "v1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(app, host=config.bind_host, port=config.bind_port)
