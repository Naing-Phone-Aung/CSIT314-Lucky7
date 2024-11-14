import unittest
from unittest.mock import patch
from app import app
from db import db
from entity.Listing import Listing
from entity.Review import Review
from entity.UserAccount import UserAccount

class Sprint2Test_19(unittest.TestCase):
    def setUp(self):
        # Set up the app for testing
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'LinPyae'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            
            # Check if the agent and seller accounts already exist
            self.agent = db.session.query(UserAccount).filter_by(email="agent@example.com").first()
            if not self.agent:
                self.agent = UserAccount(
                    name="Agent",
                    email="agent@example.com",
                    password="password",
                    dob="1980-01-01",
                    phone_number="1234567891",
                    profile="usedCarAgent"
                )
                db.session.add(self.agent)
            
            self.seller = db.session.query(UserAccount).filter_by(email="seller@example.com").first()
            if not self.seller:
                self.seller = UserAccount(
                    name="Seller",
                    email="seller@example.com",
                    password="password",
                    dob="1990-01-01",
                    phone_number="0987654322",
                    profile="seller"
                )
                db.session.add(self.seller)
            
            db.session.commit()

            # Store IDs for cleanup, if they were just created
            self.agent_id = self.agent.id
            self.seller_id = self.seller.id
            self.created_listing_ids = []
            self.created_review_ids = []

    def tearDown(self):
        with app.app_context():
            # Remove listings and reviews created in tests
            for listing_id in self.created_listing_ids:
                db.session.query(Listing).filter_by(id=listing_id).delete()
            for review_id in self.created_review_ids:
                db.session.query(Review).filter_by(id=review_id).delete()
            
            # Remove test user accounts if they were created in this test run
            if db.session.get(UserAccount, self.agent_id):
                db.session.delete(self.agent)
            if db.session.get(UserAccount, self.seller_id):
                db.session.delete(self.seller)

            db.session.commit()

    #19 Agent Create Listing
    @patch.object(Listing, 'upload_image_to_imgur', return_value="https://i.imgur.com/wcQuDG3.jpeg")
    def test_agent_create_listing(self, mock_upload):
        with app.app_context():
            form_data = {
                "name": "Test Car",
                "price": 20000,
                "model": "Model X",
                "color": "Red",
                "mileage": 10000,
                "steering_type": "Automatic",
                "steering_position": "Left",
                "fuel_type": "Petrol",
                "horsepower": 500,
                "previous_owners": 1,
                "description": "A great car",
                "image": "http://example.com/image.jpg"
            }
            success, message = Listing.create_listing(form_data, agent_id=self.agent.id, seller_id=self.seller.id)
            self.assertTrue(success)
            self.assertEqual(message, "Listing created successfully.")

            # Track created listing ID for cleanup
            created_listing = db.session.query(Listing).filter_by(name="Test Car").first()
            if created_listing:
                self.created_listing_ids.append(created_listing.id)

            # Check if image_url was set to mock URL
            self.assertEqual(created_listing.image_url, "https://i.imgur.com/wcQuDG3.jpeg")

if __name__ == "__main__":
    unittest.main()
