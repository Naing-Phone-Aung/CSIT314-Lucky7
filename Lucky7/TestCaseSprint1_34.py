import unittest
from entity.UserAccount import UserAccount
from app import app

class Sprint1Test_34(unittest.TestCase):
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
    
    #34 Seller Log in 
    def test_seller_login(self):
        # Test logging in as a seller
        success, user = UserAccount.verify_account("seller@seller.com", "seller")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.profile, 'seller')

if __name__ == '__main__':
    unittest.main()

