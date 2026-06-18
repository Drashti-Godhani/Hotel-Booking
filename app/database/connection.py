# app/database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from app.database.models import Base

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    """Tables create karo agar exist nahi karte"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """DB session do, kaam hone ke baad band karo"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()