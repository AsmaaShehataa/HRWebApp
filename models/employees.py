#!/usr/bin/python3
"""Employee model"""

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, DateTime, BLOB, ForeignKey
import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class Employee(BaseModel, Base):
    """Employee class"""
    __tablename__ = 'employees'

    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(128), nullable=False)
    department = db.Column(db.String(128), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, default=0, nullable=False)
    photo = db.Column(db.String(250), nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None) # Soft Delete
    admin = db.relationship('Admin', back_populates='employees')
    admin_id = db.Column(db.String(60), db.ForeignKey('admins.id'), nullable=True)


    #Relationships with the new added model of leave request

    head_employee_id = db.Column(db.String(60), db.ForeignKey('employees.id'), nullable=True)
    #Self-Refrence relationship for manager(head_employee)
    head_employee = relationship('Employee', remote_side='Employee.id', back_populates='employees_managed')
    #leave_request = db.relationship('LeaveRequest', backref='employee', lazy=True)
    employees_managed = db.relationship('Employee', back_populates='head_employee', lazy=True)


    # its 1:1 relationship but but one way direction (admin -> employee)
    # admin can access employee but employee atts can't access admin
    #admin = relationship('Admin', back_populates='employees')

    #setter password method
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # def __setattr__(self, name, value):
    #     """Set the password increypted"""
    #     if name == "password":
    #         value = generate_password_hash(value)
    #     super().__setattr__(name, value)


    def __init__(self, *args, **kwargs):
        """Initialize the User instance"""
        super().__init__(*args, **kwargs)

    
    _password = None

    def __setattr__(self, name, value):
        """Set the password increypted"""
        if name == "password":
            self._plain_password = value
            hashed_value = generate_password_hash(value)
            #value = value  #--> this will revert the password to plain text
            super().__setattr__("password", hashed_value)
        else:
            super().__setattr__(name, value)

    # def verify_password(self, password):
    #     """Verify the password"""
    #     return check_password_hash(self.password, password)

    def setattrs(self, **kwargs):
        """Set the attributes"""
        for key, value in kwargs.items():
            setattr(self, key, value)


    def soft_del(self):
        """Soft delete the user"""
        self.deleted_at = datetime.now()
        self.save()
