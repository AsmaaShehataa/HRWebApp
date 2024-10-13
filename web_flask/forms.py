#!/usr/bin/python3
"""Forms for employees and admins validation"""
from wtforms import Form, StringField, IntegerField, validators, DateField, PasswordField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp
import re

class EmployeeForm(FlaskForm):
    """Employee Form"""
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message='Invalid email')])
    password = StringField('Password', validators=[DataRequired(), Length(min=6)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=11)])
    department = StringField('Department', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired(), NumberRange(min=1, message='Salary must be a positive number')])
    #role = StringField('Role', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    #admin_id = StringField('Admin ID', validators=[DataRequired()])
    #head_employee_email = StringField('Head Employee Email', validators=[Email(), DataRequired()])
    head_employee_id = StringField('Head Employee ID', validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message='Invalid email')])
    password = StringField('Password', validators=[DataRequired(), Length(min=6)])

class AdminForm(FlaskForm):
    """Admin Form"""
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message='Invalid email')])
    password = StringField('Password', validators=[DataRequired(), Length(min=6)])
    role = IntegerField('Role', validators=[DataRequired(), NumberRange(min=0, max=1, message='Role must be 0 or 1')])

class AdminLoginForm(FlaskForm):
    """Admin Login Form"""
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message='Invalid email')])
    password = StringField('Password', validators=[DataRequired(), Length(min=6)])

class EmployeeUpdateForm(FlaskForm):
    """Employee Update Form"""
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message='Invalid email')])
    password = StringField('Password', validators=[DataRequired(), Length(min=6)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=11)])
    department = StringField('Department', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired(), NumberRange(min=1, message='Salary must be a positive number')])
    

class LeaveRequestForm(FlaskForm):
    """Leave Request Form"""
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message='Invalid email')])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    leave_type = StringField('Leave Type', validators=[DataRequired()])
    reason = StringField('Reason', validators=[DataRequired(), Length(max=1000)])
    leave_days = StringField('Leave Days', validators=[DataRequired()])
    