from pydantic import BaseModel
from typing import Optional
from datetime import date
import enum

class TaskStatus(str, enum.Enum):
    new = "new"
    in_progress = "in-progress"
    blocked = "blocked"
    completed = "completed"
    not_started = "not started"

class Role(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True
    
class UserRole(BaseModel):
    name: str
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    name: str
    email: str
    password: Optional[str]
    is_active: Optional[bool] = True
    role_id: Optional[int]
    role: Optional[Role] = None
    class Config:
        orm_mode = True
class UserName(BaseModel):
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class UserLoginResponse(BaseModel):
    id: int
    name: str   
    email: str
    role : str




class UserCreate(BaseModel):
    name : str
    email : str
    password : str
    is_active: Optional[bool] = True
    role_id: Optional[int]

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: date
    end_date: date
    owner_id: int | None = None
    owner: Optional[UserName] = None
    class Config:
        orm_mode = True
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    owner_id: int | None = None  # This allows null/None values

class Task(BaseModel):
    id: int
    description: str
    due_date: date
    status: TaskStatus = TaskStatus.new
    owner_id: int | None = None
    project_id: int
    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    description: str
    due_date: date
    status: TaskStatus = TaskStatus.new
    owner_id: int | None = None  # This allows null/None values
    project_id: int
