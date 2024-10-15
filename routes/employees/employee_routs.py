#!/usr/bin/python3
"""Employees routes"""
from flask import jsonify, request, abort, Blueprint, flash
from models import storage
from models.employees import Employee
from models.admin import Admin
import logging
from flask import Flask
from web_flask.forms import EmployeeForm
import os
from werkzeug.security import generate_password_hash
import jwt
from config import Config
from functools import wraps
from extensions import db
from werkzeug.utils import secure_filename
#from app import app
from models.notifications.notification_factory import NotificationFactory
from models.attendance import Attendance
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

employee_bp = Blueprint('employee_bp', __name__, url_prefix='/employees')

# Define the allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg'}
UPLOAD_FOLDER = 'web_flask/static/uploads'

# admin token required
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token is missing'}), 403
        
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            #admin = storage.filter_by(Admin, email=data['email'])
            logger.info("Employee route 1")
            logger.info(f"Decoded email from token: {data['email']}")
            current_user = storage.filter_by(Admin, email=data['email'], first_param=True)

            if not current_user:
                return jsonify({'error': 'User not found'}), 403
        except Exception as e:
            logger.error('Token is invalid')
            return jsonify({'error': 'Token is invalid'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# employee token required
def employee_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token is missing'}), 403
        
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            logger.info("Employee route 2")
            logger.info(f"Decoded email from token: {data['email']}")
            current_user = Employee.query.filter_by(email=data['email']).first()
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 403
        except Exception as e:
            logger.error('Token is invalid')
            return jsonify({'error': 'Token is invalid'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@employee_bp.route('/', methods=['GET'])
@token_required
def get_employees(current_user):
    if current_user.role != 1:
        return jsonify({'message': 'Your are Not authorized to perform this action'}), 403
    #Query from the DB stoarge file
    #employees = storage.all(Employee)
    
    # query from the database
    #exclude certain feilds from the response
    #employees =Employee.query.with_entities(Employee.name, Employee.email).all()
    employees = Employee.query.all()
    
    logger.info(f"Employees: {employees}")
    if not employees:
        return jsonify({'error': 'Employees not found'}), 404
    
    #employees_list = [{"name": name, "email": email} for name, email in employees]
    employee_list = [employee.to_dict() for employee in employees]
    return jsonify(employee_list), 200


@employee_bp.route('/new', methods=['POST'])
@token_required
def add_employee(current_user):
    """Add new employee"""
    # cehck if the user is an admin
    logger.info(f"Current user: {current_user}")
    if current_user.role != 1:
        return jsonify({'message': 'Your are Not authorized to perform this action'}), 403
    
    form = EmployeeForm()
    if not form.validate_on_submit():
        return jsonify({"errors": form.errors}), 400
    
    # Handle file upload
    file = form.photo.data
    photo_url = None
    if file:
        if file != '':
            filename = secure_filename(file.filename)
            if filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                photo_url = os.path.join(UPLOAD_FOLDER, filename)
            else:
                return jsonify({'error': 'Invalid file type'}), 400
    plain_password = form.password.data
    data = {
        'name': form.name.data,
        'email': form.email.data,
        'password': plain_password,
        'phone': form.phone.data,
        'department': form.department.data,
        'start_date': form.start_date.data,
        'salary': form.salary.data,
        'photo': photo_url if photo_url else None,
        'head_employee_id': form.head_employee_id.data
    }
    logger.info(f"Photo URL: {photo_url}")

    required_fields = ['name', 'email', 'password', 'phone', 'department', 'start_date', 'salary']
    for field in required_fields:
        if field not in data or not data[field]:
            abort(400, 'Missing {}'.format(field))

    # check if the employee already exists
    #existing_employee = storage.all(Employee)
    # adding new employee to the database
    existing_employee = Employee.query.filter_by(email=form.email.data).first()

    if existing_employee:
        #if emp.email == form.email.data:
            flash('Employee already exists', 'danger')
            return jsonify({"error": "Employee already exists"}), 400
    try:
        # check if the head_employee_id is provided and exists
        if form.head_employee_id.data:
            head_employee = Employee.query.filter_by(id=form.head_employee_id.data).first()
            if head_employee:
                data['head_employee_id'] = head_employee.id
            else:
                return jsonify({'error': 'This manager does not exist'}), 400
        
        new_employee = Employee(**data)
        #new_employee.password = generate_password_hash(data['password']) #--> set the password and return the hashed
        #new_employee.set_password(data['password']) --> ignore this bec settattr is already implemented in the model and will generate the password hash
        new_employee.save()

        # Notification Content

        emp_welcome_message = (f"Welcome {new_employee.name}!\n"
                               f"Your Credentials are Email: {new_employee.email},\n" 
                               f"Password: {plain_password},\n"
                                 f"Department: {new_employee.department},\n\n"
                                    "Please keep your credentials safe and do not share them with anyone.\n\n"
                               )
        admin_message = f"New Employee {new_employee.name} has been added successfully with email {new_employee.email} and password {new_employee.password}"

        # Send Email Notification to employee
        email_notification = NotificationFactory.create_notification("email")
        #email_notification.send(new_employee.email, emp_welcome_message)
        email_notification.send(new_employee.email, "New Employee Added", emp_welcome_message)

        # Send Email Notification to Admin
        email_notification.send(current_user.email, "New Employee Added", admin_message)

        db.session.commit() # commit the transaction only if the email is sent successfully
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding employee No email was sent: {str(e)}")
        return jsonify({"error": "Error adding employee"}), 500
    
    logger.info(f"New Employee: {new_employee}")
    flash('Employee added successfully', 'success')
    return jsonify(new_employee.to_dict()), 201


    # Send SMS Notification to Admin
    # sms_notification = NotificationFactory.create_notification("sms")
    # sms_notification.send(current_user.phone, admin_message)

    # # send SMS Notification to employee
    # sms_notification.send(new_employee.phone, emp_welcome_message)



@employee_bp.route('/<employee_id>', methods=['GET'])
@token_required
def get_employee(current_user, employee_id):
    """Get an employee"""
    if current_user.role != 1:
        return jsonify({'message': 'Your are Not authorized to perform this action'}), 403

    #employee = storage.get(Employee, employee_id)
    # query from the database
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    return jsonify(employee.to_dict()), 200


@employee_bp.route('/<employee_id>', methods=['PUT'])
@token_required

# def update_employee(current_user, employee_id):
#     """Update an employee"""
#     if current_user.role != 1:
#         return jsonify({'message': 'Your are Not authorized to perform this action'}), 403

#     #employee = storage.get(Employee, employee_id)
#     # query from the database
#     employee = Employee.query.get(employee_id)
#     print(employee)
#     if not employee:
#         return jsonify({'error': 'Employee not found'}), 404
    
#     data = request.json


#     original_data = {
#         'name': employee.name,
#         'email': employee.email,
#         'phone': employee.phone,
#         'department': employee.department,
#         'start_date': employee.start_date,
#         'salary': employee.salary
#     }

#     # Store updated attributes
#     updated_fields = {}

#     # Update the employee's information and track changed fields
#     for key, value in data.items():
#         if hasattr(employee, key) and getattr(employee, key) != value:
#             setattr(employee, key, value)
#             updated_fields[key] = {
#                 'old': original_data.get(key),
#                 'new': value
#             }

#     # Save the updated employee
#     #storage.save()
#     db.session.commit()

#     logger.info('Employee updated successfully')
#     flash('Employee updated successfully', 'success')
#     return jsonify({'message': 'Employee updated successfully', 'employee': employee.to_dict()}), 200

@employee_bp.route('/check-in', methods=['POST'], endpoint='employee_check_in')
@employee_token_required
def check_in(current_user):
    """Employee check-in"""
    # Ensure the role is 'Employee' (role = 0 for employees)
    if current_user.role != 0:
        return jsonify({'message': 'You are not authorized to perform this action'}), 403
    
    # Check if the user has already checked in and not checked out
    existing_check_in = Attendance.query.filter_by(employee_id=current_user.id, check_out=None).first()
    
    current_time = datetime.now()
    if current_time.hour != 10 or current_time.minute != 0:
        return jsonify({'error': 'You can only check in between 10:00 and 10:15'}), 403
    
    if existing_check_in:
        return jsonify({'error': 'You have already checked in'}), 400
    
    # Record the check-in time
    check_in_record = Attendance(employee_id=current_user.id, check_in_time=datetime.now())
    db.session.add(check_in_record)
    db.session.commit()
    
    return jsonify({'message': 'You have successfully checked in', 'attendance': check_in_record.custom_dict()}), 201

@employee_bp.route('/check-out', methods=['POST'], endpoint='employee_check_out')
@employee_token_required
def check_out(current_user):
    """Employee check-out"""
    # Ensure the role is 'Employee' (role = 0 for employees)
    if current_user.role != 0:
        return jsonify({'message': 'You are not authorized to perform this action'}), 403
    
    # Check if the user has already checked in and not checked out
    existing_check_in = Attendance.query.filter_by(employee_id=current_user.id, check_out=None).first()
    
    if not existing_check_in:
        return jsonify({'error': 'You have not checked in'}), 400
    
    # Record the check-out time
    existing_check_in.check_out = datetime.now()
    db.session.commit()
    
    return jsonify({'message': 'You have successfully checked out', 'attendance': existing_check_in.custom_dict()}), 201