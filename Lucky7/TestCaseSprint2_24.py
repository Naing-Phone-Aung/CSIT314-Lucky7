import unittest
from unittest.mock import patch
from app import app
from db import db
from entity.Listing import Listing
from entity.Review import Review
from entity.UserAccount import UserAccount

class Sprint2Test_24(unittest.TestCase):
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

    #24 Agent View Reviews
    def test_agent_view_reviews(self):
        with app.app_context():
            # Add sample review and track its ID
            review = Review(star_rating=4, description="Good agent", agent_id=self.agent.id, seller_id=None)
            db.session.add(review)
            db.session.commit()
            self.created_review_ids.append(review.id)

            reviews = Review.get_reviews_for_agent(agent_id=self.agent.id)
            self.assertTrue(len(reviews) > 0)
            self.assertEqual(reviews[0].description, "Good agent")

if __name__ == "__main__":
    unittest.main()
