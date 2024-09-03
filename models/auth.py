# #!/usr/bin/python3
# """Auth routes"""

# from sqlalchemy import Column, String, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# from models.base_model import BaseModel, Base
# from models import storage
# from os import getenv
# import hashlib

# class Role(BaseModel, Base):
#     """Role class"""
#     __tablename__ = 'roles'
#     name = Column(String(20), nullable=False)
#     description = Column(String(260), nullable=True)

#     #permissions = relationship('Permission', backref='role', cascade='all, delete-orphan')

#     def __init__(self, *args, **kwargs):
#         """Initialization of Role"""
#         super().__init__(*args, **kwargs)


# class User(BaseModel, Base):
#     """General User class"""
#     __tablename__ = 'users'
#     email = Column(String(128), nullable=False, unique=True)
#     password = Column(String(255), nullable=False)
#     name = Column(String(128), nullable=True)
#     phone = Column(String(20), nullable=True)
#     role_id = Column(String(128), ForeignKey('roles.id'), nullable=False)
#     role = relationship('Role', backref='users')

#     def __init__(self, *args, **kwargs):
#         """Initialization of User"""
#         super().__init__(*args, **kwargs)

#     def set_password(self, password):
#         """Set password"""
#         self.password = hashlib.md5(password.encode()).hexdigest()

#     def check_password(self, password):
#         """Check password"""
#         return self.password == hashlib.md5(password.encode()).hexdigest()
