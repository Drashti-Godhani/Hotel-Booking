# app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import GMAIL_SENDER, GMAIL_APP_PASSWORD, OWNER_EMAIL


def send_booking_email(booking: dict) -> bool:
    subject = (
        f"New Booking Inquiry — {booking.get('guest_name', 'Unknown')} "
        f"({booking.get('check_in', '?')} to {booking.get('check_out', '?')})"
    )

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
      margin: 0;
      padding: 20px;
    }}
    .container {{
      max-width: 600px;
      margin: 0 auto;
      background-color: #ffffff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .header {{
      background-color: #1a1a2e;
      color: #ffffff;
      padding: 30px;
      text-align: center;
    }}
    .header h1 {{
      margin: 0;
      font-size: 24px;
      letter-spacing: 1px;
    }}
    .header p {{
      margin: 6px 0 0;
      color: #a0a0c0;
      font-size: 14px;
    }}
    .badge {{
      display: inline-block;
      background-color: #e63946;
      color: white;
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 12px;
      margin-top: 10px;
      letter-spacing: 1px;
    }}
    .section {{
      padding: 24px 30px;
    }}
    .section-title {{
      font-size: 13px;
      font-weight: bold;
      color: #888;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 14px;
      border-bottom: 1px solid #eee;
      padding-bottom: 8px;
    }}
    .info-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    .info-box {{
      background-color: #f8f9ff;
      border-radius: 8px;
      padding: 14px 16px;
      border-left: 4px solid #1a1a2e;
    }}
    .info-box .label {{
      font-size: 11px;
      color: #999;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 4px;
    }}
    .info-box .value {{
      font-size: 15px;
      font-weight: bold;
      color: #1a1a2e;
    }}
    .special-box {{
      background-color: #fff8e1;
      border-left: 4px solid #f4a261;
      border-radius: 8px;
      padding: 14px 16px;
      margin-top: 6px;
      font-size: 14px;
      color: #555;
    }}
    .dates-row {{
      display: flex;
      gap: 14px;
      margin-bottom: 14px;
    }}
    .date-box {{
      flex: 1;
      background-color: #eef2ff;
      border-radius: 8px;
      padding: 14px 16px;
      text-align: center;
      border-top: 4px solid #4361ee;
    }}
    .date-box .label {{
      font-size: 11px;
      color: #888;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}
    .date-box .value {{
      font-size: 16px;
      font-weight: bold;
      color: #1a1a2e;
      margin-top: 4px;
    }}
    .footer {{
      background-color: #f8f8f8;
      text-align: center;
      padding: 18px;
      font-size: 12px;
      color: #aaa;
      border-top: 1px solid #eee;
    }}
  </style>
</head>
<body>
  <div class="container">

    <!-- Header -->
    <div class="header">
      <h1>🏨 New Booking Inquiry</h1>
      <p>A new guest has submitted a booking request</p>
      <span class="badge">ACTION REQUIRED</span>
    </div>

    <!-- Guest Details -->
    <div class="section">
      <div class="section-title">Guest Details</div>
      <div class="info-grid">
        <div class="info-box">
          <div class="label">Full Name</div>
          <div class="value">{booking.get("guest_name", "N/A")}</div>
        </div>
        <div class="info-box">
          <div class="label">Phone Number</div>
          <div class="value">{booking.get("phone", "N/A")}</div>
        </div>
      </div>
    </div>

    <!-- Dates -->
    <div class="section" style="padding-top: 0;">
      <div class="section-title">Stay Dates</div>
      <div class="dates-row">
        <div class="date-box">
          <div class="label">Check-in</div>
          <div class="value">{booking.get("check_in", "N/A")}</div>
        </div>
        <div class="date-box">
          <div class="label">Check-out</div>
          <div class="value">{booking.get("check_out", "N/A")}</div>
        </div>
      </div>
    </div>

    <!-- Booking Details -->
    <div class="section" style="padding-top: 0;">
      <div class="section-title">Booking Details</div>
      <div class="info-grid">
        <div class="info-box">
          <div class="label">Guests</div>
          <div class="value">{booking.get("num_guests", "N/A")} People</div>
        </div>
        <div class="info-box">
          <div class="label">Rooms</div>
          <div class="value">{booking.get("num_rooms", "N/A")} Room(s)</div>
        </div>
        <div class="info-box">
          <div class="label">Room Type</div>
          <div class="value">{booking.get("room_type", "N/A")}</div>
        </div>
        <div class="info-box">
          <div class="label">Budget / Night</div>
          <div class="value">{booking.get("budget", "N/A")}</div>
        </div>
      </div>
    </div>

    <!-- Special Request -->
    <div class="section" style="padding-top: 0;">
      <div class="section-title">Special Request</div>
      <div class="special-box">
        {booking.get("special_request") or "No special requests."}
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      Please contact the guest at your earliest convenience.<br>
      — Hotel Moon
    </div>

  </div>
</body>
</html>
"""

    msg = MIMEMultipart("alternative")
    msg["From"] = GMAIL_SENDER
    msg["To"] = OWNER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_SENDER, OWNER_EMAIL, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
