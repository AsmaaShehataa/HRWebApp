#!/usr/bin/python3

from datetime import datetime
from sqlalchemy import Column, VARCHAR, Integer, DateTime
from models.base_model import BaseModel, Base
import models


class Settings(BaseModel, Base):
    """Settings class"""
    __tablename__ = 'settings'
    key = Column(VARCHAR(128), unique=True, nullable=False)
    value = Column(VARCHAR(128), nullable=False)
    

    def __init__(self, *args, **kwargs):
        """Initialize the Settings instance"""
        super().__init__(*args, **kwargs)
