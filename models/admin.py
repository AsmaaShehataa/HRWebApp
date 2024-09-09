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
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash



class Admin(BaseModel, Base):
    """Admin class"""
    __tablename__ = 'admins'
    name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer, default=1, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)
    employees = db.relationship('Employee', back_populates='admin')

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
        return check_password_hash(self.password, entered_password)

    def soft_del(self):
        """Soft delete the user"""
        self.deleted_at = datetime.now()
        self.save()
