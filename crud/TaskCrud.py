from typing import List, Type

from sqlalchemy.orm import Session

from model.TaskModel import Task


class TaskCrud:
    @staticmethod
    def create(db: Session, video_id: int, description: str, start_time: int, output_file: str, status: int) -> Task:
        task = Task(video_id, description, start_time, output_file, status)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_all(db: Session) -> List[Type[Task]]:
        return db.query(Task).all()

    @staticmethod
    def get_by_id(db: Session, task_id: int) -> Task | None:
        return db.query(Task).filter(Task.task_id == task_id).first()

    @staticmethod
    def update(db: Session, task: Task) -> Task:
        db.commit()
        db.refresh(task)
        return task
