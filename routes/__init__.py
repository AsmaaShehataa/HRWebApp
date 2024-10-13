# routes/__init__.py
"""Routes Initialization"""
from flask import Flask
#from routes.admin.admin_routes import admin_bp
from routes.employees.employee_routs import employee_bp
from routes.auth.auth_routes import auth_bp
from routes.employees.leaves import leaves_blueprint
from routes.employees.managers_routes import managers_blueprint

def register_routes(app):
    """Register all routes"""
    #app.register_blueprint(admin_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(leaves_blueprint)
    app.register_blueprint(managers_blueprint)
