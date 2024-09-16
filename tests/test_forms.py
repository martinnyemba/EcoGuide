import unittest
from app import create_app, db
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm, ChangePasswordForm, UpdateAddressForm, \
    EstimateForm
from config import TestingConfig


class TestForms(unittest.TestCase):
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

    def test_registration_form(self):
        form = RegistrationForm()
        self.assertFalse(form.validate())
        form = RegistrationForm(username='testuser', email='test@example.com',
                                password='password123', confirm_password='password123',
                                first_name='Test', last_name='User', phone_number='1234567890')
        self.assertTrue(form.validate())

    def test_login_form(self):
        form = LoginForm()
        self.assertFalse(form.validate())
        form = LoginForm(email='test@example.com', password='password123')
        self.assertTrue(form.validate())

    def test_update_profile_form(self):
        form = UpdateProfileForm()
        self.assertFalse(form.validate())
        form = UpdateProfileForm(username='testuser', email='test@example.com',
                                 first_name='Test', last_name='User', phone_number='1234567890')
        self.assertTrue(form.validate())

    def test_change_password_form(self):
        form = ChangePasswordForm()
        self.assertFalse(form.validate())
        form = ChangePasswordForm(current_password='oldpassword', new_password='newpassword',
                                  confirm_password='newpassword')
        self.assertTrue(form.validate())

    def test_update_address_form(self):
        form = UpdateAddressForm()
        self.assertFalse(form.validate())
        form = UpdateAddressForm(street='123 Main St', city='Anytown', state='CA', country='USA')
        self.assertTrue(form.validate())

    def test_estimate_form(self):
        form = EstimateForm()
        self.assertFalse(form.validate())
        form = EstimateForm(estimate_type='electricity', electricity_value=100,
                            electricity_unit='kwh', country='us')
        self.assertTrue(form.validate())


if __name__ == '__main__':
    unittest.main()
