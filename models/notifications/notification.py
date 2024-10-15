#!/usr/bin/python3
"""Notification module"""

from datetime import datetime
from abc import ABC, abstractmethod

class Notification(ABC):
    """Notification class"""

    @abstractmethod
    def send(self, recipient, message):
        """Send a notification to a recipient"""
        pass

    @abstractmethod
    def send_leave_email(self, recipient, subject, message):
        """Send a notification of leave to a recipient"""
        pass
