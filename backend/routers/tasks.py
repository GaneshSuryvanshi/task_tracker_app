from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    logging.info(f"Creating new task: {task}")
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logging.info(f"Task created with ID: {db_task.id}")
    return db_task

@router.get("/", response_model=list[schemas.Task])
def list_tasks(db: Session = Depends(get_db)):
    logging.info("Listing all tasks.")
    return db.query(models.Task).all()

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    logging.info(f"Fetching task with ID: {task_id}")
    task = db.query(models.Task).get(task_id)
    if not task:
        logging.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="task not found")
    return task

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    logging.info(f"Updating task with ID: {task_id}")
    db_task = db.query(models.Task).get(task_id)
    if not db_task:
        logging.warning(f"Task not found for update: {task_id}")
        raise HTTPException(status_code=404, detail="task not found")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    logging.info(f"Task updated: {db_task.id}")
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    logging.info(f"Deleting task with ID: {task_id}")
    task = db.query(models.Task).get(task_id)
    if not task:
        logging.warning(f"Task not found for deletion: {task_id}")
        raise HTTPException(status_code=404, detail="task not found")
    db.delete(task)
    db.commit()
    logging.info(f"Task deleted: {task_id}")
    return {"ok": True}