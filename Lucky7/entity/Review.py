from db import db
from datetime import datetime
from sqlalchemy.orm import aliased
from sqlalchemy import case

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    star_rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    agent_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=True)

    def __init__(self, star_rating, description, agent_id, seller_id=None, buyer_id=None):
        if 1 <= star_rating <= 5:
            self.star_rating = star_rating
        else:
            raise ValueError("Star rating must be between 1 and 5")
        self.description = description
        self.agent_id = agent_id
        self.seller_id = seller_id
        self.buyer_id = buyer_id
    
    ########################### AgentController + AgentListingController ###########################
    @staticmethod
    def get_reviews_for_agent(agent_id, filter_by=None):
        # Base query for reviews related to a specific agent
        query = db.session.query(Review).filter_by(agent_id=agent_id)

        if filter_by == 'seller':
            query = query.filter(Review.seller_id.isnot(None))
        elif filter_by == 'buyer':
            query = query.filter(Review.buyer_id.isnot(None))

        return query.all()

    ########################### AgentListingController.py  ###########################
    @staticmethod
    def calculate_average_rating(reviews):
        if not reviews:
            return None
        total_rating = sum(review.star_rating for review in reviews)
        return total_rating / len(reviews)

    @staticmethod
    def add_review(agent_id, user_id, star_rating, description, user_profile):
        if star_rating < 1 or star_rating > 5:
            raise ValueError("Star rating must be between 1 and 5.")
        
        new_review = Review(
            star_rating=star_rating,
            description=description,
            agent_id=agent_id,
            seller_id=user_id if user_profile == 'seller' else None,
            buyer_id=user_id if user_profile == 'buyer' else None
        )
        db.session.add(new_review)
        db.session.commit()
        return "Review submitted successfully."

    @staticmethod
    def format_reviews(reviews):
        from entity.UserAccount import UserAccount
        formatted_reviews = []
        for review in reviews:
            # Determine if the reviewer is a seller or buyer and get the name accordingly
            reviewer_id = review.seller_id if review.seller_id else review.buyer_id
            reviewer = db.session.get(UserAccount, reviewer_id)

            reviewer_name = reviewer.name if reviewer else "Unknown"

            formatted_reviews.append({
                'star_rating': review.star_rating,
                'description': review.description,
                'created_at': review.created_at,
                'reviewer_type': 'seller' if review.seller_id else 'buyer',
                'reviewer_name': reviewer_name
            })
        return formatted_reviews
    
    def get_all_agents_with_reviews():
        from entity.UserAccount import UserAccount
        agents = UserAccount.get_all_agents()
        agent_list = []
        for agent in agents:
            reviews = Review.get_reviews_for_agent(agent.id)
            average_rating = Review.calculate_average_rating(reviews)
            formatted_reviews = Review.format_reviews(reviews)
            agent_list.append({
                'id': agent.id,
                'name': agent.name,
                'email': agent.email,
                'phone_number': agent.phone_number,
                'average_rating': average_rating,
                'reviews': formatted_reviews
            })
        return agent_list
    
    @staticmethod
    def get_reviews_by_agent(agent_id, filter_by='all'):
        from entity.UserAccount import UserAccount
        agent = UserAccount.get_agent_details(agent_id)
        if not agent:
            return [], None
        reviews = Review.get_reviews_for_agent(agent_id, filter_by=filter_by)
        formatted_reviews = Review.format_reviews(reviews)
        
        reviewlist = formatted_reviews, {
            'id': agent.id,
            'name': agent.name,
            'email': agent.email,
            'phone_number': agent.phone_number
        }

        return reviewlist
    
    ########################### AgentController  ###########################
    @staticmethod
    def get_reviews_with_names(agent_id, filter_by=None):
        from entity.UserAccount import UserAccount
        seller_alias = aliased(UserAccount)
        buyer_alias = aliased(UserAccount)

        query = db.session.query(
            Review.star_rating,
            Review.description,
            Review.created_at,
            case(
                (Review.seller_id.isnot(None), seller_alias.name),
                (Review.buyer_id.isnot(None), buyer_alias.name)
            ).label("reviewer_name")
        ).outerjoin(seller_alias, Review.seller_id == seller_alias.id) \
        .outerjoin(buyer_alias, Review.buyer_id == buyer_alias.id) \
        .filter(Review.agent_id == agent_id)

        # Apply the filter
        if filter_by == 'seller':
            query = query.filter(Review.seller_id.isnot(None))
        elif filter_by == 'buyer':
            query = query.filter(Review.buyer_id.isnot(None))

        reviews = query.all()

        reviewList = [
            {
                'star_rating': review.star_rating,
                'description': review.description,
                'created_at': review.created_at,
                'reviewer_name': review.reviewer_name
            }
            for review in reviews
        ]

        return reviewList
