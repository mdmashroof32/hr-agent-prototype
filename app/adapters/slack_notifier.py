import os
import requests
import logging

logger = logging.getLogger(__name__)
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

def notify(message: str):
    if SLACK_WEBHOOK:
        try:
            requests.post(SLACK_WEBHOOK, json={"text": message}, timeout=5)
        except Exception:
            logger.exception("Failed to send slack notification")
    else:
        # Fallback to logging for prototype
        logger.info(f"[SlackStub] {message}")
