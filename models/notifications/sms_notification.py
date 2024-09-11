#!/usr/bin/python3
"""SMS Notification module"""

from models.notifications.notification import Notification
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SMSNotification(Notification):
    """SMS Notification class"""

    def send(self, recipient, message):
        """Send a SMS notification to a recipient"""
        print(f'Sending SMS to {recipient}: {message}')
        logger.info(f'Sending SMS to {recipient}: {message}')