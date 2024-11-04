from sqlalchemy.orm import aliased
from db import db
from entity.UserAccount import UserAccount
from entity.Review import Review



class AgentController:
    def get_agent_detail(self, agent_id):
        # Create an alias for the UserAccount table to use for the agent


        # Base query with joins
        detail = db.session.query(
            UserAccount.name,
            UserAccount.email,
            UserAccount.phone_number,
            UserAccount.dob,
        ).filter(UserAccount.id == agent_id).all()

        return detail

    def get_review_to_agent(self, agent_id):
        # Create aliases for the UserAccount table
        agent = aliased(UserAccount)
        seller = aliased(UserAccount)

        # Query with joins using aliases
        reviews = db.session.query(
            Review.star_rating,
            Review.description,
            Review.created_at,
            seller.name.label('seller_name'),  # Seller's name alias
            agent.name.label('agent_name'),    # Agent's name alias
        ).join(agent, Review.agent_id == agent.id) \
        .join(seller, Review.seller_id == seller.id) \
        .filter(Review.agent_id == agent_id) \
        .all()


        return reviews
