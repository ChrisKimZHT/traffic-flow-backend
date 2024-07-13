from typing import List, Type

from sqlalchemy.orm import Session

from model.VideoModel import Video


class VideoCrud:
    @staticmethod
    def create(db: Session, title: str, description: str, file_name: str, file_size: int, upload_time: int) -> Video:
        video = Video(title=title, description=description, file_name=file_name, file_size=file_size,
                      upload_time=upload_time)
        db.add(video)
        db.commit()
        db.refresh(video)
        return video

    @staticmethod
    def get_all(db: Session) -> List[Type[Video]]:
        return db.query(Video).all()

    @staticmethod
    def get_by_id(db: Session, video_id: int) -> Video | None:
        return db.query(Video).filter(Video.video_id == video_id).first()

    @staticmethod
    def update(db: Session, video: Video) -> Video:
        db.commit()
        db.refresh(video)
        return video
