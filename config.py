import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Database configuration
    HEROKU_POSTGRESQL_WHITE_URL = os.environ.get('HEROKU_POSTGRESQL_WHITE_URL')
    if HEROKU_POSTGRESQL_WHITE_URL and HEROKU_POSTGRESQL_WHITE_URL.startswith("postgres://"):
        HEROKU_POSTGRESQL_WHITE_URL = HEROKU_POSTGRESQL_WHITE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = HEROKU_POSTGRESQL_WHITE_URL or 'sqlite:///ecoguide.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Carbon Interface API key
    CARBON_INTERFACE_API_KEY = os.environ.get('CARBON_INTERFACE_API_KEY')

    # OpenWeatherMap API key for weather and AQI
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')

    # Logging configuration
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')



class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}