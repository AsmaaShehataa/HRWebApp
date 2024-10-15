#!/usr/bin/python3

from datetime import datetime
from sqlalchemy import Column, VARCHAR
from models.base_model import BaseModel, Base
from extensions import db


class Settings(BaseModel, Base):
    """Settings class"""
    __tablename__ = 'settings'
    key = db.Column(VARCHAR(128), unique=True, nullable=False)
    value = db.Column(VARCHAR(128), nullable=False)
    


    @staticmethod
    def get_value(key):
        """Get a setting by key"""
        setting = db.session.query(Settings).filter(Settings.key == key).first()
        return setting.value if setting else None

    @staticmethod
    def set_value(key, value):
        """Set a setting by key"""
        setting = db.session.query(Settings).filter(Settings.key == key).first()
        if setting:
            setting.value = value
        else:
            setting = Settings(key=key, value=value)
        db.session.add(setting)
        db.session.commit()

    def __init__(self, *args, **kwargs):
        """Initialize the Settings instance"""
        super().__init__(*args, **kwargs)
