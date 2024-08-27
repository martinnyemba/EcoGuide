# app/utils.py
from flask import abort
from flask_login import current_user
from functools import wraps
from app import mail
from flask_mail import Message
#from twilio.rest import Client
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