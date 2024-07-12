from sqlalchemy import Column, Integer, String

from database import Base


class Video(Base):
    __tablename__ = "video"

    video_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(255))
    file_name = Column(String(255))
    file_size = Column(Integer)  # bytes
    upload_time = Column(Integer)
    stat_processed = Column(Integer)  # 0: not processed, 1: processing, 2: processed
    plate_processed = Column(Integer)
    face_processed = Column(Integer)
    stat_res_path = Column(String(255))
    plate_res_path = Column(String(255))
    face_res_path = Column(String(255))

    def __init__(self, title: str, description: str, file_name: str, file_size: int, upload_time: int,
                 stat_processed: int = 0, plate_processed: int = 0, face_processed: int = 0,
                 stat_res_path: str = "", plate_res_path: str = "", face_res_path: str = ""):
        self.title = title
        self.description = description
        self.file_name = file_name
        self.file_size = file_size
        self.upload_time = upload_time
        self.stat_processed = stat_processed
        self.plate_processed = plate_processed
        self.face_processed = face_processed
        self.stat_res_path = stat_res_path
        self.plate_res_path = plate_res_path
        self.face_res_path = face_res_path
