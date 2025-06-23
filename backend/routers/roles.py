from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

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
    db_task = models.Role(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=list[schemas.Role])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Role).all()

@router.get("/{task_id}", response_model=schemas.Role)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Role).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="roles not found")
    return task

@router.put("/{task_id}", response_model=schemas.Role)
def update_task(task_id: int, task: schemas.Role, db: Session = Depends(get_db)):
    db_task = db.query(models.Role).get(task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="roles not found")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Role).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="roles not found")
    db.delete(task)
    db.commit()
    return {"ok": True}