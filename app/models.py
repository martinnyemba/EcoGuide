from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from datetime import datetime, timezone
from sqlalchemy.orm import validates
from . import db, login


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(20))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    activities = db.relationship('Activity', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', lazy=True, cascade='all, delete-orphan')
    user_challenges = db.relationship('UserChallenges', backref='user', lazy=True, cascade='all, delete-orphan')
    carbon_footprint = db.relationship('CarbonFootprint', backref='user', uselist=False, cascade='all, delete-orphan')
    address = db.relationship('Address', backref='user', uselist=False, cascade='all, delete-orphan')

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Invalid email address")
        return address

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(128))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    country = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Address {self.city}, {self.state}, {self.country}>'


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    activity_type = db.Column(db.String(20))
    description = db.Column(db.String(200))
    carbon_impact = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Activity {self.activity_type}>'


class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    impact = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Recommendation {self.title}>'


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Contact {self.name}>'


class UserChallenges(db.Model):
    __tablename__ = 'user_challenges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    challenge_id = db.Column(db.Integer, db.ForeignKey('eco_challenges.id'))
    eco_challenge = db.relationship('EcoChallenges', backref='user_challenges', lazy=True)

    def __repr__(self):
        return f'<UserChallenge {self.id}>'


class CarbonFootprint(db.Model):
    __tablename__ = 'carbon_footprints'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    footprint = db.Column(db.Float)

    def __repr__(self):
        return f'<CarbonFootprint {self.footprint}>'


class EcoChallenges(db.Model):
    __tablename__ = 'eco_challenges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<EcoChallenge {self.name}>'
