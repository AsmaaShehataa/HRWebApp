from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}/{}'.format(
        os.getenv('HR_MYSQL_USER'),
        os.getenv('HR_MYSQL_PWD'),
        os.getenv('HR_MYSQL_HOST'),
        os.getenv('HR_MYSQL_DB')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = 'web_flask/static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg'}
    