#!/usr/bin/env python
"""Module for configuring Flask application instance"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
mail = Mail()
csrf = CSRFProtect()


def create_app(config_class=Config):
    """
    This function creates and configures a Flask application instance.

    Parameters:
    config_class (Config): An instance of the configuration class. Defaults to Config.

    Returns:
    app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from app.routes import main, auth, user, admin
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(admin.bp)

    # Logging configuration
    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('EcoGuide startup')

    with app.app_context():
        from app.models import Role
        db.create_all()
        Role.insert_roles()

    return app


# Import models at the end to avoid circular imports
from app import models
