#!/usr/bin/python3

"""Admin model class"""

from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.employees import Employee
import models
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime

db = SQLAlchemy()

class Admin(BaseModel, Base):
    """Admin class"""
    __tablename__ = 'admins'
    name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False)
    password = Column(String(256), nullable=False)
    role = Column(Integer, default=1, nullable=False)
    deleted_at = Column(DateTime, nullable=True, default=None) # Soft Delete
    employees = relationship('Employee', back_populates='admin')

    def __init__(self, *args, **kwargs):
        """Initialize the Admin instance"""
        super().__init__(*args, **kwargs)
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    # def __setattr__(self, name, value):
    #     """Set the password increypted"""
    #     if name == "password":
    #         value = hashlib.md5(value.encode()).hexdigest()
    #     super().__setattr__(name, value)

    def verify_password(self, entered_password):
        """Verify the password"""
        entered_md5_hash= hashlib.md5(entered_password.encode()).hexdigest()
        return entered_md5_hash == self.password

    def soft_del(self):
        """Soft delete the user"""
        self.deleted_at = datetime.now()
        self.save()
