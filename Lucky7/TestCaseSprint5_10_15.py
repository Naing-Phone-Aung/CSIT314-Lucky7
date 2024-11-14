import unittest
from app import app
from db import db
from entity.UserAccount import UserAccount

class Sprint5test_10_15(unittest.TestCase):
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

    #10 #15 User Admin Suspend
    def test_delete_account(self):
        with app.app_context():
            # Test deleting user1
            result, message = UserAccount.delete_account(self.user1.id)
            self.assertTrue(result)
            self.assertEqual(message, "Account deleted successfully.")

            # Verify anonymization of user1's data
            deleted_user = db.session.get(UserAccount, self.user1.id)

            self.assertEqual(deleted_user.name, "Deleted_Account")
            self.assertIsNone(deleted_user.email)
            self.assertIsNone(deleted_user.phone_number)


if __name__ == "__main__":
    unittest.main()