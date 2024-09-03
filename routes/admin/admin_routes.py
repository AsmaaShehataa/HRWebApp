# #!/usr/bin/python3
# """Admin routes"""
# from flask import jsonify, request, abort, Blueprint, flash
# from models import storage
# from models.admin import Admin
# import logging
# from flask import Flask
# from web_flask.forms import EmployeeForm
# from web_flask.forms import AdminForm
# import os
# from werkzeug.security import generate_password_hash
# import jwt
# from config import Config
# from datetime import datetime, timedelta
# from functools import wraps

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admins')

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return jsonify({'error': 'Token is missing'}), 403
        
#         try:
#             token = auth_header.split(" ")[1]
#             data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256']) 
#             admin = storage.filter_by(Admin, email=data['email'])
#             print(admin)
#             current_user = storage.filter_by(Admin, email=data['email'])
#             if not current_user or len(current_user) == 0:
#                 return jsonify({'error': 'User not found'}), 403
#             current_user = current_user[0]
#             logger.info(f"User Found {current_user}")

#         except jwt.ExpiredSignatureError:
#             logger.error('Token is expired')
#             return jsonify({'error': 'Token is expired'}), 403
#         except jwt.InvalidTokenError:
#             logger.error('Token is invalid')
#             return jsonify({'error': 'Token is invalid'}), 403
#         return f(current_user, *args, **kwargs)
#     return decorated


# @admin_bp.route('/all', methods=['GET'])
# @token_required
# def get_admins():
#     """Get all admins"""
#     admins_list = storage.all(Admin)
#     logger.info('Admins retrieved successfully')
#     return jsonify([admin.to_dict() for admin in admins_list.values()])

# logger.info('Admins retrieved successfully')

# # @admin_bp.route('/new', methods=['POST'])
# # @token_required
# # def add_admin(current_user):
# #     """Add new admin"""
# #     #cehck if the user is an admin
# #     if current_user.role != 1:
# #         return jsonify({'message': 'Your are Not authorized to perform this action'}), 403
    
# #     form = AdminForm()
# #     if not form.validate_on_submit():
# #         return jsonify({"errors": form.errors}), 400
    
# #     data = {
# #         'name': form.name.data,
# #         'email': form.email.data,
# #         'password': form.password.data,
# #         'role': form.role.data
# #     }
# #     required_fields = ['name', 'email', 'password', 'role']
# #     for field in required_fields:
# #         if field not in data or not data[field]:
# #             abort(400, 'Missing{}'.format(field))
    
# #     # Check if the admin exists
# #     existing_admin = storage.filter_by(Admin, email=data['email'])
# #     if existing_admin:
# #         logger.info(f'Found admin: {existing_admin.email}')
# #         return jsonify({'error': 'Admin already exists'}), 400

# #     new_admin = Admin(**data)
# #     new_admin.password = generate_password_hash(data['password'])
# #     new_admin.save()
# #     token = jwt.encode({'email': new_admin.email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, Config.SECRET_KEY)
# #     logger.info('Admin created successfully')
# #     flash('Admin created successfully')
# #     #return jsonify({'token': token})
# #     return jsonify(new_admin.to_dict()), 201
