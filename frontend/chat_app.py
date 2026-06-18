import streamlit as st

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.database.connection import init_db, SessionLocal
from app.database.repository import (
    create_session,
    save_conversation,
    save_booking,
    mark_email_sent
)
from app.agents.conversation_agent import chat
from app.agents.structuring_agent import extract_booking_data
from app.services.email_service import send_booking_email

# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------
init_db()

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Hotel Booking Assistant",
    page_icon="🏨",
    layout="centered"
)

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.stChatMessage {
    border-radius: 12px;
}

.header-box {
    text-align: center;
    padding: 10px;
}

.footer {
    text-align: center;
    color: gray;
    font-size: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="header-box">
        <h1>🏨 Hotel Booking Assistant</h1>
        <p>
            Welcome! I am here to help you with your hotel reservation.
            Please provide your details and I will guide you through the booking process.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.header("Reservation Details")

    st.info("""
    Please keep the following information ready:

    • Full Name

    • Email Address

    • Phone Number

    • Check-in Date

    • Check-out Date

    • Number of Guests

    • Room Preference
    """)

    st.success("Our team will contact you after reviewing your request.")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()

if "booking_data" not in st.session_state:
    st.session_state.booking_data = None

if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

if "history" not in st.session_state:
    st.session_state.history = []

if "done" not in st.session_state:
    st.session_state.done = False

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------
for msg in st.session_state.history:
    role = "user" if msg["role"] == "user" else "assistant"

    with st.chat_message(role):
        st.write(msg["content"])

# --------------------------------------------------
# BOOKING COMPLETED
# --------------------------------------------------
if st.session_state.done:

    st.success("✅ Booking Inquiry Submitted Successfully!")

    if st.session_state.email_sent:
        st.success("📧 Confirmation Email Sent Successfully")
    else:
        st.warning("⚠️ Booking saved but email could not be sent")

    st.subheader("Reservation Summary")

    if st.session_state.booking_data:
        st.json(st.session_state.booking_data)

    st.info(
        "Our hotel team will review your request and contact you shortly."
    )

    st.balloons()
    st.stop()

# --------------------------------------------------
# INITIAL GREETING
# --------------------------------------------------
if not st.session_state.history:

    greeting = """
Hello! 👋

Welcome to our Hotel Booking Assistant.

I will help you complete your reservation request quickly and easily.

To get started, may I know your full name?
"""

    with st.chat_message("assistant"):
        st.write(greeting)

    st.session_state.history.append(
        {
            "role": "assistant",
            "content": greeting
        }
    )

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------
user_input = st.chat_input(
    "Type your message here..."
)

# --------------------------------------------------
# CHAT PROCESSING
# --------------------------------------------------
if user_input:

    # Display User Message
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Generate Assistant Response
    with st.spinner("Processing your request..."):

        bot_reply, is_complete = chat(
            st.session_state.history,
            user_input
        )

    # Display Assistant Response
    with st.chat_message("assistant"):
        st.write(bot_reply)

    st.session_state.history.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )

    # Save Conversation
    db = SessionLocal()

    save_conversation(
        db,
        st.session_state.session_id,
        st.session_state.history
    )

    # --------------------------------------------------
    # COMPLETE BOOKING WORKFLOW
    # --------------------------------------------------
    if is_complete:

        booking_data = extract_booking_data(
            st.session_state.history
        )

        booking = save_booking(
            db,
            st.session_state.session_id,
            booking_data
        )

        success = send_booking_email(
            booking_data
        )

        if success:
            mark_email_sent(
                db,
                booking.id
            )

        st.session_state.booking_data = booking_data
        st.session_state.email_sent = success
        st.session_state.done = True

        db.close()

        st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")

st.markdown(
    """
    <div class="footer">
        © 2026 Hotel Booking Assistant | Powered by AI
    </div>
    """,
    unsafe_allow_html=True
)

