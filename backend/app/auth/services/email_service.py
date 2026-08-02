import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class EmailService:

    @staticmethod
    async def send_otp(email: str, otp: str):

        subject = "Alumni Portal - Email Verification"

        body = f"""
Hello,

Your verification code is:

{otp}

This code will expire in 60 seconds.

If you didn't request this code, please ignore this email.

Regards,
Alumni Portal Team
"""

        message = MIMEMultipart()

        message["From"] = settings.SMTP_FROM
        message["To"] = email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                settings.SMTP_EMAIL,
                settings.SMTP_PASSWORD
            )

            server.send_message(message)