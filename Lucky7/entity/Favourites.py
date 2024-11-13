from datetime import datetime
from db import db
from entity.Listing import Listing
from sqlalchemy import and_

class Favourites(db.Model):
    __tablename__ = 'favourites'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=True)

    def __init__(self,listing_id=None, buyer_id=None):
        self.listing_id = listing_id
        self.buyer_id = buyer_id

    @staticmethod
    def check_favourites(listing_id, buyer_id):
        return db.session.query(
            db.exists().where(
                and_(
                    Favourites.listing_id == listing_id,
                    Favourites.buyer_id == buyer_id
                )
            )
        ).scalar()

    @staticmethod
    def add_to_favourites(listing_id, buyer_id):
        if not Favourites.check_favourites(listing_id, buyer_id):
            favourite = Favourites(listing_id=listing_id, buyer_id=buyer_id)
            db.session.add(favourite)
            db.session.commit()
            return True
        return False  # Already in favourites

    @staticmethod
    def remove_from_favourites(listing_id, buyer_id):
        favourite = Favourites.query.filter_by(listing_id=listing_id, buyer_id=buyer_id).first()
        if favourite:
            db.session.delete(favourite)
            db.session.commit()
            return True
        return False  # Not found in favourites


    @classmethod
    def get_favourite_listings_for_user(cls, buyer_id):
      # Retrieve all listings marked as favourites for a specific buyer, excluding those with status 'sold'
      favourite_listings = db.session.query(
        Listing.id,
        Listing.name,
        Listing.mileage,
        Listing.price,
        Listing.image_url,
        Listing.created_at,
        Listing.previous_owners,
        Listing.status,
        Listing.views,
        Listing.seller_id,
        Listing.agent_id
      ).select_from(cls).join(Listing, cls.listing_id == Listing.id).filter(
        cls.buyer_id == buyer_id,
        Listing.status != 'sold'
      )

      return favourite_listings.all()
