import os
import smtplib
import json
import logging
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")
CONTACT_LOG = Path(__file__).resolve().parent.parent.parent / "contact_logs.json"


def is_configured() -> bool:
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASS and NOTIFY_EMAIL)


def _log_to_file(name, email, project_type, message):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "email": email,
        "project_type": project_type,
        "message": message,
    }
    logs = []
    if CONTACT_LOG.exists():
        try:
            logs = json.loads(CONTACT_LOG.read_text("utf-8"))
        except Exception:
            logs = []
    logs.append(entry)
    CONTACT_LOG.write_text(json.dumps(logs, indent=2), "utf-8")
    logger.info(f"Contact logged to file: {name} <{email}>")


async def send_contact_notification(name: str, email: str, project_type: str, message: str) -> bool:
    _log_to_file(name, email, project_type, message)

    if not is_configured():
        logger.warning("Email not configured — logged to file instead")
        return True

    subject = f"New Contact from {name} — {project_type}"
    body = f"""
New project inquiry from LeadForge AI website:

Name: {name}
Email: {email}
Project Type: {project_type}
Message: {message}
"""

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = NOTIFY_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        logger.info(f"Contact email sent for {name} <{email}>")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return True
