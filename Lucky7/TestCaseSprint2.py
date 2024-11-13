import unittest
from unittest.mock import patch
from app import app
from db import db
from entity.Listing import Listing
from entity.Review import Review
from entity.UserAccount import UserAccount

class Sprint2Test(unittest.TestCase):
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

    #20 Agent View Listing
    def test_agent_view_listing(self):
        with app.app_context():
            # Add sample listing and track ID
            listing = Listing(
                name="Sample Car",
                image_url="https://i.imgur.com/wcQuDG3.jpeg",
                price=15000,
                model="Model S",
                color="Blue",
                mileage=12000,
                steering_type="Automatic",
                steering_position="Left",
                fuel_type="Petrol",
                horsepower=300,
                previous_owners=1,
                description="A sample car",
                seller_id=self.seller.id,
                agent_id=self.agent.id
            )
            db.session.add(listing)
            db.session.commit()

            # Track created listing ID for cleanup
            self.created_listing_ids.append(listing.id)

            # Fetch listings and validate
            listings = Listing.get_listings_by_agent(agent_id=self.agent.id)
            self.assertTrue(len(listings) > 0)
            self.assertEqual(listings[0].name, "Sample Car")

    #21 Agent Update Listing
    def test_agent_update_listing(self):
        with app.app_context():
            # Create and update listing
            listing = Listing(name="Update Test Car", image_url="http://example.com/image.jpg", price=15000, 
                  model="Model S", color="Blue", mileage=12000, steering_type="Automatic", 
                  steering_position="Left", fuel_type="Petrol", horsepower=300, previous_owners=1, 
                  description="A car to update", seller_id=self.seller.id, agent_id=self.agent.id)
            db.session.add(listing)
            db.session.commit()

            # Track listing for cleanup
            self.created_listing_ids.append(listing.id)

            # Update the listing
            updated_data = {"price": 18000, "color": "Black"}
            Listing.process_update(listing_id=listing.id, form_data=updated_data)

            updated_listing = db.session.get(Listing, listing.id)
            self.assertEqual(updated_listing.price, 18000)
            self.assertEqual(updated_listing.color, "Black")

    #22 Agent Delete Listing
    def test_agent_delete_listing(self):
        with app.app_context():
            # Add and delete listing
            listing = Listing(name="Delete Test Car", image_url="http://example.com/image.jpg", price=15000, 
                  model="Model S", color="Blue", mileage=12000, steering_type="Automatic", 
                  steering_position="Left", fuel_type="Petrol", horsepower=300, previous_owners=1, 
                  description="A car to delete", seller_id=self.seller.id, agent_id=self.agent.id)
            db.session.add(listing)
            db.session.commit()

            # Track listing for cleanup
            self.created_listing_ids.append(listing.id)

            delete_success = Listing.remove_listing(listing_id=listing.id)
            self.assertTrue(delete_success)
            self.assertIsNone(db.session.get(Listing, listing.id))

    #23 Agent Search Listing
    def test_agent_search_listings(self):
        with app.app_context():
            # Add listings
            listing1 = Listing(name="Tesla Model S", image_url="http://example.com/image1.jpg", price=80000, 
                   model="Model S", color="White", mileage=10000, steering_type="Automatic", 
                   steering_position="Left", fuel_type="Electric", horsepower=400, previous_owners=0, 
                   description="Electric car", seller_id=self.seller.id, agent_id=self.agent.id)

            listing2 = Listing(name="Toyota Corolla", image_url="http://example.com/image2.jpg", price=20000, 
                   model="Corolla", color="Red", mileage=15000, steering_type="Manual", 
                   steering_position="Left", fuel_type="Petrol", horsepower=120, previous_owners=1, 
                   description="Compact car", seller_id=self.seller.id, agent_id=self.agent.id)
            db.session.add_all([listing1, listing2])
            db.session.commit()

            # Track listings for cleanup
            self.created_listing_ids.extend([listing1.id, listing2.id])

            # Search listings
            search_results = Listing.get_listings_by_agent(agent_id=self.agent.id, search_query="Tesla")
            self.assertEqual(len(search_results), 1)
            self.assertEqual(search_results[0].name, "Tesla Model S")

    #208 Agent View Detail of Listing
    def test_agent_view_detail_of_listing(self):
        with app.app_context():
            # Add listing and fetch details
            listing = Listing(name="Detail Test Car", image_url="http://example.com/image.jpg", price=15000, 
                  model="Model S", color="Blue", mileage=12000, steering_type="Automatic", 
                  steering_position="Left", fuel_type="Petrol", horsepower=300, previous_owners=1, 
                  description="Detailed car", seller_id=self.seller.id, agent_id=self.agent.id)
            db.session.add(listing)
            db.session.commit()

            # Track listing for cleanup
            self.created_listing_ids.append(listing.id)

            listing_details = Listing.get_listing_details(listing_id=listing.id)
            self.assertIsNotNone(listing_details)
            self.assertEqual(listing_details.Listing.name, "Detail Test Car")

if __name__ == "__main__":
    unittest.main()
