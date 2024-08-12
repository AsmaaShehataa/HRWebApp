#!/usr/bin/python3
"""Admin seeder"""

from models import storage
from models.user import User
from datetime import datetime
import hashlib
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdminSeeder():
    """Admin seeder"""

    def __init__(self):
        """Initialize the AdminSeeder instance"""
        self.users = []

    def seed(self):
        """Seed the database with an admin user"""
        # delete user if exists to avoid duplicates
        existing_users = storage.all(User)
        for user in existing_users.values():
          if user.email in ["admin@example.com", "alice.smith@example.com", "bob.john@example.com"]:
            storage.delete(user)
        storage.save()

        # securing PWs
        admin_password = hashlib.md5("admin_password".encode()).hexdigest()
        user_password = hashlib.md5("user_password".encode()).hexdigest()

        # Create an admin user
        self.admin = User(  #instance variable
            name="Admin",
            email="admin@example.com",
            password=admin_password,
            phone="1234567890",
            department="HR",
            start_date=datetime(2024, 8, 1),
            salary="100000",
            role=1
        )
        
        # Create a regular user
        self.regular_user = User(
            name="Alice Smith",
            email="alice.smith@example.com",
            password=user_password,
            phone="0987654321",
            department="Engineering",
            start_date=datetime(2024, 8, 1),
            salary="80000",
            role=0
        )
        
        # 1 more user for testing
        user2 = User( # local variable
            name="Bob Johnson",
            email="bob.john@example.com",
            password=user_password,
            phone="0987654321",
            department="Finance",
            start_date=datetime(2024, 8, 1),
            salary="50000",
            role=0
        )
        # adding users to the empty list 
        # self.users.append(self.admin)
        # self.users.append(self.regular_user)
        # self.users.append(user2)
        self.users.extend([self.admin, self.regular_user, user2])
        
        for user in self.users:
          storage.new(user)
          if user.role == 1:
            logger.info(f"Welcome Admin user: {user.name}")
          else:
            logger.info(f"Welcome Regular user: {user.name}")
        storage.save()
        logger.info("Users saved successfully")

if __name__ == "__main__":
  seeder = AdminSeeder()
  seeder.seed()