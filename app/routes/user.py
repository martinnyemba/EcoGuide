#!/usr/bin/env python
"""User Blueprint and Routes for the user pages."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.carbon_interface import get_carbon_estimate
from app.forms import ChangePasswordForm, UpdateAddressForm, UpdateProfileForm, EstimateForm
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Address, User
from app.utils import calculate_footprint
from datetime import datetime
import random
from app.weather import get_weather_and_aqi

bp = Blueprint('user', __name__)

# Generate random tips
tips = [
    "Turn off lights when not in use to save energy.",
    "Use a reusable coffee cup to reduce waste.",
    "Unplug electronics when not in use to avoid phantom energy consumption.",
    "Choose products with minimal packaging to reduce waste.",
    "Start a small garden to grow your own vegetables.",
    "Opt for public transportation, biking, or walking instead of driving.",
    "Install energy-efficient appliances and light bulbs.",
    "Reduce water usage by fixing leaks and using water-saving fixtures.",
    "Support local and sustainable businesses.",
    "Compost kitchen scraps to reduce landfill waste.",
    "Use a programmable thermostat to optimize heating and cooling.",
    "Plant trees to absorb CO2 and provide shade.",
    "Reduce meat consumption and opt for plant-based meals.",
    "Recycle and properly dispose of hazardous materials.",
    "Educate others about the importance of sustainability."
]


@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard"""
    return render_template('user/dashboard.html')


@bp.route('/carbon_estimate', methods=['GET', 'POST'])
def carbon_estimate():
    form = EstimateForm()
    if form.validate_on_submit():
        estimate_type = form.estimate_type.data
        data = form.data
        result = get_carbon_estimate(estimate_type, data)
        return jsonify(result)
    return render_template('user/estimates.html', form=form)


@bp.route('/impact_calculator')
@login_required
def impact_calculator():
    """Impact Calculator"""
    actions = [
        {"name": "Recycle plastic", "impact": 5, "category": "Waste"},
        {"name": "Use public transport", "impact": 8, "category": "Transportation"},
        {"name": "Reduce meat consumption", "impact": 7, "category": "Food"},
        {"name": "Use renewable energy", "impact": 10, "category": "Energy"},
        {"name": "Compost food waste", "impact": 6, "category": "Waste"},
        {"name": "Use a reusable water bottle", "impact": 4, "category": "Waste"},
        {"name": "Plant a tree", "impact": 9, "category": "Environment"},
        {"name": "Use energy-efficient appliances", "impact": 7, "category": "Energy"},
        {"name": "Buy local produce", "impact": 6, "category": "Food"},
        {"name": "Carpool to work", "impact": 8, "category": "Transportation"},
        {"name": "Use cloth bags for shopping", "impact": 5, "category": "Waste"},
        {"name": "Take shorter showers", "impact": 6, "category": "Water"},
        {"name": "Use a bike for short trips", "impact": 7, "category": "Transportation"},
        {"name": "Donate unused items", "impact": 5, "category": "Waste"},
        {"name": "Use natural cleaning products", "impact": 4, "category": "Environment"}
    ]

    random_tips = random.sample(tips, 3)

    return render_template('user/impact_calculator.html', actions=actions, tips=random_tips)


@bp.route('/carbonfootprint', methods=['GET', 'POST'])
@login_required
def calculator():
    if request.method == 'POST':
        # Handle form submission
        data = request.form

        # Perform calculations
        result = calculate_footprint(data)

        return jsonify(result=result)

    return render_template('user/calculator.html')


@bp.route('/profile')
@login_required
def profile():
    update_profile_form = UpdateProfileForm()
    change_password_form = ChangePasswordForm()
    update_address_form = UpdateAddressForm()

    # Pre-fill the update profile form with current user data
    update_profile_form.username.data = current_user.username
    update_profile_form.email.data = current_user.email
    update_profile_form.first_name.data = current_user.first_name
    update_profile_form.last_name.data = current_user.last_name
    update_profile_form.phone_number.data = current_user.phone_number

    # Pre-fill the address form if the user has an address
    if current_user.address:
        update_address_form.street.data = current_user.address.street
        update_address_form.city.data = current_user.address.city
        update_address_form.state.data = current_user.address.state
        update_address_form.country.data = current_user.address.country

    return render_template('user/profile.html',
                           update_profile_form=update_profile_form,
                           change_password_form=change_password_form,
                           update_address_form=update_address_form)


@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        return jsonify({
            'success': True,
            'username': current_user.username,
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'phone_number': current_user.phone_number or 'Not provided'
        })
    return jsonify({'success': False, 'errors': form.errors}), 400


@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.current_password.data):
            current_user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated.', 'success')
        else:
            flash('Incorrect current password.', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", 'danger')
    return redirect(url_for('profile'))


@bp.route('/update_address', methods=['POST'])
@login_required
def update_address():
    form = UpdateAddressForm()
    if form.validate_on_submit():
        if current_user.address:
            current_user.address.street = form.street.data
            current_user.address.city = form.city.data
            current_user.address.state = form.state.data
            current_user.address.country = form.country.data
        else:
            new_address = Address(
                user_id=current_user.id,
                street=form.street.data,
                city=form.city.data,
                state=form.state.data,
                country=form.country.data
            )
            db.session.add(new_address)
        db.session.commit()
        flash('Your address has been updated.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", 'danger')
    return redirect(url_for('user.profile'))


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('user/settings.html')


@bp.route('/weather', methods=['POST'])
@login_required
def weather():
    data = request.json
    city = data.get('city')
    state = data.get('state')
    country = data.get('country')

    weather_data = get_weather_and_aqi(city, state, country)
    return jsonify(weather_data)


@bp.route('/get_weather', methods=['GET', 'POST'])
@login_required
def get_weather():
    """Get weather data for the user's address"""
    return render_template('user/weather.html')


@bp.route('/sustainablity_score', methods=['GET'])
@login_required
def sustainability_score():
    """Sustainability Score"""
    return render_template('user/sustainability_score.html')


@bp.route('/recommendations', methods=['GET'])
@login_required
def recommendations():
    """Recommendations"""
    return render_template('user/recommendations.html')

@bp.route('/eco_challanges', methods=['GET'])
@login_required
def eco_challanges():
    """Eco Challanges"""
    return render_template('user/eco_challanges.html')