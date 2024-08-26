# routes/__init__.py
"""Routes Initialization"""
from flask import Flask
from routes.admin.admin_routes import admin_bp
from routes.employees.employee_routs import employee_bp

def register_routes(app):
    """Register all routes"""
    app.register_blueprint(admin_bp)
    app.register_blueprint(employee_bp)
