import unittest
from entity.UserAccount import UserAccount
from app import app
from db import db

class Sprint1Test(unittest.TestCase):
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
    
    #7 User Admin Create Account
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

    #25 Buyer Log in
    def test_buyer_login(self):
        # Test logging in as a buyer
        success, user = UserAccount.verify_account("buyer@buyer.com", "buyer")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.profile, 'buyer')

    #34 Seller Log in 
    def test_seller_login(self):
        # Test logging in as a seller
        success, user = UserAccount.verify_account("seller@seller.com", "seller")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.profile, 'seller')

    #5 Admin Log in
    def test_admin_login(self):
        # Test logging in as an admin
        success, user = UserAccount.verify_account("admin@admin.com", "admin")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.profile, 'admin')

    #17 Agent Log in 
    def test_used_car_agent_login(self):
        # Test logging in as a used car agent
        success, user = UserAccount.verify_account("agent@agent.com", "agent")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.profile, 'usedCarAgent')

    #6 User Admin Log out    
    def test_admin_logout(self):
        # Simulate admin login
        with self.client.session_transaction() as session:
            session['user_id'] = 1
            session['user_role'] = 'admin'

        response = self.client.get("/Logout")
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers['Location'])

    #18 Agent Log out
    def test_agent_logout(self):
        # Simulate agent login
        with self.client.session_transaction() as session:
            session['user_id'] = 22
            session['user_role'] = 'usedCarAgent'

        response = self.client.get("/Logout")
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers['Location'])

    #26 Buyer Log out
    def test_buyer_logout(self):
        # Simulate buyer login
        with self.client.session_transaction() as session:
            session['user_id'] = 20
            session['user_role'] = 'buyer'

        response = self.client.get("/Logout")
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers['Location'])

    #35 Seller Log out
    def test_seller_logout(self):
        # Simulate seller login
        with self.client.session_transaction() as session:
            session['user_id'] = 21
            session['user_role'] = 'seller'

        response = self.client.get("/Logout")
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()
