from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/roles", tags=["roles"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Role)
def create_task(task: schemas.Role, db: Session = Depends(get_db)):
    logging.info(f"Creating new role: {task}")
    db_task = models.Role(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logging.info(f"Role created with ID: {db_task.id}")
    return db_task

@router.get("/", response_model=list[schemas.Role])
def list_tasks(db: Session = Depends(get_db)):
    logging.info("Listing all roles.")
    return db.query(models.Role).all()

@router.get("/{task_id}", response_model=schemas.Role)
def get_task(task_id: int, db: Session = Depends(get_db)):
    logging.info(f"Fetching role with ID: {task_id}")
    task = db.query(models.Role).get(task_id)
    if not task:
        logging.warning(f"Role not found: {task_id}")
        raise HTTPException(status_code=404, detail="roles not found")
    return task

@router.put("/{task_id}", response_model=schemas.Role)
def update_task(task_id: int, task: schemas.Role, db: Session = Depends(get_db)):
    logging.info(f"Updating role with ID: {task_id}")
    db_task = db.query(models.Role).get(task_id)
    if not db_task:
        logging.warning(f"Role not found for update: {task_id}")
        raise HTTPException(status_code=404, detail="roles not found")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    logging.info(f"Role updated: {db_task.id}")
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    logging.info(f"Deleting role with ID: {task_id}")
    task = db.query(models.Role).get(task_id)
    if not task:
        logging.warning(f"Role not found for deletion: {task_id}")
        raise HTTPException(status_code=404, detail="roles not found")
    db.delete(task)
    db.commit()
    logging.info(f"Role deleted: {task_id}")
    return {"ok": True}