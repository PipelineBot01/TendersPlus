from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="TendersPlus",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)
def sender():
    global conf
    return FastMail(conf)




