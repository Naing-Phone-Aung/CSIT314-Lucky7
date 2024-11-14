import unittest
from app import app
from db import db
from entity.UserAccount import UserAccount

class Sprint5test_9_14(unittest.TestCase):
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

    #9 #14 User Admin Update
    def test_update_account_info(self):
        with app.app_context():
            # Test updating user1's info
            result, message = UserAccount.update_account_info(
                account_id=self.user1.id,
                name="Updated User1",
                email="newuser1@example.com",
                dob="1991-01-01",
                phone_number="9876543210",
                profile="seller"
            )
            self.assertTrue(result)
            self.assertEqual(message, "Account updated successfully.")

            # Verify updates
            updated_user = db.session.get(UserAccount, self.user1.id)

            self.assertEqual(updated_user.name, "Updated User1")
            self.assertEqual(updated_user.email, "newuser1@example.com")
            self.assertEqual(updated_user.phone_number, "9876543210")
            self.assertEqual(updated_user.profile, "seller")

if __name__ == "__main__":
    unittest.main()