# 🏨 Hotel Booking AI Assistant

A terminal-based AI-powered hotel booking assistant that collects guest information through natural conversation and automatically sends a formatted email to the hotel owner.

---
## 💡 How It Works

1. Customer chats with the AI bot in the terminal
2. Bot collects all required booking information one question at a time
3. Once all info is collected, a structured email is sent to the hotel owner automatically

---

## 🔁 Flow
Customer (Terminal)

↓

Conversation Agent (OpenRouter AI)

↓

Structuring Agent (Extract JSON)

↓

PostgreSQL Database

↓

Email Service (Gmail SMTP) → Hotel Owner

---

<img width="1717" height="916" alt="ChatGPT Image Jun 18, 2026, 02_08_02 PM" src="https://github.com/user-attachments/assets/31539b63-9297-4949-b86e-99711b69a82b" />

## 🛠️ Tech Stack

| Layer        | Technology              |
|--------------|-------------------------|
| Language     | Python 3.11             |
| AI API       | OpenRouter              |
| Database     | PostgreSQL (Docker)     |
| ORM          | SQLAlchemy              |
| Email        | Gmail SMTP              |
| Package Manager | uv                   |
| Container    | Docker + Docker Compose |

---

## 📁 Project Structure
hotel-booking-bot/

├── app/

│   ├── agents/

│   │   ├── conversation_agent.py    # AI chat logic

│   │   └── structuring_agent.py     # Extract JSON from chat

│   ├── database/

│   │   ├── models.py                # SQLAlchemy tables

│   │   ├── connection.py            # DB session setup

│   │   └── repository.py           # Save/fetch functions

│   ├── services/

│   │   └── email_service.py         # Gmail SMTP email sender

│   └── config.py                    # Environment variables

├── frontend/

│   └── chat_app.py                  # Streamlit UI (optional)

├── main.py                          # Terminal bot entry point

├── docker-compose.yml               # PostgreSQL Docker setup

├── Dockerfile                       # App Docker setup

├── pyproject.toml                   # Dependencies (uv)

├── .env.example                     # Environment variables template

└── README.md

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) installed
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- OpenRouter API key → [openrouter.ai](https://openrouter.ai)
- Gmail App Password → [Google Account Settings](https://myaccount.google.com/apppasswords)

---

### Step 1 — Clone the repo

```bash
git clone https://github.com/yourusername/hotel-booking-bot.git
cd hotel-booking-bot
```

### Step 2 — Install dependencies

```bash
uv sync
```

### Step 3 — Setup environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
DATABASE_URL=postgresql://hoteluser:hotelpass@localhost:5433/hoteldb
GMAIL_SENDER=yourbot@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
OWNER_EMAIL=hotelowner@gmail.com
```

### Step 4 — Start PostgreSQL with Docker

```bash
docker compose up db -d
```

### Step 5 — Run the bot

```bash
uv run main.py
```

---

## 🗄️ Database Tables

### `conversations`
Stores full chat history per session.

| Column       | Type    | Description              |
|--------------|---------|--------------------------|
| id           | Integer | Primary key              |
| session_id   | String  | Unique session ID        |
| history      | JSON    | Full conversation history|
| is_complete  | Integer | 1 = all info collected   |
| created_at   | DateTime| Timestamp                |

### `booking_inquiries`
Stores structured booking data after conversation ends.

| Column          | Type    | Description           |
|-----------------|---------|-----------------------|
| id              | Integer | Primary key           |
| session_id      | String  | Links to conversation |
| guest_name      | String  | Guest full name       |
| phone           | String  | Contact number        |
| check_in        | String  | Check-in date         |
| check_out       | String  | Check-out date        |
| num_guests      | Integer | Number of guests      |
| num_rooms       | Integer | Number of rooms       |
| room_type       | String  | AC or Non-AC          |
| budget          | String  | Budget per night      |
| special_request | Text    | Any special requests  |
| email_sent      | Integer | 1 = email sent        |

---

## 📧 Email Preview

Owner receives a clean HTML email with:

- Guest name and phone number
- Check-in and check-out dates
- Number of guests and rooms
- Room type and budget
- Special requests

---

## 🚀 Run with Full Docker (Optional)

To run both the app and database in Docker:

```bash
docker compose up --build
```

App will be available at `http://localhost:8501`

---

## 🔐 Environment Variables

| Variable           | Description                        |
|--------------------|------------------------------------|
| OPENROUTER_API_KEY | Your OpenRouter API key            |
| DATABASE_URL       | PostgreSQL connection string       |
| GMAIL_SENDER       | Gmail address used to send emails  |
| GMAIL_APP_PASSWORD | Gmail app password (not regular)   |
| OWNER_EMAIL        | Hotel owner's email address        |

---

## ⚠️ Important Notes

- Never commit your `.env` file — it is in `.gitignore`
- Use Gmail **App Password**, not your regular Gmail password
- OpenRouter free models may have rate limits

---

## 📄 License

MIT License — free to use and modify.
