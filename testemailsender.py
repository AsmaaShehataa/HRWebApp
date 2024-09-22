from app import app
from models.settings import Settings
from extensions import db

# Open a new application context
with app.app_context():
    # Check if the setting already exists
    existing_setting = Settings.query.filter_by(key="email_sender").first()
    
    if existing_setting:
        # If it exists, update the value
        existing_setting.value = "asmaa_shihata@yahoo.com"
    else:
        # If it does not exist, create a new entry
        email_setting = Settings(key="email_sender", value="asmaa_shihata@yahoo.com")
        db.session.add(email_setting)
    
    # Commit the transaction
    db.session.commit()
    
    # Query to verify
    result = Settings.query.filter_by(key="email_sender").first()
    print(result.value)  # This should print 'asmaa_shihata@yahoo.com'
