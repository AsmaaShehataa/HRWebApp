#!/usr/bin/python3
"""Leave Request Model"""

from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, relationship
from models.base_model import BaseModel, Base
from extensions import db



class LeaveRequest(BaseModel, Base):
    """Leave Request class"""
    __tablename__ = 'leave_requests'

    employee_id = db.Column(db.String(60), db.ForeignKey('employees.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    leave_type = db.Column(db.String(60), nullable=False)
    status = db.Column(db.Integer, default=0, nullable=False)
    leave_days = db.Column(db.String, nullable=False)
    approved_by = db.Column(db.String(60), db.ForeignKey('employees.id'), nullable=True)
    reason = db.Column(db.String(1000), nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)
    
    # Relationships
    employee = db.relationship('Employee', ForeignKeys=[employee_id], backref='leave_requests')
    manager = db.relationship('Employee', ForeignKeys=[approved_by], backref='approved_leaves')
    #admin = db.relationship('Admin', back_populates='leave_requests')

    def __init__(self, *args, **kwargs):
        """Initialize the Leave Request instance"""
        super().__init__(*args, **kwargs)
        # if kwargs:
        #     for key, value in kwargs.items():
        #         if key != "__class__":
        #             setattr(self, key, value)
  
