#!/usr/bin/python3
"""User model"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime
import hashlib

class User(BaseModel, Base):
    """User class"""
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    department = Column(String(128), nullable=False)
    start_date = Column(DateTime, nullable=False)
    salary = Column(String(128), nullable=False)
    role = Column(Integer, default=0, nullable=False)

# Hashing the password

    def __init__(self, *args, **kwargs):
        """Initialize the User instance"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Set the password increypted"""
        if name == "password":
            value = hashlib.md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

    def verify_password(self, entered_password):
        """Verify the password"""
        entered_md5_hash= hashlib.md5(entered_password.encode()).hexdigest()
        return entered_md5_hash == self.password
