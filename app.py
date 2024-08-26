#!/usr/bin/python3
"""Script to generate flask app server and sentry"""

import sentry_sdk
import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
#from web_flask.blueprints.bpuser import bpuser
from models import storage
import logging
from config import Config
from routes import register_routes
from models.settings import Settings
from models.employees import Employee
from models.admin import Admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Sentry SDK with performance monitoring
sentry_sdk.init(
    dsn="https://871fda2ea18cf0357d48aeaa965a06fc@o4507736600084480.ingest.us.sentry.io/4507737031114752",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0
)

# Load environment variables
load_dotenv()

# print(os.getenv('HR_MYSQL_USER'))
# print(os.getenv('HR_MYSQL_PWD'))
# print(os.getenv('HR_MYSQL_HOST'))
# print(os.getenv('HR_MYSQL_DB'))

app = Flask(__name__)
app.config.from_object('config')

# Register routes
register_routes(app)


# Initialize Flask Seeder 
seeder = FlaskSeeder()
seeder.init_app(app, storage._DBStorage__session)

# Initialize Flask Migrate
migrate = Migrate(app, storage.get_engine())

@app.teardown_appcontext
def close_db(error):
    """Close the database connection"""
    storage.close()

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
