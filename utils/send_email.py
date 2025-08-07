from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import os
from dotenv import load_dotenv
from celery_worker import celery_ap
import asyncio

configs = ConnectionConfig(
    MAIL_USERNAME= os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM= os.environ.get('MAIL_FROM'),
    MAIL_PORT= os.environ.get('MAIL_PORT'),
    MAIL_SERVER= os.environ.get('MAIL_SERVER'),
    MAIL_STARTTLS= os.environ.get('MAIL_STARTTLS'),
    MAIL_SSL_TLS= os.environ.get('MAIL_SSL_TLS'),
    USE_CREDENTIALS= os.environ.get('USE_CREDENTIALS'),
    VALIDATE_CERTS= os.environ.get('VALIDATE_CERTS'),
)

@celery_ap.task
def send_email_task(to: str, subject: str, body: str):
    asyncio.run(_send_email(to, subject, body))

async def _send_email(to: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to],
        body=body,
        subtype="html",
    )
    fm = FastMail(configs)
    await fm.send_message(message)
