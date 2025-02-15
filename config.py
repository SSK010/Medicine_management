import os

# Base directory for the app
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for Flask sessions (change this to something secret!)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'

# Database configuration
DB_PATH = os.path.join(BASE_DIR, 'database', 'stock.db')

# Twilio SMS credentials (for low stock alerts)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
ADMIN_PHONE_NUMBER = os.environ.get('ADMIN_PHONE_NUMBER')

# Other configurations can be added here as needed
