import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Secret Key Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. This is insecure.")

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ecoguide.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    if not MAIL_SERVER or not MAIL_USERNAME or not MAIL_PASSWORD or not MAIL_DEFAULT_SENDER:
        raise ValueError("Email configuration is not set properly. Please check your environment variables.")

    # Carbon Interface API key
    CARBON_INTERFACE_API_KEY = os.environ.get('CARBON_INTERFACE_API_KEY')
    if not CARBON_INTERFACE_API_KEY:
        raise ValueError("CARBON_INTERFACE_API_KEY is not set. Please set the environment variable.")

    # OpenWeatherMap API key for weather and AQI
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')
    if not OPENWEATHERMAP_API_KEY:
        raise ValueError("OPENWEATHERMAP_API_KEY is not set. Please set the environment variable.")