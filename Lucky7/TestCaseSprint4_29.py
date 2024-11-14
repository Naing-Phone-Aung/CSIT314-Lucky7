import unittest
from app import app
from db import db
from entity.Favourites import Favourites
from entity.Listing import Listing
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
            self.created_favourite_ids = []

    def tearDown(self):
        with app.app_context():
            # Remove only created favorites
            for fav_id in self.created_favourite_ids:
                db.session.query(Favourites).filter_by(id=fav_id).delete()

            # Remove the created listing and users if they exist
            db.session.query(Listing).filter_by(id=self.listing_id).delete()
            db.session.query(UserAccount).filter_by(id=self.agent_id).delete()
            db.session.query(UserAccount).filter_by(id=self.seller_id).delete()
            db.session.query(UserAccount).filter_by(id=self.buyer_id).delete()

            db.session.commit()

    #29 Buyer Save Car Info
    def test_buyer_save_car_info(self):
        with app.app_context():
            result = Favourites.add_to_favourites(self.listing_id, self.buyer_id)
            self.assertTrue(result)
            favourite = Favourites.query.filter_by(listing_id=self.listing_id, buyer_id=self.buyer_id).first()
            self.created_favourite_ids.append(favourite.id)
            self.assertIsNotNone(favourite)

if __name__ == "__main__":
    unittest.main()
