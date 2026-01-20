from typing import Dict
import logging

logger = logging.getLogger(__name__)

def send_email(params: Dict):
    to = params.get("to")
    subject = params.get("subject")
    body = params.get("body")
    # In production, integrate with SendGrid, SES, Mailgun, etc.
    logger.info(f"[Email] To: {to} Subject: {subject} Body: {body}")
    return {"ok": True}
