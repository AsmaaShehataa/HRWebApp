#!/usr/bin/python3
"""Admin seeder"""

from models import storage
from models.employees import Employee
from models.admin import Admin
from datetime import datetime
import hashlib
import logging
from routes.auth.auth_routes import token_required
from werkzeug.security import generate_password_hash


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
        # existing_users = storage.all(Employee)
        # for user in existing_users.values():
        #   if user.email in ["admin@example.com", "admin2@example.com", "alice.smith@example.com", "bob.john@example.com"]:
        #     storage.delete(user)
        # storage.save()

        # securing PWs
        #admin_password = hashlib.md5("admin_password".encode()).hexdigest() -->old Version
        admin_password = generate_password_hash("admin_password")
        logger.info(f"Admin password: {admin_password}")
        #user_password = hashlib.md5("user_password".encode()).hexdigest() --> old Version
        user_password = generate_password_hash("user_password")

        # Create an admin user
        # existing_admins = storage.filter_by(Admin, email="admin@example.com")
        # logger.info(f"Existing adminsfound: {[admin.email for admin in existing_admins]}")
        # if len(existing_admins) == 0:
        #    self.admins.append(Admin(  
        #     name="Admin",
        #     email="admin@example.com",
        #     password=admin_password,
        #     role=1
        # ))


        
        # # create new admin
        # if len(storage.filter_by(Admin, email="admin2@example.com"))== 0:
        #   self.admins.append(Admin(
        #     name="Admin2",
        #     email="admin2@example.com",
        #     password=admin_password,
        #     role=1
        # ))
        self.admins.append(Admin(
            name="Admin",
            email="admin@example.com",
            password=admin_password,
            role=1
        ))
      

        
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
            admin_id=self.admins[0].id  # Assign to the created admin
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
            admin_id=self.admins[0].id
        ))

        # Save the admins and employees
        for admin in self.admins:
          storage.new(admin)
          logger.info(f"Saving email: {admin.email}, hashed password: {admin.password}")

        for employee in self.employees:
          storage.new(employee)
          logger.info(f"User created: {employee.name} (Role: {'Admin' if employee.role == 1 else 'Employee'})")

        storage.save()

if __name__ == "__main__":
  seeder = AdminSeeder()
  seeder.seed()