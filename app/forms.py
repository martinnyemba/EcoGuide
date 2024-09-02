# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, DateTimeField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, \
    Length, Optional
from app.models import User, Address


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


# User Forms
class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number')
    submit = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class UpdateAddressForm(FlaskForm):
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Update Address')


# Forms for Carbon Interface API
class EstimateForm(FlaskForm):
    estimate_type = SelectField('Estimate Type', choices=[
        ('electricity', 'Electricity'),
        ('shipping', 'Shipping'),
        ('flight', 'Flight'),
        ('vehicle', 'Vehicle')
    ], validators=[DataRequired()])

    # Electricity fields
    electricity_usage = FloatField('Electricity Usage (kWh)', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])

    # Shipping fields
    weight = FloatField('Weight (kg)', validators=[Optional()])
    distance = FloatField('Distance (km)', validators=[Optional()])
    method = SelectField('Shipping Method', choices=[
        ('truck', 'Truck'),
        ('train', 'Train'),
        ('ship', 'Ship'),
        ('plane', 'Plane')
    ], validators=[Optional()])

    # Flight fields
    passengers = IntegerField('Number of Passengers', validators=[Optional()])
    departure_airport = StringField('Departure Airport', validators=[Optional()])
    destination_airport = StringField('Destination Airport', validators=[Optional()])

    # Vehicle fields
    distance_km = FloatField('Distance (km)', validators=[Optional()])
    vehicle_make = StringField('Vehicle Make', validators=[Optional()])
    vehicle_model = StringField('Vehicle Model', validators=[Optional()])
    vehicle_year = IntegerField('Vehicle Year', validators=[Optional()])