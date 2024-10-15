#!/usr/bin/python3

"""Notification Factory module"""

from models.notifications.email_notification import EmailNotification
from models.notifications.sms_notification import SMSNotification
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationFactory:
    """Notification Factory Class"""

    @staticmethod
    def create_notification(notification_type):
        """Create a notification"""
        if notification_type == "email":
            return EmailNotification()
        elif notification_type == "sms":
            return SMSNotification()
        else:
            logger.error(f"Invalid notification type: {notification_type}")
            raise ValueError(f'Invalid notification type: {notification_type}')

