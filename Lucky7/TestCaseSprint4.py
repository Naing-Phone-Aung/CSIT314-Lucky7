import unittest

from app import app
from db import db
from entity.Favourites import Favourites
from entity.Listing import Listing
from entity.Review import Review
from entity.UserAccount import UserAccount


class Sprint4Test(unittest.TestCase):
    def setUp(self):
        # Set up the app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

            # Create test users and listings with dob and phone_number
            self.agent = UserAccount(
                name="Test Agent",
                email="agent@example.com",
                password="password",
                dob="1980-01-01",
                phone_number="1234567891",
                profile="usedCarAgent"
            )
            self.seller = UserAccount(
                name="Test Seller",
                email="seller@example.com",
                password="password",
                dob="1990-01-01",
                phone_number="1234567892",
                profile="seller"
            )
            self.buyer = UserAccount(
                name="Test Buyer",
                email="buyer@example.com",
                password="password",
                dob="2000-01-01",
                phone_number="1234567893",
                profile="buyer"
            )

            db.session.add_all([self.agent, self.seller, self.buyer])
            db.session.commit()

            # Create a test listing by seller
            self.listing = Listing(
                name="Test Car",
                image_url="https://i.imgur.com/wcQuDG3.jpeg",
                price=10000,
                mileage=20000,
                seller_id=self.seller.id,
                agent_id=self.agent.id,
                model="Model S",
                color="Red",
                steering_type="Automatic",
                steering_position="Left",
                fuel_type="Electric",
                horsepower=400,
                previous_owners=1,
                description="A test car"
            )
            db.session.add(self.listing)
            db.session.commit()

            # Track created IDs for cleanup
            self.listing_id = self.listing.id
            self.agent_id = self.agent.id
            self.seller_id = self.seller.id
            self.buyer_id = self.buyer.id
            self.created_review_ids = []
            self.created_favourite_ids = []

    def tearDown(self):
        with app.app_context():
            # Remove only created favorites and reviews
            for fav_id in self.created_favourite_ids:
                db.session.query(Favourites).filter_by(id=fav_id).delete()
            for review_id in self.created_review_ids:
                db.session.query(Review).filter_by(id=review_id).delete()

            # Remove the created listing and users if they exist
            db.session.query(Listing).filter_by(id=self.listing_id).delete()
            db.session.query(UserAccount).filter_by(id=self.agent_id).delete()
            db.session.query(UserAccount).filter_by(id=self.seller_id).delete()
            db.session.query(UserAccount).filter_by(id=self.buyer_id).delete()

            db.session.commit()

    # Tests for Sprint 2 functionalities
    def test_get_all_listings(self):
        with app.app_context():
            listings = Listing.get_all_listings()
            self.assertTrue(any(listing.id == self.listing_id for listing in listings))

    def test_get_listing_details(self):
        with app.app_context():
            listing_details = Listing.get_listing_details(self.listing_id)
            self.assertIsNotNone(listing_details)
            self.assertEqual(listing_details.Listing.id, self.listing_id)

    def test_get_reviews_by_agent(self):
        with app.app_context():
            # Seller adds review for agent
            Review.add_review(agent_id=self.agent_id, user_id=self.seller_id, star_rating=4, description="Good service", user_profile="seller")
            review = db.session.query(Review).filter_by(agent_id=self.agent_id, seller_id=self.seller_id).first()
            self.created_review_ids.append(review.id)  # Track ID for cleanup

            # Retrieve reviews for agent
            reviews, agent_info = Review.get_reviews_by_agent(agent_id=self.agent_id, filter_by='seller')
            self.assertTrue(len(reviews) > 0)
            self.assertEqual(reviews[0]['description'], "Good service")

    def test_add_to_favourites(self):
        with app.app_context():
            result = Favourites.add_to_favourites(self.listing_id, self.buyer_id)
            self.assertTrue(result)
            favourite = Favourites.query.filter_by(listing_id=self.listing_id, buyer_id=self.buyer_id).first()
            self.created_favourite_ids.append(favourite.id)
            self.assertIsNotNone(favourite)

    def test_remove_from_favourites(self):
        with app.app_context():
            # First, add to favourites
            Favourites.add_to_favourites(self.listing_id, self.buyer_id)
            favourite = Favourites.query.filter_by(listing_id=self.listing_id, buyer_id=self.buyer_id).first()
            self.created_favourite_ids.append(favourite.id)

            # Now, remove from favourites
            result = Favourites.remove_from_favourites(self.listing_id, self.buyer_id)
            self.assertTrue(result)
            favourite_removed = Favourites.query.filter_by(listing_id=self.listing_id, buyer_id=self.buyer_id).first()
            self.assertIsNone(favourite_removed)

if __name__ == "__main__":
    unittest.main()
