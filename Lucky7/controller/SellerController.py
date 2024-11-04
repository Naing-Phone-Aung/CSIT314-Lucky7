from sqlalchemy.orm import aliased
from db import db
from entity.UserAccount import UserAccount
from entity.Listing import Listing



class SellerController:
    def get_seller_details(self, seller_id):

        # Base query with joins
        detail = db.session.query(
            UserAccount.name,
            UserAccount.email,
            UserAccount.phone_number,
            UserAccount.dob,
        ).filter(UserAccount.id == seller_id).all()

        return detail

    def get_seller_listings(self, seller_id):
        AgentAccount = aliased(UserAccount)  # Alias for the agent's account

        listing = db.session.query(
            Listing.id,
            Listing.name,
            Listing.mileage,
            Listing.price,
            Listing.image_url,
            Listing.created_at,
            Listing.previous_owners,
            Listing.price,
            Listing.status,
            UserAccount.name.label("seller_name"),  # Fetch seller's name
            AgentAccount.name.label("agent_name")   # Fetch agent's name
        ).join(UserAccount, Listing.seller_id == UserAccount.id) \
        .join(AgentAccount, Listing.agent_id == AgentAccount.id) \
        .filter(Listing.seller_id == seller_id).all()

        return listing
