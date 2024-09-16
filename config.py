import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Database configuration
    HEROKU_POSTGRESQL_WHITE_URL = os.environ.get('HEROKU_POSTGRESQL_WHITE_URL')
    if HEROKU_POSTGRESQL_WHITE_URL and HEROKU_POSTGRESQL_WHITE_URL.startswith("postgres://"):
        HEROKU_POSTGRESQL_WHITE_URL = HEROKU_POSTGRESQL_WHITE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = HEROKU_POSTGRESQL_WHITE_URL or os.environ.get('DATABASE_URL') or 'sqlite:///ecoguide.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Docker configuration / Setting for Postgres

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
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'False').lower() in ['true', 'on', '1']


class DevelopmentConfig(Config):
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', 'on', '1']


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Disable CSRF protection during testing
    WTF_CSRF_ENABLED = False


# Dictionary to access configuration classes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# If the environment variable 'FLASK_CONFIG' is set, use it to select the configuration class
# Otherwise, use the default configuration class
config_name = os.environ.get('FLASK_CONFIG', 'default')
current_config = config[config_name]
