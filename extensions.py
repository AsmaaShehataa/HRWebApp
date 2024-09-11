from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

mail = Mail()
def init_app(app):
    mail.init_app(app)

db = SQLAlchemy()