# app/utils.py
from flask import abort
from flask_login import current_user
from functools import wraps
from app import mail
from flask_mail import Message
from twilio.rest import Client
import app


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'Admin':
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_appointment_confirmation(booking):
    send_email('Appointment Confirmation',
               sender=app.config['ADMINS'][0],
               recipients=[booking.user.email],
               text_body=f'Your appointment for {booking.service.name} on {booking.date} has been booked.',
               html_body=f'<p>Your appointment for {booking.service.name} on {booking.date} has been booked.</p>')


def send_appointment_reminder(booking):
    send_email('Appointment Reminder',
               sender=app.config['ADMINS'][0],
               recipients=[booking.user.email],
               text_body=f'Reminder: Your appointment for {booking.service.name} is scheduled for {booking.date}.',
               html_body=f'<p>Reminder: Your appointment for {booking.service.name} is scheduled for {booking.date}.</p>')


def send_sms(to, body):
    client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    message = client.messages.create(
        body=body,
        from_=app.config['TWILIO_PHONE_NUMBER'],
        to=to
    )
    return message.sid


def send_appointment_sms_confirmation(booking):
    body = f'Your appointment for {booking.service.name} on {booking.date} has been booked.'
    send_sms(booking.user.phone_number, body)


def generate_reference_number():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


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