from datetime import datetime

import requests
from config import IMGUR_CLIENT_ID
from db import db
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import aliased


class Listing(db.Model):
    __tablename__ = 'listing'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)  # Store the Imgur link
    price = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)

    # Enums for select fields
    steering_type = db.Column(SQLAlchemyEnum('Automatic', 'Manual', name='steering_type_enum'), nullable=False)
    steering_position = db.Column(SQLAlchemyEnum('Left', 'Right', name='steering_position_enum'), nullable=False)
    fuel_type = db.Column(SQLAlchemyEnum('Diesel', 'Petrol', 'Electric', name='fuel_type_enum'), nullable=False)

    horsepower = db.Column(db.Integer, nullable=False)
    previous_owners = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='listed')  # Initial status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation

    # Foreign keys
    seller_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=True)  # Initially empty

    views = db.Column(db.Integer, default=0)
    favs = db.Column(db.Integer, default=0)

    def __init__(self, name, image_url, price, model, color, mileage, steering_type, steering_position,fuel_type, horsepower, previous_owners, description, seller_id, agent_id, views=0, favs=0):
        self.name = name
        self.image_url = image_url
        self.price = price
        self.model = model
        self.color = color
        self.mileage = mileage
        self.steering_type = steering_type
        self.steering_position = steering_position
        self.fuel_type = fuel_type
        self.horsepower = horsepower
        self.previous_owners = previous_owners
        self.description = description
        self.seller_id = seller_id
        self.agent_id = agent_id
        self.views = 0
        self.favs = 0


    ########################### SellerController.py ###########################
    def get_seller_listings(seller_id):
        from entity.UserAccount import \
            UserAccount  # Local import to avoid circular dependency

        # Perform a join to retrieve both listing and agent details
        return db.session.query(
            Listing.id,
            Listing.name,
            Listing.mileage,
            Listing.price,
            Listing.image_url,
            Listing.created_at,
            Listing.previous_owners,
            Listing.status,
            Listing.seller_id,
            Listing.agent_id,
            Listing.views,
            Listing.favs,
            UserAccount.name.label("agent_name")
        ).join(UserAccount, UserAccount.id == Listing.agent_id) \
        .filter(Listing.seller_id == seller_id).all()


    ########################### CarListingController ###########################
    @staticmethod
    def validate_form_data(form_data):
        errors = []
        if not form_data['name'] or len(form_data['name']) > 100:
            errors.append("Car name must be between 1 and 100 characters.")
        if not form_data.get('image'):
            errors.append("Image is required.")
        try:
            price = int(form_data['price'])
            if price < 0:
                errors.append("Price must be a positive integer.")
        except ValueError:
            errors.append("Price must be a valid integer.")
        if not form_data['model'] or len(form_data['model']) > 50:
            errors.append("Model must be 50 characters or fewer.")
        if not form_data['color'] or len(form_data['color']) > 30:
            errors.append("Color must be 30 characters or fewer.")
        try:
            mileage = int(form_data['mileage'])
            if mileage < 0 or mileage > 500000:
                errors.append("Mileage must be between 0 and 500,000.")
        except ValueError:
            errors.append("Mileage must be a valid integer.")
        if form_data['steering_type'] not in ['Automatic', 'Manual']:
            errors.append("Steering type must be either 'Automatic' or 'Manual'.")
        if form_data['steering_position'] not in ['Left', 'Right']:
            errors.append("Steering position must be either 'Left' or 'Right'.")
        if form_data['fuel_type'] not in ['Diesel', 'Petrol', 'Electric']:
            errors.append("Fuel type must be 'Diesel', 'Petrol', or 'Electric'.")
        try:
            horsepower = int(form_data['horsepower'])
            if horsepower < 50 or horsepower > 2000:
                errors.append("Horsepower must be between 50 and 2000.")
        except ValueError:
            errors.append("Horsepower must be a valid integer.")
        try:
            previous_owners = int(form_data['previous_owners'])
            if previous_owners < 0 or previous_owners > 10:
                errors.append("Number of previous owners must be between 0 and 10.")
        except ValueError:
            errors.append("Previous owners must be a valid integer.")
        if form_data.get('description') and len(form_data['description']) > 500:
            errors.append("Description must be 500 characters or fewer.")
        return errors

    @staticmethod
    def upload_image_to_imgur(file):
        headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
        response = requests.post(
            'https://api.imgur.com/3/upload',
            headers=headers,
            files={'image': file}
        )
        data = response.json()
        return data['data']['link'] if 'data' in data else None

    @classmethod
    def create_listing(cls, form_data, agent_id, seller_id):
        errors = cls.validate_form_data(form_data)
        if errors:
            return False, errors

        image_url = cls.upload_image_to_imgur(form_data['image'])
        if not image_url:
            return False, ["Image upload failed."]

        new_listing = cls(
            name=form_data['name'],
            image_url=image_url,
            price=form_data['price'],
            model=form_data['model'],
            color=form_data['color'],
            mileage=form_data['mileage'],
            steering_type=form_data['steering_type'],
            steering_position=form_data['steering_position'],
            fuel_type=form_data['fuel_type'],
            horsepower=form_data['horsepower'],
            previous_owners=form_data['previous_owners'],
            description=form_data.get('description', ''),
            seller_id=seller_id,
            agent_id=agent_id
        )
        db.session.add(new_listing)
        db.session.commit()
        return True, "Listing created successfully."

    @staticmethod
    def process_update(listing_id, form_data):
        listing = Listing.query.get(listing_id)
        if listing:
            # Update listing fields
            for field, value in form_data.items():
                setattr(listing, field, value)
            db.session.commit()

    @classmethod
    def get_listings_by_agent(cls, agent_id, search_query=None):
        # Retrieve listings created by a specific agent with optional search filtering
        listing = db.session.query(
            cls.id,
            cls.name,
            cls.mileage,
            cls.price,
            cls.image_url,
            cls.created_at,
            cls.previous_owners,
            cls.status,
            cls.seller_id,
            cls.agent_id,
            cls.views,
            cls.favs
        ).filter(cls.agent_id == agent_id)

        # Apply search query if provided
        if search_query:
            listing = listing.filter(cls.name.ilike(f"%{search_query}%"))

        return listing.all()

    @classmethod
    def get_all_listings(cls, search_query=None):
        # Retrieve listings created by a specific agent with optional search filtering
        listing = db.session.query(
            cls.id,
            cls.name,
            cls.mileage,
            cls.price,
            cls.image_url,
            cls.created_at,
            cls.previous_owners,
            cls.status,
            cls.views,
            cls.seller_id,
            cls.agent_id
        ).filter(cls.status != 'sold')  # Exclude listings where status is 'sold'

        # Apply search query if provided
        if search_query:
            listing = listing.filter(cls.name.ilike(f"%{search_query}%"))

        return listing.all()

    @classmethod
    def get_listing_details(cls, listing_id):
        # Query the Listing details along with seller and agent information
        from entity.UserAccount import UserAccount
        AgentAccount = aliased(UserAccount)
        listing = db.session.query(
            cls,
            UserAccount.name.label("seller_name"),
            UserAccount.email.label("seller_email"),
            AgentAccount.name.label("agent_name")
        ).join(UserAccount, cls.seller_id == UserAccount.id) \
        .join(AgentAccount, cls.agent_id == AgentAccount.id).filter(
            cls.id == listing_id
        ).first()
        return listing

    @classmethod
    def remove_listing(cls, listing_id):
        # Retrieve the listing to be deleted
        listing = cls.query.get(listing_id)
        if listing:
            db.session.delete(listing)
            db.session.commit()
            return True
        return False


    @classmethod
    def increment_view_count(cls, listing_id):
        """Finds a listing by ID and increments its view count."""
        listing = cls.query.get(listing_id)
        if listing:
            listing.views = (listing.views or 0) + 1  # Ensure views is not None
            db.session.commit()
            return True
        return False

    @classmethod
    def increment_fav_count(cls, listing_id):
        """Finds a listing by ID and increments its fav count."""
        listing = cls.query.get(listing_id)
        if listing:
            listing.favs = (listing.favs or 0) + 1  # Ensure favs is not None
            db.session.commit()
            return True
        return False

    @classmethod
    def decrement_fav_count(cls, listing_id):
        """Finds a listing by ID and decrements its fav count."""
        listing = cls.query.get(listing_id)
        if listing and listing.favs > 0:
            listing.favs -= 1
            db.session.commit()
            return True
        return False

    @staticmethod
    def mark_listing_as_sold(listing_id, buyer_email):
        """Marks a listing as sold by updating the buyer_id based on the buyer's email."""
        from entity.UserAccount import \
            UserAccount  # Import to avoid circular dependency

        try:
            # Fetch the buyer's ID using the email
            buyer = db.session.query(UserAccount).filter_by(email=buyer_email).first()
            if not buyer:
                return False, "Buyer with the provided email not found."

            # Retrieve the listing by ID
            listing = Listing.query.get(listing_id)
            if not listing:
                return False, "Listing with the provided ID not found."

            if listing.status == 'sold':
                return False, "Listing is already marked as sold."

            # Update the listing's buyer_id and status
            listing.buyer_id = buyer.id
            listing.status = 'sold'

            # Commit the changes to the database
            db.session.commit()
            return True, "Listing marked as sold successfully."
        except Exception as e:
            # Log the exception if needed
            return False, str(e)
