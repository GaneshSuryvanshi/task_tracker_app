from fastapi import FastAPI
from routers import projects, tasks, users, roles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import SessionLocal, Base, engine
import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.email == "admin@test.com").first()
    if not user:
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

