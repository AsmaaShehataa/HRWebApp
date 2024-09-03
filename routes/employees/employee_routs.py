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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

employee_bp = Blueprint('employee_bp', __name__, url_prefix='/employees')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token is missing'}), 403
        
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            admin = storage.filter_by(Admin, email=data['email'])
            logger.info(f"Decoded email from token: {data['email']}")
            current_user = storage.filter_by(Admin, email=data['email'])

            if not current_user:
                return jsonify({'error': 'User not found'}), 403
        except Exception as e:
            logger.error('Token is invalid')
            return jsonify({'error': 'Token is invalid'}), 403
        return f(current_user[0], *args, **kwargs)
    return decorated

@employee_bp.route('/', methods=['GET'])
@token_required
def get_employees(): #work with token
    employee_list = storage.all(Employee)
    logger.info('Employees retrieved successfully')
    return jsonify([employee.to_dict() for employee in employee_list.values()])


@employee_bp.route('/new', methods=['POST'])
@token_required
def add_employee(current_user): #work with token
    """Add new employee"""
    # cehck if the user is an admin
    logger.info(f"Current user: {current_user}")
    if current_user.role != 1:
        return jsonify({'message': 'Your are Not authorized to perform this action'}), 403
    
    form = EmployeeForm()
    if not form.validate_on_submit():
        return jsonify({"errors": form.errors}), 400
    
    # Handle file upload (commented out for now)
    # file = request.files.get('photo')
    # photo_url = None
    # if file and allowed_file(file.filename):
    #     if len(file.read()) > Max_Length:
    #         return jsonify({"error": "File size exceeds 1MB limit."}), 400
    #     file.seek(0)
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join('web_flask/static', filename))
    #     photo_url = os.path.join(file_path, filename)
    # elif file:
    #     return jsonify({"error": "Invalid file type."}), 400
        
    # Get data from the form
    data = {
        'name': form.name.data,
        'email': form.email.data,
        'password': form.password.data,
        'phone': form.phone.data,
        'department': form.department.data,
        'start_date': form.start_date.data,
        'salary': form.salary.data,
        # 'photo': photo_url
    }

    required_fields = ['name', 'email', 'password', 'phone', 'department', 'start_date', 'salary']
    for field in required_fields:
        if field not in data or not data[field]:
            abort(400, 'Missing {}'.format(field))

    # check if the employee already exists
    existing_employee = storage.all(Employee)
    for emp in existing_employee.values():
        if emp.email == form.email.data:
            flash('Employee already exists', 'danger')
            return jsonify({"error": "Employee already exists"}), 400

    new_employee = Employee(**data)
    new_employee.password = generate_password_hash(data['password'])
    new_employee.save()
    logger.info('Employee added successfully')
    flash('Employee added successfully', 'success')
    return jsonify(new_employee.to_dict()), 201
