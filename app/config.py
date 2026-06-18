# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://hoteluser:hotelpass@localhost:5433/hoteldb"
)
GMAIL_SENDER = os.getenv("GMAIL_SENDER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
OWNER_EMAIL = os.getenv("OWNER_EMAIL")
AI_MODEL = "anthropic/claude-3-haiku"  # ya jo bhi model use karna ho
