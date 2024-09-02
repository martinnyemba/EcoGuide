# app/utils.py
from flask import abort, url_for, current_app, request, render_template
from flask_login import current_user
from flask_mail import Message
from markupsafe import Markup

from app import mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='emtechmediapro@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def render_pagination(pagination, endpoint, **kwargs):
    args = request.args.copy()
    args.update(kwargs)
    page_urls = []
    for page in pagination.iter_pages(left_edge=2, left_current=2, right_current=3, right_edge=2):
        if page:
            args['page'] = page
            page_urls.append((page, url_for(endpoint, **args)))
        else:
            page_urls.append((None, None))
    return Markup(render_template('_pagination.html', pagination=pagination, page_urls=page_urls))

def calculate_footprint(data):
    # Convert form data to float
    electricity = float(data['electricity'])
    gas = float(data['gas'])
    oil = float(data['oil'])
    mileage = float(data['mileage'])
    flights = float(data['flights'])
    publictransport = float(data['publictransport'])
    diet = data['diet']
    waste = float(data['waste'])
    water = float(data['water'])
    shopping = float(data['shopping'])

    # Carbon footprint calculations (in metric tons of CO2)
    electricityFootprint = electricity * 12 * 0.000404  # kWh to metric tons CO2
    gasFootprint = gas * 12 * 0.00220462 * 0.005  # m3 to kg, then to metric tons CO2
    oilFootprint = oil * 0.00264172 * 0.011  # Litres to gallons, then to metric tons CO2
    mileageFootprint = mileage * 0.000621371 * 0.000404  # km to miles, then to metric tons CO2
    flightsFootprint = flights * 0.9
    publictransportFootprint = publictransport * 52 * 0.000621371 * 0.000186  # km to miles, then to metric tons CO2

    dietFootprint = {
        'meat_lover': 3.3,
        'average': 2.5,
        'vegetarian': 1.7,
        'vegan': 1.5
    }.get(diet, 0)

    wasteFootprint = waste * 52 * 2.20462 * 0.00058  # kg to lbs, then to metric tons CO2
    waterFootprint = water * 365 * 0.264172 * 0.000298 / 1000  # Litres to gallons, then to metric tons CO2
    shoppingFootprint = shopping * 12 * 0.0045  # Assuming 1 USD = 1 CAD for simplicity

    totalFootprint = (
            electricityFootprint + gasFootprint + oilFootprint + mileageFootprint +
            flightsFootprint + publictransportFootprint + dietFootprint +
            wasteFootprint + waterFootprint + shoppingFootprint
    )

    return round(totalFootprint, 2)