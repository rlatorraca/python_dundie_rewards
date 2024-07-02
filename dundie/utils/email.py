import re  # Regular expression (REGEX)
import smtplib  # Send email using Simple Mail Transfer Protocol (SMTP).
from email.mime.text import MIMEText

from dundie.settings import SMTP_HOST, SMTP_PORT, SMTP_TIMEOUT
from dundie.utils.log import get_logger

log = get_logger()

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"  # Regular expression


def check_valid_email(email_address):
    """Check if email address is valid"""
    return bool(re.fullmatch(regex, email_address))


def send_email(from_, to_, subject, text):
    if not isinstance(to_, list):
        to_ = [to_]

    server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT, timeout=SMTP_TIMEOUT)
    try:
        with server as email_server:
            message = MIMEText(text)
            message["Subject"] = subject
            message["From"] = from_
            message["To"] = ",".join(to_)
            email_server.sendmail(from_, to_, message.as_string())
    except Exception:
        log.error("Dundie cannot send email to %s", to_)
