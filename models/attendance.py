#!/usr/bin/python3
"""Attendance model"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from extensions import db

class Attendance(BaseModel, Base):
    """Attendance class"""
    __tablename__ = 'attendance'

    employee_id = db.Column(db.String(60), db.ForeignKey('employees.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=True)
    #employee = db.relationship('Employee', back_populates='attendance')

    def __init__(self, *args, **kwargs):
        """Initialize the Attendance instance"""
        super().__init__(*args, **kwargs)
