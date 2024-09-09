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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

employee_bp = Blueprint('employee_bp', __name__, url_prefix='/employees')

# Define the allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg'}
UPLOAD_FOLDER = 'web_flask/static/uploads'

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
            logger.info(f"Decoded email from token: {data['email']}")
            current_user = storage.filter_by(Admin, email=data['email'], first_param=True)

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
    data = {
        'name': form.name.data,
        'email': form.email.data,
        'password': form.password.data,
        'phone': form.phone.data,
        'department': form.department.data,
        'start_date': form.start_date.data,
        'salary': form.salary.data,
        'photo': photo_url if photo_url else None
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

    new_employee = Employee(**data)
    #new_employee.password = generate_password_hash(data['password']) #--> set the password and return the hashed
    #new_employee.set_password(data['password']) --> ignore this bec settattr is already implemented in the model and will generate the password hash
    new_employee.save()
    logger.info('Employee added successfully')
    flash('Employee added successfully', 'success')
    return jsonify(new_employee.to_dict()), 201

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
def update_employee(current_user, employee_id):
    """Update an employee"""
    if current_user.role != 1:
        return jsonify({'message': 'Your are Not authorized to perform this action'}), 403

    #employee = storage.get(Employee, employee_id)
    # query from the database
    employee = Employee.query.get(employee_id)
    print(employee)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    data = request.json


    original_data = {
        'name': employee.name,
        'email': employee.email,
        'phone': employee.phone,
        'department': employee.department,
        'start_date': employee.start_date,
        'salary': employee.salary
    }

    # Store updated attributes
    updated_fields = {}

    # Update the employee's information and track changed fields
    for key, value in data.items():
        if hasattr(employee, key) and getattr(employee, key) != value:
            setattr(employee, key, value)
            updated_fields[key] = {
                'old': original_data.get(key),
                'new': value
            }

    # Save the updated employee
    #storage.save()
    db.session.commit()
    flash('Employee updated successfully', 'success')
    logger.info('Employee updated successfully')
    return jsonify({'message': 'Employee updated successfully', 'employee': employee.to_dict()}), 200
