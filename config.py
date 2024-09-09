import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Secret Key Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. This is insecure.")

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('JAWSDB_MARIA_URL') or ('mysql+pymysql://kbacgzlnvt355vgc:flz36pkp28rlq6fw'
                                                                 '@uyu7j8yohcwo35j3.cbetxkdyhwsb.us-east-1.rds'
                                                                 '.amazonaws.com:3306/w66f0g9tyenpt50b')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Carbon Interface API key
    CARBON_INTERFACE_API_KEY = os.environ.get('CARBON_INTERFACE_API_KEY')

    # OpenWeatherMap API key for weather and AQI
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')

    # Twilio configuration
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
