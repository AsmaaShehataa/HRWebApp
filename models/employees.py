#!/usr/bin/python3
"""Employee model"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, DateTime, BLOB, ForeignKey
import hashlib
from datetime import datetime


class Employee(BaseModel, Base):
    """Employee class"""
    __tablename__ = 'employees'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    department = Column(String(128), nullable=False)
    start_date = Column(DateTime, nullable=False)
    salary = Column(String(128), nullable=False)
    role = Column(Integer, default=0, nullable=False)
    photo = Column(String(250), nullable=True)
    deleted_at = Column(DateTime, nullable=True, default=None) # Soft Delete
    admin_id = Column(String(60), ForeignKey('admins.id'), nullable=False)

    # its 1:1 relationship but but one way direction (admin -> employee)
    # admin can access employee but employee atts can't access admin
    admin = relationship('Admin', back_populates='employees')

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

    def soft_del(self):
        """Soft delete the user"""
        self.deleted_at = datetime.now()
        self.save()
