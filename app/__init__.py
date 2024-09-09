#!/usr/bin/env python
"""Module for the Flask Application Factory"""
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from jinja2 import TemplateNotFound

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
mail = Mail()
bcrypt = Bcrypt()
csrf = CSRFProtect()


def create_app(config_class=Config):
    """
    Function to create the Flask application.
    Initializes the Flask app with the provided configuration.
    Initializes the database, migrations, bcrypt, login manager, and mail extensions.
    Registers the blueprints for the main, auth, user, and admin routes.
    Registers the error handlers for 404, 500, and 403 errors.
    Registers the user loader for the login manager.
    :param config_class:
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    # Register error handlers
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {str(e)}")
        return render_template('errors/500.html'), 500

    @app.errorhandler(TemplateNotFound)
    def handle_template_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @login.user_loader
    def load_user(user_id):
        """
        Function to handle logins and load the user from the database.
        """
        from app.models import User
        return User.query.get(int(user_id))

    from app.routes import main, auth, user, admin
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(admin.bp)

    with app.app_context():
        db.create_all()

    return app
