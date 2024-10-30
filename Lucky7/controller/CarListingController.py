import requests
from config import IMGUR_CLIENT_ID
from entity.Listing import Listing
from entity.UserAccount import UserAccount
from db import db

class CarListingController:
    def validate_seller_email(self, email):
        seller = UserAccount.query.filter_by(email=email).first()
        return seller.id if seller else None

    def upload_image_to_imgur(self, file):
        headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
        response = requests.post(
            'https://api.imgur.com/3/upload',
            headers=headers,
            files={'image': file}
        )
        data = response.json()
        return data['data']['link'] if 'data' in data else None

    def create_listing(self, form_data, agent_id):
        errors = []

        # Validate car name
        if not form_data['name'] or len(form_data['name']) > 100:
            errors.append("Car name must be between 1 and 100 characters.")

        # Validate image file
        if not form_data.get('image'):
            errors.append("Image is required.")

        # Validate mileage
        try:
            price = int(form_data['price'])
            if price < 0 :
                errors.append("Price must be a positive integer.")
        except ValueError:
            errors.append("Price must be a valid integer.")

        # Validate model
        if not form_data['model'] or len(form_data['model']) > 50:
            errors.append("Model must be 50 characters or fewer.")

        # Validate color
        if not form_data['color'] or len(form_data['color']) > 30:
            errors.append("Color must be 30 characters or fewer.")

        # Validate mileage
        try:
            mileage = int(form_data['mileage'])
            if mileage < 0 or mileage > 500000:
                errors.append("Mileage must be between 0 and 500,000.")
        except ValueError:
            errors.append("Mileage must be a valid integer.")

        # Validate steering type
        if form_data['steering_type'] not in ['Automatic', 'Manual']:
            errors.append("Steering type must be either 'Automatic' or 'Manual'.")

        # Validate steering position
        if form_data['steering_position'] not in ['Left', 'Right']:
            errors.append("Steering position must be either 'Left' or 'Right'.")

        # Validate fuel type
        if form_data['fuel_type'] not in ['Diesel', 'Petrol', 'Electric']:
            errors.append("Fuel type must be 'Diesel', 'Petrol', or 'Electric'.")

        # Validate horsepower
        try:
            horsepower = int(form_data['horsepower'])
            if horsepower < 50 or horsepower > 2000:
                errors.append("Horsepower must be between 50 and 2000.")
        except ValueError:
            errors.append("Horsepower must be a valid integer.")

        # Validate previous owners
        try:
            previous_owners = int(form_data['previous_owners'])
            if previous_owners < 0 or previous_owners > 10:
                errors.append("Number of previous owners must be between 0 and 10.")
        except ValueError:
            errors.append("Previous owners must be a valid integer.")

        # Validate description length
        if form_data.get('description') and len(form_data['description']) > 500:
            errors.append("Description must be 500 characters or fewer.")

        # Validate seller email
        seller_id = self.validate_seller_email(form_data['seller_email'])
        if not seller_id:
            errors.append("Seller email not found in the system.")

        if errors:
            return False, errors  # Return errors if validation fails

        # Upload image to Imgur
        image_url = self.upload_image_to_imgur(form_data['image'])
        if not image_url:
            return False, ["Image upload failed."]

        # Create and save the listing
        new_listing = Listing(
            name=form_data['name'],
            image_url=image_url,
            model=form_data['model'],
            price=form_data['price'],
            color=form_data['color'],
            mileage=mileage,
            steering_type=form_data['steering_type'],
            steering_position=form_data['steering_position'],
            fuel_type=form_data['fuel_type'],
            horsepower=horsepower,
            previous_owners=previous_owners,
            description=form_data['description'],
            seller_id=seller_id,
            agent_id=agent_id
        )
        db.session.add(new_listing)
        db.session.commit()
        return True, "Listing created successfully."

    def get_listings_by_agent(self, agent_id):
        # Custom query to select only necessary fields
        listings = db.session.query(
            Listing.id,
            Listing.name,
            Listing.price,
            Listing.model,
            Listing.image_url,
            Listing.created_at,
            UserAccount.name.label("seller_name")  # Only fetch the seller's name
        ).join(UserAccount, Listing.seller_id == UserAccount.id).filter(
            Listing.agent_id == agent_id
        ).all()

        return listings

    def get_listing_details(self, listing_id):
        # Query the entire Listing object along with only the seller's name
        listing = db.session.query(
            Listing,
            UserAccount.name.label("seller_name")
        ).join(UserAccount, Listing.seller_id == UserAccount.id).filter(
            Listing.id == listing_id
        ).first()

        return listing
