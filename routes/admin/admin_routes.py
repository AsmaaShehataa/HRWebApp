#!/usr/bin/python3
"""Admin routes"""
from flask import jsonify, request, abort, Blueprint
from models import storage
from models.admin import Admin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET'])
def get_admins():
    """Get all admins"""
    admins_list = storage.all(Admin)
    return jsonify([admin.to_dict() for admin in admins_list.values()])

logger.info('Admins retrieved successfully')
