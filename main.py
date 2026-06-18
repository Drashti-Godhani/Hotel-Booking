# main.py
from app.database.connection import init_db, SessionLocal
from app.database.repository import (
    create_session, save_conversation,
    mark_complete, save_booking, mark_email_sent
)
from app.agents.conversation_agent import chat
from app.agents.structuring_agent import extract_booking_data
from app.services.email_service import send_booking_email

def main():
    init_db()
    session_id = create_session()
    history = []

    print("\n" + "="*50)
    print("🏨  Hotel Booking Assistant")
    print("="*50)
    print("(Type 'exit' to quit)\n")

    greeting = "Welcome! I'm your hotel booking assistant. May I know your name please?"
    print(f"Bot: {greeting}\n")
    history.append({"role": "assistant", "content": greeting})

    db = SessionLocal()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Bot: Thank you! Have a great day. 🙏")
            break

        if not user_input:
            continue

        bot_reply, is_complete = chat(history, user_input)
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": bot_reply})

        if is_complete:
            # BOOKING_COMPLETE part hide karo, sirf clean message dikhao
            clean_reply = bot_reply.replace("BOOKING_COMPLETE:", "").strip()
            print(f"\nBot: {clean_reply}")
            print("\n✅ Your booking inquiry has been submitted successfully!")
            print("━"*50)

            save_conversation(db, session_id, history)
            mark_complete(db, session_id)

            print("⏳ Processing your booking details...")
            booking_data = extract_booking_data(history)
            booking = save_booking(db, session_id, booking_data)

            print("📧 Sending email to hotel owner...")
            success = send_booking_email(booking_data)
            if success:
                mark_email_sent(db, booking.id)
                print("✅ Hotel owner has been notified via email!")
            else:
                print("❌ Email sending failed.")

            print("━"*50)
            print("👋 Thank you for choosing our hotel. Goodbye!\n")
            break  # ← yahan conversation band ho jata hai

        print(f"\nBot: {bot_reply}\n")
        save_conversation(db, session_id, history)

    db.close()

if __name__ == "__main__":
    main()