from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

conf = ConnectionConfig(
    MAIL_USERNAME = Config.MAIL_USERNAME,
    MAIL_PASSWORD = Config.MAIL_PASSWORD,
    MAIL_FROM = Config.MAIL_FROM,
    MAIL_PORT = Config.MAIL_PORT,
    MAIL_SERVER = Config.MAIL_SERVER,
    MAIL_FROM_NAME = Config.MAIL_FROM_NAME,
    MAIL_SSL_TLS = Config.MAIL_SSL_TLS,
    MAIL_STARTTLS= Config.MAIL_STARTTLS,
    USE_CREDENTIALS = Config.USE_CREDENTIALS,

    TEMPLATE_FOLDER=Path(BASE_DIR, 'templates')
)


mail = FastMail(
    config=conf
)

def create_message(recipients : list[str], subject  :str, body : str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )

    return message

