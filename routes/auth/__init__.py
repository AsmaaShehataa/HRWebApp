# routes/__init__.py
"""Routes Initialization"""
from flask import Flask
#from routes.admin.admin_routes import admin_bp
from routes.employees.employee_routs import employee_bp
from routes.auth.auth_routes import auth_bp

def register_routes(app):
    """Register Auth routes"""
    app.register_blueprint(auth_bp)
