# email_notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_PASSWORD, SENDER_EMAIL, RECEIVER_EMAIL

def send_alert_email(city, temperature):
    sender_email = SENDER_EMAIL
    receiver_email = RECEIVER_EMAIL
    password = EMAIL_PASSWORD

    subject = f"ALERT: High Temperature in {city}"
    body = f"The temperature has exceeded the threshold! Current temperature in {city} is {temperature}°C."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print(f"Alert email sent for {city}.")
    except Exception as e:
        print(f"Failed to send email: {e}")
