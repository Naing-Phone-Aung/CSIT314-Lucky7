import unittest
from app import app

class Sprint1Test_18(unittest.TestCase):
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

    #18 Agent Log out
    def test_agent_logout(self):
        # Simulate agent login
        with self.client.session_transaction() as session:
            session['user_id'] = 22
            session['user_role'] = 'usedCarAgent'

        response = self.client.get("/Logout")
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()
