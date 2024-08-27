from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
# from app.models import Service, BlogPost
from app import db
from datetime import datetime

bp = Blueprint('user', __name__)


@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard"""
    return render_template('user/dashboard.html')


