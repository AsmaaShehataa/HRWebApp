#!/usr/bin/python3
"""Base Model"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from extensions import db

time = "%Y-%m-%dT%H:%M:%S.%f"
Base = declarative_base()

class BaseModel(db.Model):
    __abstract__ = True
    """BaseModel class"""
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of BaseModel"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            if kwargs.get("id", None) is None:
                self.id = str(uuid4())
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """String representation of BaseModel"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """Updayes the attribute 'updated_at with the current datetime"""
        # self.updated_at = datetime.utcnow()
        # models.storage.new(self)
        # models.storage.save()
        if not self.id:
            self.id = str(uuid4())
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """Return a dictionary contains all k & v of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        if hasattr(self, "_plain_password"):
            new_dict["password"] = self.password # other wise to retuen the password as plain text we should replace with self._plain_password


        for attr in ["name", "email", "phone", "department", "start_date", "salary", "role", "photo", "admin_id"]:
            if hasattr(self, attr):
                new_dict[attr] = getattr(self, attr)
        for column in self.__table__.columns:
            column_name = column.name
            if isinstance(getattr(self, column_name), datetime):
                new_dict[column_name] = getattr(self, column_name).strftime("%Y-%m-%d %H:%M:%S")
            else:
                new_dict[column_name] = getattr(self, column_name)
        # if getenv("save_fs") is None:
        #     if "password" in new_dict:
        #         del new_dict["password"] --> this is for the old version will remove the password field from the emp class
        return new_dict
    
    def custom_dict(self):
        """Return a custom dictionary with selected fields"""
        return {
            "check_in": self.check_in.strftime("%Y-%m-%d %H:%M:%S") if self.check_in else None,
            "check_out": self.check_out.strftime("%Y-%m-%d %H:%M:%S") if self.check_out else None,
            "employee_id": self.employee_id
    }


    def delete(self):
        """Delete the current instance from the storage"""
        #models.storage.delete(self)
        db.session.delete(self)
        db.session.commit()
