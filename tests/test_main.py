import unittest
from flask import url_for
from app import create_app, db
from config import TestingConfig


class TestMainRoutes(unittest.TestCase):
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

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home', response.data)

    def test_features_route(self):
        response = self.client.get('/features')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Features', response.data)

    def test_about_route(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)

    def test_how_it_works_route(self):
        response = self.client.get('/how')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'How It Works', response.data)

    def test_contact_route_get(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact Us', response.data)

    def test_contact_route_post(self):
        response = self.client.post('/contact', data=dict(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='Test Message'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Note: This test might fail if the email sending fails. You might want to mock the email sending function.
        self.assertIn(b'"success":true', response.data)


if __name__ == '__main__':
    unittest.main()
