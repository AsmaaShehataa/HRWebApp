from flask import Blueprint, jsonify, request, abort, flash
from models import storage
from models.admin import Admin
from models.employees import Employee
from web_flask.forms import LoginForm
from web_flask.forms import AdminLoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from config import Config
import logging
import hashlib
import os
from werkzeug.security import generate_password_hash
import jwt
from config import Config
from functools import wraps
from os import getenv
from extensions import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/check')




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
            print(admin)
            logger.info("Auth routes")
            logger.info(f"Decoded email from token: {data['email']}")
            current_admin = storage.filter_by(Admin, email=data['email'])
            if not current_admin:
                return jsonify({'error': 'User not found'}), 403
        except Exception as e:
            logger.error('Token is invalid')
            return jsonify({'error': 'Token is invalid'}), 403
        return f(current_admin, *args, **kwargs)
    return decorated


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    form = LoginForm()
    if not form.validate_on_submit():
        return jsonify({'error': form.errors}), 400

    data = {
        'email': form.email.data,
        'password': form.password.data,
    }

    # Required fields for user creation
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            abort(400, f'Missing {field}')
        
    # Check if the user exists
    existing_emp = Employee.query.filter_by(email=form.email.data).first()
    
    if existing_emp:
        logger.info(f'Found user: {existing_emp.email}')
        logger.info(f'Checking password: stored: {existing_emp.password}, entered: {form.password.data}')

        
        if check_password_hash(existing_emp.password, form.password.data):
            token = jwt.encode({'email': existing_emp.email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, Config.SECRET_KEY)
            flash('Login successful')
            logger.info(f'user: {existing_emp}')
            return jsonify({'token': token})
        else:
            logger.warning('Password mismatch')
            return jsonify({'error': 'Invalid username or password'}), 400

    logger.warning('User not found')
    # Create a new user
    new_emp = Employee(**data)
    new_emp.password = generate_password_hash(data['password'])
    new_emp.add(new_emp)
    db.session.commit()

    token = jwt.encode({'email': new_emp.email,'id': new_emp.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, Config.SECRET_KEY)
    logger.info('User created successfully')
    return jsonify({'token': token})


# @auth_bp.route('/adminlogin', methods=['POST'])
# def admin_login():
#     """Login Admin"""
#     form = AdminLoginForm()
#     if not form.validate_on_submit():
#         return jsonify({'error': form.errors}), 400

#     data = {
#         'email': form.email.data,
#         'password': form.password.data,
#     }

#     # print the email being passed with a query
#     logger.info(f'Email: {data["email"]}')
#     logger.info(f'Password: {data["password"]}')

#     # Required fields for user creation
#     required_fields = ['email', 'password']
#     for field in required_fields:
#         if field not in data or not data[field]:
#             abort(400, f'Missing {field}')
        
#     # Check if the user exists
#     email_to_check = data['email'].strip().lower()
#     all_admin = storage.all(Admin)
#     existing_admin = [admin for admin in all_admin if admin.email == email_to_check]
#     #logger.info(f'Found user: {existing_admin}')
    
#     if existing_admin:
#         # access the first element of the list
#         admin = existing_admin[0]
#         logger.info(f"Retrieved email: {admin.email}, retrieved hashed password: {admin.password}")

#         if check_password_hash(admin.password, form.password.data):
#             logger.info('Email and Password match')
#             flash('Login successful')
#         else:
#             logger.warning("The email or hashed password does not match.")
#             return jsonify({'token': token})
#     else:
#         logger.warning("No admin found with this email.")

#     # admins_email = [admin.email for admin in existing_admin]
#     # logger.info(f'Found user: {admins_email}')
#     exit()
    
#     if existing_admin and len(existing_admin) == 1:
#         existing_admin = existing_admin[0]  # Since it's a list, access the first element
#         logger.info(f'Found user: {existing_admin.email}')

#         logger.info('Checking password', existing_admin.password, form.password.data)
#         if check_password_hash(existing_admin.password, form.password.data):
#             token = jwt.encode({'email': existing_admin.email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, Config.SECRET_KEY)
#             flash('Login successful')
#             return jsonify({'token': token})
#         else:
#             logger.warning('Password mismatch')
#             logger.warning('User not found')
#             return jsonify({'error': 'Invalid username or password'}), 400
#     else:
#         logger.warning('Admin not found')
        
#     exit()
#         # Create a new admin
#         # new_admin = Admin(**data)
#         # new_admin.password = generate_password_hash(data['password'])
#         # new_admin.save()
#         # token = jwt.encode({'email': new_admin.email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, Config.SECRET_KEY)
#         # logger.info('Admin created successfully')
#         # flash('User created successfully')
    
#         # return jsonify({'token': token})
@auth_bp.route('/adminlogin', methods=['POST'])
def admin_login():
    """Login Admin"""
    form = AdminLoginForm()
    if not form.validate_on_submit():
        return jsonify({'error': form.errors}), 400

    data = {
        'email': form.email.data,
        'password': form.password.data,
    }

    admin = storage.filter_by(Admin, email=data['email'])

    if admin:
        existing_admin = admin[0]
        logger.info(f'Found user: {existing_admin.email}')


        #logger.info('Checking password', existing_admin.password, form.password.data)
        logger.info(f'Checking password: stored: {existing_admin.password}, entered: {form.password.data}')
        logger.info(generate_password_hash(data['password']))

        if check_password_hash(existing_admin.password, form.password.data):
            logger.info('Email and Password match')
            token = jwt.encode({'email': existing_admin.email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, Config.SECRET_KEY)
            logger.info('Login successful')
            flash('Login successful')
            return jsonify({'token': token})
        else:
            logger.warning('Password mismatch')
            return jsonify({'error': 'Invalid username or password'}), 400
    exit()
    logger.warning('User not found, creating new user')
  
    # Create a new user
    new_admin = Admin(**data)
    new_admin.password = generate_password_hash(data['password'])
    new_admin.save()
    token = jwt.encode({'email': new_admin.email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, Config.SECRET_KEY)
    logger.info('User created successfully')
    flash('User created successfully')
    
    return jsonify({'token': token})