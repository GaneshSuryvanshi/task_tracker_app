from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Root123")
MYSQL_HOST = os.getenv("MYSQL_HOST","localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "task_tracker")

logging.basicConfig(level=logging.INFO)
logging.info(f"Creating SQLAlchemy engine for DB: {MYSQL_DB} at {MYSQL_HOST}:{MYSQL_PORT} as user {MYSQL_USER}")

DATABASE_URL = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()