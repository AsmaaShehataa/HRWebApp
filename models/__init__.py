#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from models.engine.db_storage import DBStorage
from models.attendance import Attendance

storage = DBStorage()
storage.reload()
