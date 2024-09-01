import random

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
# from app.models import Service, BlogPost
from app import db
from datetime import datetime
from app.utils import calculate_footprint

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


@bp.route('/impact_calculator')
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
def calculator():
    if request.method == 'POST':
        # Handle form submission
        data = request.form

        # Perform calculations
        result = calculate_footprint(data)

        return jsonify(result=result)

    return render_template('user/calculator.html')
