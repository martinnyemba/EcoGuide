import unittest
from app import create_app, db
from app.models import User, Role, Activity, Recommendation, Contact, UserChallenges, CarbonFootprint, EcoChallenges, \
    Address
from config import TestingConfig


class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='test')
        u.set_password('mypassword123')
        self.assertFalse(u.check_password('checkpassword'))
        self.assertTrue(u.check_password('mypassword123'))

    @unittest.skip("Skipping test for now")
    def test_user_role(self):
        Role.insert_roles()
        u = User(username='john', email='john@example.com')
        self.assertTrue(u.role.name == 'User')

    def test_activity_creation(self):
        u = User(username='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        a = Activity(user_id=u.id, activity_type='walking', description='Walked to work', carbon_impact=0.5)
        db.session.add(a)
        db.session.commit()
        self.assertTrue(a in u.activities)

    def test_recommendation_creation(self):
        u = User(username='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        r = Recommendation(user_id=u.id, title='Use public transport', description='Use buses or trains', impact=2.0)
        db.session.add(r)
        db.session.commit()
        self.assertTrue(r in u.recommendations)

    def test_contact_creation(self):
        c = Contact(name='John Doe', email='john@example.com', message='Test message')
        db.session.add(c)
        db.session.commit()
        self.assertIsNotNone(c.id)

    def test_user_challenge_creation(self):
        u = User(username='john', email='john@example.com')
        e = EcoChallenges(name='Reduce plastic', description='Use less plastic for a week')
        db.session.add_all([u, e])
        db.session.commit()
        uc = UserChallenges(user_id=u.id, challenge_id=e.id)
        db.session.add(uc)
        db.session.commit()
        self.assertTrue(uc in u.user_challenges)

    def test_carbon_footprint_creation(self):
        u = User(username='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        cf = CarbonFootprint(user_id=u.id, footprint=10.5)
        db.session.add(cf)
        db.session.commit()
        self.assertEqual(u.carbon_footprint, cf)

    def test_address_creation(self):
        u = User(username='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        a = Address(user_id=u.id, street='123 Main St', city='Anytown', state='CA', country='USA')
        db.session.add(a)
        db.session.commit()
        self.assertEqual(u.address, a)


if __name__ == '__main__':
    unittest.main()
