#!/usr/bin/python3
"""Manager Route to View Pending Leave Requests"""

from flask import jsonify, request, abort, Blueprint
from functools import wraps
from models.leave_request import LeaveRequest
from models.employees import Employee
from datetime import datetime
from flask import Flask
from extensions import db
from config import Config
import jwt
import logging
from models.notifications.notification_factory import NotificationFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

managers_blueprint = Blueprint('managers_blueprint', __name__, url_prefix='/managers')

def managers_token_required(f):
      @wraps(f)
      def decorated(*args, **kwargs):
          logger.info("Hello world")
  
          auth_header = request.headers.get('Authorization')
          if not auth_header:
              return jsonify({'error': 'Token is missing'}), 403
          
          try:
              token = auth_header.split(" ")[1]
              data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
              logger.info("Managers route")
              logger.info(f"Decoded email from token: {data['email']}")
              
              
              
              current_user = Employee.query.filter_by(email=data['email']).first()
              
              if not current_user:
                  return jsonify({'error': 'User not found'}), 403
              logger.info(f"User found: {current_user.name} with role {current_user.role}")
  
          except Exception as e:
              logger.error(f'Token is invalid: {str(e)}')
              return jsonify({'error': 'Token is invalid'}), 403
          return f(current_user, *args, **kwargs)
      return decorated

@managers_blueprint.route('/pending_leave_request', methods=['GET'])
@managers_token_required
def view_pending_leaves(current_user):
  """View leaves requests from employees under the team's manager"""
  
  logger.info(current_user)
  # current user is a Manager 
  if current_user.role != 3: # manager ID
    return jsonify({'message': 'Only managers can view pending leave requests'}), 403
  
  # Get the employees under this manager
  supervised_employees = Employee.query.filter_by(head_employee_id = current_user.id).all()
  if not supervised_employees:
    return jsonify({'message': 'No employees under your supervision'}), 404
  
  # Get the pending leave requests from the supervised employees
  employees_ids = [emp.id for emp in supervised_employees]
  pending_leaves = LeaveRequest.query.filter(LeaveRequest.employee_id.in_(employees_ids), LeaveRequest.status == 0).all()
  
  if not pending_leaves:
    return jsonify({'message': 'No pending leave requests from your supervised employees'}), 404

  # Return the pending leave requests
  leave_req = [request.to_dict() for request in pending_leaves]
  return jsonify({"Pending_leave_requests": leave_req}), 200


@managers_blueprint.route('/approve_leaves/<leave_id>', methods=['POST'])
@managers_token_required
def approve_leave(current_user, leave_id):
  """Approve leave req by the manager"""
  
  if current_user.role != 3:
    return jsonify({'message': 'Only managers can approve leave requests'}), 403
  
  # going through 3 levels; fetch for leaves to be approved by this manager, approve or reject
  
  leave_request = LeaveRequest.query.get(leave_id)
  if not leave_request:
    return jsonify({'message': 'No Leave requests to be shown'}), 404
  
  # checking if this is the manager of this team
  supervised_employee = Employee.query.filter_by(id = leave_request.employee_id, head_employee_id = current_user.id).first()
  if not supervised_employee:
    return jsonify({'message': 'You are not authurized to approve this leave request'}), 403
  
  # Approve the leave request
  leave_request.status = 1 # for approval
  leave_request.approved_by = current_user.id
  db.session.commit()
  
  logger.debug(f"Preparing to send approval email to employee {supervised_employee.email}")

  #send notification email with approval
  try:
    email_notification = NotificationFactory.create_notification("email")
    email_subject = "Leave Request Approved"
    email_message = (f"Dear {supervised_employee.name},\n\n"
                        f"Your leave request from {leave_request.start_date.strftime('%Y-%m-%d')} to {leave_request.end_date.strftime('%Y-%m-%d')} "
                        "has been approved by your manager.\n\n"
                        "Best regards,\n"
                        )
    logger.debug(f"Email details - To: {supervised_employee.email}, Subject: {email_subject}, Message: {email_message}")

    email_notification.send(supervised_employee.email, email_subject, email_message)
    logger.info(f"Leave request email sent to employee {supervised_employee.email}")
  except Exception as email_error:
    logger.error(f"Failed to send leave email to employee: {str(email_error)}")
  
  return jsonify({'message': "Leave request approved successfully", "leave_request": leave_request.to_dict()}), 200


@managers_blueprint.route('/reject_leave/<leave_id>', methods=['POST'])
@managers_token_required
def reject_leave(current_user, leave_id):
  """Reject leave req by the manager"""
  
  if current_user.role != 3:
    return jsonify({'message': 'Only managers can approve leave requests'}), 403

  leave_request = LeaveRequest.query.get(leave_id)
  if not leave_request:
    return jsonify({'message': 'No Leave requests to be shown'}), 404

  supervised_employee = Employee.query.filter_by(id = leave_request.employee_id, head_employee_id = current_user.id).first()
  if not supervised_employee:
    return jsonify({'message': 'You are not authurized to reject this leave request'}), 403

  leave_request.status = 2 # for rejecting
  leave_request.approved_by = current_user.id
  db.session.commit()
  
  logger.info("Leave rejected")
  return jsonify({'message': "Unfortunately your leave is rejected due to Business need", "leave_request": leave_request.to_dict()}), 200
