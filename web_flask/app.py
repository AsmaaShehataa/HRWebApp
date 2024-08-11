#!/usr/bin/python3
"""Script to generate flask app server and sentry"""

import sentry_sdk
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from web_flask.blueprints.bpuser import bpuser
from models import storage
from models.user import User


# Initialize Sentry SDK with performance monitoring
sentry_sdk.init(
    dsn="https://871fda2ea18cf0357d48aeaa965a06fc@o4507736600084480.ingest.us.sentry.io/4507737031114752",
    traces_sample_rate=1.0,  # Capture 100% of transactions for monitoring
    profiles_sample_rate=1.0  # Profile 100% of sampled transactions (adjust in production)
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Register blueprints
app.register_blueprint(bpuser)

@app.teardown_appcontext
def close_db(error):
    """Close the database connection"""
    storage.close()

@app.route('/', methods=['GET'])
def home():
    
    return "<p>Welcome Home Page!</p>"

@app.route('/HrWeb/user/all', methods=['GET'])
def get_users():
    """Get all users"""
    users = storage.all(User).values()
    users_list = []
    
    for user in users:
            user_dict = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'password': user.password,
            'phone': user.phone,
            'department': user.department,
            'start_date': user.start_date.isoformat(),
            'role': user.role
        }
            users_list.append(user_dict)
            print("Data retrieved successfully")

    return jsonify(users_list)

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
