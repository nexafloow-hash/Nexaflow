import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

print("EMAIL_USER:", EMAIL_USER)
print("EMAIL_PASSWORD:", EMAIL_PASSWORD)


def enviar_email(destinatario: str, assunto: str, mensagem: str):
    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = EMAIL_USER
    msg["To"] = destinatario

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, destinatario, msg.as_string())