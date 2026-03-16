from sqlalchemy.orm import Session

from app import models, schemas



def list_tasks(db: Session) -> list[models.Task]:
    return db.query(models.Task).order_by(models.Task.id.desc()).all()



def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.query(models.Task).filter(models.Task.id == task_id).first()



def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task



def update_task(db: Session, db_task: models.Task, task_update: schemas.TaskUpdate) -> models.Task:
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task



def delete_task(db: Session, db_task: models.Task) -> None:
    db.delete(db_task)
    db.commit()
