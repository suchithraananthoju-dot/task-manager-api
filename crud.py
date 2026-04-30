from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate
from schemas import TaskCreate
from schemas import TaskCreate, TaskUpdate

def create_task(db: Session, task: TaskCreate):
    new_task = Task(
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task": new_task
    }


def get_tasks(db: Session):
    return db.query(Task).all()

def update_task(db: Session, task_id: int, updated_task: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    task.title = updated_task.title
    task.description = updated_task.description
    task.status = updated_task.status

    db.commit()
    db.refresh(task)

    return {
        "message": "Task updated successfully",
        "task": task
    }



def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}