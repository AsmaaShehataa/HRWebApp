#!/usr/bin/python3
"""Employees routes"""
from flask import jsonify, request, abort, Blueprint
from models import storage
from models.employees import Employee
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


employee_bp = Blueprint('employee_bp', __name__, url_prefix='/employees')


@employee_bp.route('/', methods=['GET'])
def get_emplooyees():
    """Get all employees"""
    employee_list = storage.all(Employee)
    return jsonify([employee.to_dict() for employee in employee_list.values()])

logger.info('Employees retrieved successfully')
