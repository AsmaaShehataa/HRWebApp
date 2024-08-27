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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

employee_bp = Blueprint('employee_bp', __name__, url_prefix='/employees')

# file_path = 'web_flask/static'
# Allowed_Extensions = {'png', 'jpg'}
# Max_Length = 1 * 1024 * 1024 # 1MB

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in Allowed_Extensions

@employee_bp.route('/', methods=['GET'])
def get_employees():
    """Get all employees"""
    employee_list = storage.all(Employee)
    logger.info('Employees retrieved successfully')
    return jsonify([employee.to_dict() for employee in employee_list.values()])


@employee_bp.route('/new', methods=['POST'])
def add_employee():
    """Add new employee"""
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
        'role': form.role.data,
        'admin_id': form.admin_id.data
        # 'photo': photo_url
    }

    required_fields = ['name', 'email', 'password', 'phone', 'department', 'start_date', 'salary', 'role', 'admin_id']
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
    new_employee.save()
    logger.info('Employee added successfully')
    flash('Employee added successfully', 'success')
    return jsonify(new_employee.to_dict()), 201
