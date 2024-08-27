#!/usr/bin/python3
"""Storage module"""

from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import BaseModel, Base
from models.employees import Employee
from models.admin import Admin

load_dotenv() # to take the variables from .env

classes = {"Employee": Employee}

class DBStorage:
    """Class to interact with the MySQL database"""
    __engine = None
    __session = None
    
    def __init__(self):
        """Instantiate a DBStorage object"""
# Retrieve environment variables
        HR_MYSQL_USER = getenv('HR_MYSQL_USER')
        HR_MYSQL_PWD = getenv('HR_MYSQL_PWD')
        HR_MYSQL_HOST = getenv('HR_MYSQL_HOST')
        HR_MYSQL_DB = getenv('HR_MYSQL_DB')
        HR_ENV = getenv('HR_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                              format(HR_MYSQL_USER,
                                     HR_MYSQL_PWD,
                                     HR_MYSQL_HOST,
                                     HR_MYSQL_DB))
        if HR_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    #print(f"Retrieved object: {obj}")  # Debug print
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.close()

    def get(self, cls, id):
        """Returns the object based on the class name and its ID, or
        None if not found"""
        if cls not in classes.values():
            return None
        all_cls = models.storage.all(cls)
        for obj in all_cls.values():
            if obj.id == id:
                return obj

    def get_active_users(self):
        """Returun all active users only"""
        users = self.all(Employee)
        active_users = {key: user for key, user in users.items() if user.deleted_at is None}
        return active_users
    
    def get_engine(self):
        """Returns the engine"""
        return self.__engine

    def get_meta(self):
        """Returns the metadata"""
        return Base.metadata

    def count(self, cls=None):
        """Returns the number of objects in storage"""
        return len(self.all(cls))
