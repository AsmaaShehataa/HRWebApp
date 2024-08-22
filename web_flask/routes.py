from flask import Blueprint, request, jsonify, abort
from models import storage
from models.user import User
import logging
from flask import Flask


logger = logging.getLogger(__name__)

bpuser = Blueprint('bpuser', __name__, url_prefix='/HrWeb/user')


@bpuser.route('/all', methods=['GET'])
def get_users():
    """Get all users"""
    users = storage.all(User).values()
    users_list = [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'password': user.password,
            'phone': user.phone,
            'department': user.department,
            'start_date': user.start_date.isoformat(),
            'role': user.role,
            'deleted_at': user.deleted_at.isoformat() if user.deleted_at else None
        }
        for user in users
    ]
    logger.info("Data retrieved successfully")
    return jsonify(users_list)

@bpuser.route('/active', methods=['GET'])
def get_active_users():
    """Get all active users only"""
    users = storage.all(User).values()
    active_users_list = [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'password': user.password,
            'phone': user.phone,
            'department': user.department,
            'start_date': user.start_date.isoformat(),
            'role': user.role
        }
        for user in users if user.deleted_at is None
    ]
    logger.info("Data retrieved successfully")
    return jsonify(active_users_list)

def register_routes(app):
    """Register all routes with the Flask app"""
    app.register_blueprint(bpuser)
