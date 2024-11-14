import unittest

from app import app
from db import db
from entity.UserAccount import UserAccount


class Sprint5test(unittest.TestCase):
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

    #11 #16 User Admin Search
    def test_get_filtered_accounts(self):
        with app.app_context():
            results = UserAccount.get_filtered_accounts(search_query="User", profile_filter="buyer")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].id, self.user1.id)

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
