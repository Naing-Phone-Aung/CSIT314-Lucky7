import unittest
from app import app
from db import db
from entity.UserAccount import UserAccount

class Sprint5test_8_18(unittest.TestCase):
    def setUp(self):
        # Set up the app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

            # Create test users
            self.admin = UserAccount(
                name="Test Admin",
                email="admin@example.com",
                password="password",
                dob="1980-01-01",
                phone_number="1234567890",
                profile="admin"
            )
            self.user1 = UserAccount(
                name="Test User1",
                email="user1@example.com",
                password="password",
                dob="1990-01-01",
                phone_number="1234567891",
                profile="buyer"
            )
            self.user2 = UserAccount(
                name="Test User2",
                email="user2@example.com",
                password="password",
                dob="1995-01-01",
                phone_number="1234567892",
                profile="seller"
            )

            db.session.add_all([self.admin, self.user1, self.user2])
            db.session.commit()

            # Track created IDs for cleanup
            self.created_account_ids = [self.admin.id, self.user1.id, self.user2.id]

    def tearDown(self):
        with app.app_context():
            # Only delete accounts created in this test
            for account_id in self.created_account_ids:
                db.session.query(UserAccount).filter_by(id=account_id).delete()
            db.session.commit()

    #8 #18 User Admin View
    def test_account_detail(self):
        with app.app_context():
            # Retrieve details for user1
            account_detail = UserAccount.get_account_by_id(self.user1.id)
            self.assertIsNotNone(account_detail)

            # Verify the details match what was set up
            self.assertEqual(account_detail['name'], "Test User1")
            self.assertEqual(account_detail['email'], "user1@example.com")
            self.assertEqual(account_detail['phone_number'], "1234567891")
            self.assertEqual(account_detail['profile'], "buyer")

if __name__ == "__main__":
    unittest.main()