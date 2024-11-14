import unittest
from entity.UserAccount import UserAccount
from app import app
from db import db

class Sprint1Test_12(unittest.TestCase):
    def setUp(self):
        # Set up the app for testing
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'LinPyae'
        self.client = app.test_client()

        # Create application context
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        UserAccount.query.filter_by(email="test@test.com").delete()
        db.session.commit()
        
        self.app_context.pop()
    
    #12 User Admin Create Profile
    def test_create_account(self):
        name = "test"
        email = "test@test.com"
        password = "test"
        confirm_password = "test"
        dob = "2000-11-11"
        phone_number = "12345678"
        profile = "admin"

        success, message = UserAccount.create_account(
            name=name,
            email=email,
            password=password,
            confirm_password=confirm_password,
            dob=dob,
            phone_number=phone_number,
            profile=profile
        )
        
        self.assertTrue(success)
        self.assertEqual(message, 'Account created successfully!')

if __name__ == '__main__':
    unittest.main()

