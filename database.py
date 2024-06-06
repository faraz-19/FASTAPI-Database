from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL='sqlite:///./database.db' #connects with the database file created
engine = create_engine(SQL_DATABASE_URL,connect_args={"check_same_thread": False})

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) #starts session when called in main.py




