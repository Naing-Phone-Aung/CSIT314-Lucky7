import unittest
from entity.UserAccount import UserAccount
from app import app

class Sprint1Test_25(unittest.TestCase):
    def setUp(self):
        # Set up the app for testing
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'LinPyae'
        self.client = app.test_client()

        # Create application context
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    #25 Buyer Log in
    def test_buyer_login(self):
        # Test logging in as a buyer
        success, user = UserAccount.verify_account("buyer@buyer.com", "buyer")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.profile, 'buyer')

if __name__ == '__main__':
    unittest.main()
