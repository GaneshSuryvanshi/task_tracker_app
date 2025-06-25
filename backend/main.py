from fastapi import FastAPI
from routers import projects, tasks, users, roles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import SessionLocal, Base, engine
import models
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("App startup: Initializing database and roles...")
    # Startup code
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Add roles if not present
    roles = [
        {"id": 1, "name": "admin"},
        {"id": 2, "name": "task_creator"},
        {"id": 3, "name": "user"}
    ]
    for role in roles:
        db_role = db.query(models.Role).filter_by(id=role["id"]).first()
        if not db_role:
            logging.info(f"Adding missing role: {role['name']}")
            db.add(models.Role(id=role["id"], name=role["name"]))
    db.commit()
    # Add admin user if not present
    user = db.query(models.User).filter(models.User.email == "admin@test.com").first()
    if not user:
        logging.info("Adding default admin user.")
        user = models.User(
            name="Admin",
            email="admin@test.com",
            password="admin123",
            is_active=True,
            role_id=1
        )
        db.add(user)
        db.commit()
    db.close()
    yield
    # (Optional) Shutdown code

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(roles.router)

@app.get("/")
def read_root():
    return {"message": "Task Tracker API is running"}

