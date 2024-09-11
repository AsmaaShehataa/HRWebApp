#!/usr/bin/python3

"""Email Notification module"""

from models.notifications.notification import Notification
import logging
from flask_mail import Message
from extensions import mail
from models.settings import Settings
from config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailNotification(Notification):
    """Email Notification Class"""

    def send(self, recipient, message):
        """Send an email notification to a recipient"""
        sender_email = Settings.get_value('email_sender') or Config.MAIL_DEFAULT_SENDER
        logger.info(f'Sending email to {recipient}: {message}')
        msg = Message(subject="New Employee Added", 
                      sender=sender_email,
                        recipients=[recipient])
        msg.body = message
        mail.send(msg)
        logger.info(f'Email from sender {sender_email} sent to {recipient}')
