from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
import logging

router = APIRouter(prefix="/projects", tags=["projects"])

# Configure logging
logging.basicConfig(level=logging.INFO)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    logging.info(f"Creating new project: {project}")
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    logging.info(f"Project created with ID: {db_project.id}")
    return db_project

@router.get("/", response_model=list[schemas.Project])
def list_projects(db: Session = Depends(get_db)):
    logging.info("Listing all projects.")
    return db.query(models.Project).all()

@router.get("/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    logging.info(f"Fetching project with ID: {project_id}")
    project = db.query(models.Project).get(project_id)
    if not project:
        logging.warning(f"Project not found: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    logging.info(f"Updating project with ID: {project_id}")
    db_project = db.query(models.Project).get(project_id)
    if not db_project:
        logging.warning(f"Project not found for update: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.model_dump().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    logging.info(f"Project updated: {db_project.id}")
    return db_project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    logging.info(f"Deleting project with ID: {project_id}")
    project = db.query(models.Project).get(project_id)
    if not project:
        logging.warning(f"Project not found for deletion: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    logging.info(f"Project deleted: {project_id}")
    return {"ok": True}