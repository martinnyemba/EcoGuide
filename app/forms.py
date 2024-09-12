#!/usr/bin/env python
"""Forms for the user authentication and profile pages."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, FloatField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, \
    Length, Optional
from app.models import User, Address
import re


class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    Methods:
    validate_username(self, username)
        Ensures the username is unique and secure.
    validate_email(self, email)
        Ensures the email is unique.
    """

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        Function to validate that the username is unique and follows security guidelines.

        Parameters:
        username (StringField): The username field from the form.

        Raises:
        ValidationError: If the username is not unique or does not follow the security guidelines.
        """
        if not re.match(r'^[\w.-]+$', username.data):
            raise ValidationError('Username can only contain letters, numbers, dots, and underscores.')
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """
        Function to validate that the email is unique.

        Parameters:
        email (StringField): The email field from the form.

        Raises:
        ValidationError: If the email is not unique.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """Form for users to log in."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    """Form for users to request a password reset."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """Validate that the email exists in the database."""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """Form for users to reset their password."""
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UpdateProfileForm(FlaskForm):
    """Form for users to update their profile."""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number')
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    """Form for users to change their password."""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class UpdateAddressForm(FlaskForm):
    """Form for users to update their address."""
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Update Address')


class EstimateForm(FlaskForm):
    """Form for interacting with the Carbon Interface API"""
    estimate_type = SelectField('Estimate Type', choices=[
        ('', 'Please choose an estimate type'),
        ('electricity', 'Electricity'),
        ('flight', 'Flight'),
        ('shipping', 'Shipping'),
        ('vehicle', 'Vehicle'),
        ('fuel_combustion', 'Fuel Combustion')
    ], validators=[DataRequired(message='Please select an Estimate Type')])

    # Electricity fields
    electricity_value = FloatField('Electricity Usage', validators=[Optional()])
    electricity_unit = SelectField('Electricity Unit', choices=[
        ('mwh', 'Megawatt Hours (MWh)'),
        ('kwh', 'Kilowatt Hours (kWh)')
    ], validators=[Optional()])
    country = SelectField('Country', choices=[
        ('us', 'United States of America'),
        ('ca', 'Canada'),
        ('at', 'Austria'),
        ('be', 'Belgium'),
        ('bg', 'Bulgaria'),
        ('hr', 'Croatia'),
        ('cy', 'Cyprus'),
        ('cz', 'Czechia'),
        ('dk', 'Denmark'),
        ('eu27', 'EU-27'),
        ('eu27plus1', 'EU27+1'),
        ('ee', 'Estonia'),
        ('fi', 'Finland'),
        ('fr', 'France'),
        ('de', 'Germany'),
        ('gr', 'Greece'),
        ('hu', 'Hungary'),
        ('ie', 'Ireland'),
        ('it', 'Italy'),
        ('lv', 'Latvia'),
        ('lt', 'Lithuania'),
        ('lu', 'Luxembourg'),
        ('mt', 'Malta'),
        ('nl', 'Netherlands'),
        ('pl', 'Poland'),
        ('pt', 'Portugal'),
        ('ro', 'Romania'),
        ('sk', 'Slovakia'),
        ('si', 'Slovenia'),
        ('es', 'Spain'),
        ('se', 'Sweden'),
        ('gb', 'United Kingdom'),
        # Add other countries as needed
    ], validators=[Optional()])
    state = StringField('State', validators=[Optional()])

    # Flight fields
    passengers = IntegerField('Number of Passengers', validators=[Optional()])
    departure_airport = StringField('Departure Airport', validators=[Optional()])
    destination_airport = StringField('Destination Airport', validators=[Optional()])
    return_flight = BooleanField('Return Flight?', validators=[Optional()])

    # Shipping fields
    weight_value = FloatField('Weight', validators=[Optional()])
    weight_unit = SelectField('Weight Unit', choices=[
        ('g', 'Grams (g)'),
        ('kg', 'Kilograms (kg)'),
        ('lb', 'Pounds (lb)')
    ], validators=[Optional()])
    distance_value = FloatField('Distance', validators=[Optional()])
    distance_unit = SelectField('Distance Unit', choices=[
        ('km', 'Kilometers (km)'),
        ('mi', 'Miles (mi)')
    ], validators=[Optional()])
    transport_method = SelectField('Transport Method', choices=[
        ('truck', 'Truck'),
        ('train', 'Train'),
        ('ship', 'Ship'),
        ('plane', 'Plane')
    ], validators=[Optional()])

    # Vehicle fields
    vehicle_make = StringField('Vehicle Make', validators=[Optional()])
    vehicle_model = StringField('Vehicle Model', validators=[Optional()])
    vehicle_year = IntegerField('Vehicle Year', validators=[Optional()])

    # Fuel Combustion fields
    fuel_source_type = SelectField('Fuel Source Type', choices=[
        ('bit', 'Bituminous Coal'),
        ('dfo', 'Home Heating and Diesel Fuel (Distillate)'),
        ('jf', 'Jet Fuel'),
        ('ker', 'Kerosene'),
        ('lig', 'Lignite Coal'),
        ('msw', 'Municipal Solid Waste'),
        ('ng', 'Natural Gas'),
        ('pc', 'Petroleum Coke'),
        ('pg', 'Propane Gas'),
        ('rfo', 'Residual Fuel Oil'),
        ('sub', 'Subbituminous Coal'),
        ('tdf', 'Tire-Derived Fuel'),
        ('wo', 'Waste Oil')
        # Add more fuel types as needed
    ], validators=[Optional()])

    fuel_source_unit = SelectField('Fuel Source Unit', choices=[
        ('btu', 'British Thermal Units (BTU)'),
        ('therm', 'Therms'),
        ('liter', 'Liters'),
        ('gallon', 'Gallons'),
        ('kg', 'Kilograms'),
        ('lb', 'Pounds'),
        ('short_ton', 'Short Ton'),
        ('thousand_cubic_feet', 'Thousand Cubic Feet'),
        ('barrel', 'Barrel')
        # Add more units as needed
    ], validators=[Optional()])

    fuel_source_value = DecimalField('Fuel Source Value', validators=[Optional()])

    submit = SubmitField('Calculate Carbon Estimate')
