from flask import Blueprint, render_template, request, jsonify, url_for
# from app.models import Service, BlogPost
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register')
def register():
    """Register"""
    return render_template('auth/register.html', title='Register')