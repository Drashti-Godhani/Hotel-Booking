# app/database/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Conversation(Base):
    """Har customer ki poori chat history store hoti hai"""
    __tablename__ = "conversations"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    session_id    = Column(String(100), unique=True, nullable=False)
    history       = Column(JSON, default=list)       # list of {role, content}
    is_complete   = Column(Integer, default=0)        # 1 = sab info mil gayi
    created_at    = Column(DateTime, default=datetime.utcnow)
    updated_at    = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BookingInquiry(Base):
    """Structured booking data — structuring agent ke baad banta hai"""
    __tablename__ = "booking_inquiries"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    session_id      = Column(String(100), nullable=False)
    guest_name      = Column(String(200))
    phone           = Column(String(20))
    check_in        = Column(String(20))    # "2026-06-20"
    check_out       = Column(String(20))    # "2026-06-22"
    num_guests      = Column(Integer)
    num_rooms       = Column(Integer)
    room_type       = Column(String(50))    # "AC" ya "Non-AC"
    budget          = Column(String(100))   # "3000-5000 per night"
    special_request = Column(Text)
    email_sent      = Column(Integer, default=0)   # 1 = email bhej diya
    created_at      = Column(DateTime, default=datetime.utcnow)