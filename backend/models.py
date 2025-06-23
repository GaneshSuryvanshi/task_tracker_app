from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from database import Base
import enum

class TaskStatus(str, enum.Enum):
    new = "new"
    in_progress = "in-progress"
    blocked = "blocked"
    completed = "completed"
    not_started = "not started"

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    password = Column(String(128))  # Add this for password-based login
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="SET NULL"),nullable=True)
    owner = relationship("User")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    due_date = Column(Date)
    status = Column(Enum(TaskStatus), default=TaskStatus.new)
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="SET NULL"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id",ondelete="CASCADE"))
    owner = relationship("User")
    project = relationship("Project")


