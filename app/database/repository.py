# app/database/repository.py
import uuid
from sqlalchemy.orm import Session
from app.database.models import Conversation, BookingInquiry

def create_session() -> str:
    """Naya unique session ID banao"""
    return str(uuid.uuid4())

def get_conversation(db: Session, session_id: str) -> Conversation | None:
    return db.query(Conversation).filter(Conversation.session_id == session_id).first()

def save_conversation(db: Session, session_id: str, history: list) -> Conversation:
    """Conversation save ya update karo"""
    conv = get_conversation(db, session_id)
    if not conv:
        conv = Conversation(session_id=session_id, history=history)
        db.add(conv)
    else:
        conv.history = history
    db.commit()
    db.refresh(conv)
    return conv

def mark_complete(db: Session, session_id: str):
    """Jab sab info mil jaye"""
    conv = get_conversation(db, session_id)
    if conv:
        conv.is_complete = 1
        db.commit()

def save_booking(db: Session, session_id: str, data: dict) -> BookingInquiry:
    """Structured booking inquiry save karo"""
    booking = BookingInquiry(
        session_id      = session_id,
        guest_name      = data.get("guest_name"),
        phone           = data.get("phone"),
        check_in        = data.get("check_in"),
        check_out       = data.get("check_out"),
        num_guests      = data.get("num_guests"),
        num_rooms       = data.get("num_rooms"),
        room_type       = data.get("room_type"),
        budget          = data.get("budget"),
        special_request = data.get("special_request", ""),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def mark_email_sent(db: Session, booking_id: int):
    booking = db.query(BookingInquiry).filter(BookingInquiry.id == booking_id).first()
    if booking:
        booking.email_sent = 1
        db.commit()