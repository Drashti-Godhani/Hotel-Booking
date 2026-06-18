# app/agents/structuring_agent.py
import json
import requests
from app.config import OPENROUTER_API_KEY, AI_MODEL
from datetime import datetime

CURRENT_YEAR = datetime.now().year

EXTRACT_PROMPT = f"""
You are a data extraction assistant.

Extract hotel booking information from the conversation below and return ONLY valid JSON.

IMPORTANT DATE RULES:

- Today's year is {CURRENT_YEAR}.
- If the customer provides only day and month (example: "12 July"), use year {CURRENT_YEAR}.
- If the customer explicitly provides a year, use that year.
- Never invent a random year such as 2023 or 2024.
- Dates must be returned in YYYY-MM-DD format.

Required JSON format:

{{
  "guest_name": "string or null",
  "phone": "string or null",
  "check_in": "YYYY-MM-DD or null",
  "check_out": "YYYY-MM-DD or null",
  "num_guests": number or null,
  "num_rooms": number or null,
  "room_type": "AC" or "Non-AC" or null,
  "budget": "string or null",
  "special_request": "string or null"
}}

Return ONLY the JSON object.
No explanation.
No markdown.
"""

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Hotel Booking Bot",
}

def extract_booking_data(history: list[dict]) -> dict:
    conversation_text = ""
    for msg in history:
        role = "Customer" if msg["role"] == "user" else "Bot"
        conversation_text += f"{role}: {msg['content']}\n"

    payload = {
        "model": AI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": f"{EXTRACT_PROMPT}\n\nConversation:\n{conversation_text}"
            }
        ],
    }

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=HEADERS,
        json=payload,
    )

    if not response.ok:
        print(f"API Error: {response.status_code} - {response.text}")
        response.raise_for_status()

    raw = response.json()["choices"][0]["message"]["content"].strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        data  = json.loads(raw[start:end])

    return data
