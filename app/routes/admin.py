from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
# from app.models import Booking, Service, User, Role
from app import db
from app.utils import admin_required
from datetime import datetime

bp = Blueprint('admin', __name__)

@bp.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')