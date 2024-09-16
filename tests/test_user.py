import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Address
from config import TestingConfig


class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_dashboard_route(self):
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Log in the user
        login_response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertIn(b'Welcome', login_response.data)  # or another success message

        # Test dashboard route
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_carbon_estimate_route(self):
        response = self.client.get('/carbon_estimate')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Carbon Estimate', response.data)

    def test_impact_calculator_route(self):
        # Log in a user (required for this route)
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        self.client.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)

        response = self.client.get('/impact_calculator')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Impact Calculator', response.data)

    def test_profile_route(self):
        # Log in a user (required for this route)
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        self.client.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)

        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile', response.data)

    def test_update_profile_route(self):
        # Log in a user (required for this route)
        user = User(username='testuser', email='test@example.com')
        user.set_password('password1223')
        db.session.add(user)
        db.session.commit()
        self.client.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)

        response = self.client.post('/update_profile', data=dict(
            username='newusername',
            email='newemail@example.com',
            first_name='New',
            last_name='Name',
            phone_number='1234567890'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'"Email":False', response.data)

    def test_update_address_route(self):
        # Log in a user (required for this route)
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        self.client.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)

        response = self.client.post('/update_address', data=dict(
            street='123 Test St',
            city='Test City',
            state='Test State',
            country='Test Country'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Address', response.data)


if __name__ == '__main__':
    unittest.main()
