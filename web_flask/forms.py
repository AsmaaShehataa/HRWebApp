#!/usr/bin/python3
"""Forms for employees validation"""
from wtforms import Form, StringField, IntegerField, validators, DateField
from flask_wtf import FlaskForm
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
    role = StringField('Role', validators=[DataRequired()])
    #photo = StringField('Photo', validators=[DataRequired()])
    admin_id = StringField('Admin ID', validators=[DataRequired()])
