from sqlalchemy import Column, Integer, String

from database import Base


class Task(Base):
    __tablename__ = "task"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer)
    description = Column(String(255))
    output_file = Column(String(255))
    status = Column(Integer)  # 0: in queue, 1: processing, 2: finished, 3: failed
