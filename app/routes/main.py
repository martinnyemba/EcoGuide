# app/routes/main.py
from flask import Blueprint, render_template, request, jsonify, url_for
# from app.models import Service, BlogPost
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """
    Renders the home page of the web application.

    This function serves as the view for the root URL of the web application.
    It renders the 'index.html' template with a context variable 'title'
    that is set to 'Home'.

    Returns:
        Response: A Flask Response object containing the rendered HTML of
        the home page.
    :return:
    """
    return render_template('index.html', title='Home')


@bp.route('/features')
def features():
    """Renders the Features page of the web application."""
    return render_template('features.html', title='Features')


@bp.route('/how')
def how():
    """Renders the How it works page of the web application."""
    return render_template('how-it-works.html', title='How It Works')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Renders the Contact me page of the web application."""
    return render_template('contact.html', title='Contact Us')