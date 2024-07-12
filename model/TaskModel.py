from sqlalchemy import Column, Integer, String

from database import Base


class Task(Base):
    __tablename__ = "task"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer)
    description = Column(String(255))
    start_time = Column(Integer)
    output_file = Column(String(255))
    status = Column(Integer)  # 0: in queue, 1: processing, 2: finished, 3: failed

    def __init__(self, video_id: int, description: str, start_time: int, output_file: str, status: int):
        self.video_id = video_id
        self.description = description
        self.start_time = start_time
        self.output_file = output_file
        self.status = status
