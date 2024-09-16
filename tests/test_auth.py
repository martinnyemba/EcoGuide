import unittest
from app import create_app, db
from app.models import User, Role
from config import TestingConfig


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home', response.data)

    def test_register_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_user_registration(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890'
        }, follow_redirects=True)
        self.assertIn(b'Your account has been created!', response.data)

    def test_user_login_logout(self):
        # Create a user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Login
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Dashboard', response.data)

        # Logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'EcoGuide', response.data)

    def test_protected_route(self):
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)


if __name__ == '__main__':
    unittest.main()
