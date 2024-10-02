#!/usr/bin/python3

"""Script for checking and sending reminders for those who haven't signed out"""
import os
import sys
from flask import Flask
from datetime import datetime, timedelta
import schedule

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#print(sys.path)

from models.attendance import Attendance
from models.employees import Employee
from extensions import db
from models.notifications.notification_factory import NotificationFactory
from models.notifications.email_notification import EmailNotification
from config import Config
from app import app

#not checked out only for this day not all the employees 
    #check in but not checked out (NULL) 
with app.app_context():

    # Attendance calculation
    today = datetime.now()
    # start_time = today - timedelta(minutes=2)
    # end_time = today
    start_time = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    end_time = today.replace(hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=1)
    
    # Getting all employees who haven't signed in or out
    missing_att_emp = db.session.query(Employee).outerjoin(Attendance).filter(
            (Attendance.check_in == None) | 
            (Attendance.check_in >= start_time) &
            (Attendance.check_in <= end_time) &
            (Attendance.check_out == None)
            ).all()

    # Send reminder via email
    if missing_att_emp:
        email_notify = NotificationFactory.create_notification("email")
        for emp in missing_att_emp:
            reminder_msg = (
                f"Hello {emp.name},\n"
                "This is a friendly reminder that you haven't checked in or checked out on the previous day. "
                "Please make sure to record your attendance accordingly.\n\n"
                "Thank you!"
            )
            email_notify.send(emp.email, "Attendance Reminder", reminder_msg)
        print(f"Sent Reminders to {len(missing_att_emp)} employees.")
    else:
        print("No reminders to send.")
