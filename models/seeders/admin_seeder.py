#!/usr/bin/python3
"""Admin seeder"""

from models import storage
from models.employees import Employee
from models.admin import Admin
from datetime import datetime
import hashlib
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdminSeeder():
    """Admin seeder"""

    def __init__(self):
        """Initialize the AdminSeeder instance"""
        self.admins = []
        self.employees = []

    def seed(self):
        """Seed the database with an admin user"""
        # delete user if exists to avoid duplicates
        existing_users = storage.all(Employee)
        for user in existing_users.values():
          if user.email in ["admin@example.com", "alice.smith@example.com", "bob.john@example.com"]:
            storage.delete(user)
        storage.save()

        # securing PWs
        admin_password = hashlib.md5("admin_password".encode()).hexdigest()
        user_password = hashlib.md5("user_password".encode()).hexdigest()

        # Create an admin user
        self.admin = Admin(  #instance variable
            name="Admin",
            email="admin@example.com",
            password=admin_password,
            role=1
        )
        
        # Create a regular user
        self.employees.append(Employee(
            name="Alice Smith",
            email="alice.smith@example.com",
            password=user_password,
            phone="0987654321",
            department="Engineering",
            start_date=datetime(2024, 8, 1),
            salary="80000",
            role=0,
            admin_id=self.admin.id  # Assign to the created admin
        ))
        
        # 1 more user for testing
        self.employees.append(Employee(
            name="Bob Johnson",
            email="bob.john@example.com",
            password=user_password,
            phone="0987654321",
            department="Finance",
            start_date=datetime(2024, 8, 1),
            salary="50000",
            role=0,
            admin_id=self.admin.id
        ))

        # Save the admins and employees
        storage.new(self.admin)
        for employee in self.employees:
          storage.new(employee)
          if employee.role == 1:
            logger.info(f"Welcome Admin user: {employee.name}")
          else:
            logger.info(f"Welcome Regular user: {employee.name}")
        storage.save()
        #logger.info("Users saved successfully")
        logger.info(f"Admin ID: {self.admin.id}")


if __name__ == "__main__":
  seeder = AdminSeeder()
  seeder.seed()