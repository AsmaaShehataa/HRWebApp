#!/usr/bin/python3

"""Leave Request APIs"""

from flask import Blueprint, request, jsonify
from extensions import db
from models.leave_request import LeaveRequest
from models.employees import Employee
from config import Config
from functools import wraps
from datetime import datetime, timedelta
from web_flask.forms import LeaveRequestForm
import jwt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

leaves_blueprint = Blueprint('leaves_blueprint', __name__, url_prefix='/employees')

def employee_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token is missing'}), 403
        
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            logger.info("Leaves route")
            logger.info(f"Decoded email from token: {data['email']}")
            current_user = Employee.query.filter_by(email=data['email']).first()
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 403
        except Exception as e:
            logger.error(f'Token is invalid: {str(e)}')
            return jsonify({'error': 'Token is invalid'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@leaves_blueprint.route('/leave_request', methods=['POST'])
@employee_token_required
def submit_leave_request(current_user):
    """Submit a leave for a logged-in employee"""

    if current_user.role != 0:
        return jsonify({'message': 'Only employees can submit leave requests through this link'}), 403

    form = LeaveRequestForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    # Employee duration check
    today = datetime.today()
    employment_duration = today - current_user.start_date

    # Ensure the employee has been with the company for at least 3 months
    if employment_duration < timedelta(days=90):
        return jsonify({'error': 'You need to be employed for at least 3 months before requesting leave'}), 403

    # Submit leave request
    try:
        new_leave_request = LeaveRequest(
            employee_id=current_user.id,
            email=current_user.email,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            leave_type=form.leave_type.data,
            reason=form.reason.data,
            leave_days=form.leave_days.data,
            status=0  # 0 = pending
        )
        db.session.add(new_leave_request)
        db.session.commit()

        logger.info(f'Leave request submitted by employee {current_user.email}')
        return jsonify({"message": "Leave request submitted successfully", "leave_request": new_leave_request.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f'Error submitting leave request: {str(e)}')
        return jsonify({"error": "Error submitting leave request", "details": str(e)}), 500
