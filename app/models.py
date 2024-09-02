#!/usr/bin/env python3
"""Module for Database Models"""
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    """Model for User Roles"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')


class User(UserMixin, db.Model):
    """Model for User Accounts and Profiles"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(20))
    reset_token = db.Column(db.String(100))
    reset_token_expiration = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    activities = db.relationship('Activity', backref='user', lazy='dynamic')
    recommendations = db.relationship('Recommendation', backref='user', lazy=True)
    user_challenges = db.relationship('UserChallenges', backref='user', lazy=True)
    carbon_footprint = db.relationship('CarbonFootprint', backref='user', uselist=False)
    address = db.relationship('Address', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}, Email: {self.email}, Name: {self.first_name} {self.last_name}>'

    def set_password(self, password):
        """Set a hashed password for the user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hashed password."""
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        """Generate and return a reset token for the user."""
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """Verify the reset token and return the user if valid."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Address(db.Model):
    """Model for User Addresses"""
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(128))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    country = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        """Return a string representation of the address."""
        return f'<Address {self.city}, {self.state}, {self.country}>'


class Activity(db.Model):
    """Model for User Activities"""
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    activity_type = db.Column(db.String(20))
    description = db.Column(db.String(200))
    carbon_impact = db.Column(db.Float)
    date = db.Column(db.Date, default=datetime.utcnow)


class Recommendation(db.Model):
    """Model for User Recommendations"""
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    impact = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Contact(db.Model):
    """Model for Contact Form"""
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Return a string representation of the contact."""
        return f'<Contact {self.name}>'


class UserChallenges(db.Model):
    """Model for User Challenges"""
    __tablename__ = 'user_challenges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    challenge_id = db.Column(db.Integer, db.ForeignKey('eco_challenges.id'))
    eco_challenge = db.relationship('EcoChallenges', backref='user_challenges', lazy=True)


class CarbonFootprint(db.Model):
    """Model for User Carbon Footprints"""
    __tablename__ = 'carbon_footprints'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    footprint = db.Column(db.Float)


class EcoChallenges(db.Model):
    """Model for Eco Challenges"""
    __tablename__ = 'eco_challenges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
