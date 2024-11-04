from entity.Review import Review
from entity.UserAccount import UserAccount
from db import db
from sqlalchemy.orm import aliased

class AgentListingController:

    def get_all_agents_with_reviews(self):
        # Query all agents from the UserAccount table where profile is 'usedCarAgent'
        agents = UserAccount.query.filter_by(profile='usedCarAgent').all()

        # Create a list to store agent details along with reviews
        agent_list = []

        # Loop through each agent and get their reviews
        for agent in agents:
            # Query all reviews related to this agent
            reviews = Review.query.filter_by(agent_id=agent.id).all()

            # Calculate average rating
            if reviews:
                total_rating = sum(review.star_rating for review in reviews)
                average_rating = total_rating / len(reviews)
            else:
                average_rating = None

            # Create a dictionary for each agent with their details and reviews
            agent_details = {
                'id': agent.id,
                'name': agent.name,
                'email': agent.email,
                'phone_number': agent.phone_number,
                'average_rating': average_rating,
                'reviews': [
                    {
                        'star_rating': review.star_rating,
                        'description': review.description,
                        'created_at': review.created_at
                    }
                    for review in reviews
                ]
            }

            # Append the agent details to the list
            agent_list.append(agent_details)

        return agent_list


    def get_reviews_by_agent(self, agent_id, filter_by='all'):
        # Get agent details
        agent = UserAccount.query.filter_by(id=agent_id, profile='usedCarAgent').first()
        if not agent:
            return [], None

        # Create an alias for UserAccount to represent the seller
        seller_alias = aliased(UserAccount)

        # Base query for reviews
        query = Review.query \
            .outerjoin(seller_alias, Review.seller_id == seller_alias.id) \
            .filter(Review.agent_id == agent_id)

        # Apply filters for 'seller' or 'buyer' reviews
        if filter_by == 'seller':
            query = query.filter(Review.seller_id.isnot(None))
        elif filter_by == 'buyer':
            query = query.filter(Review.buyer_id.isnot(None))

        # Execute the query and fetch all reviews
        reviews = query.all()

        # Create a list of reviews with relevant details, including the seller's name if available
        review_list = [
            {
                'star_rating': review.star_rating,
                'description': review.description,
                'created_at': review.created_at,
                'reviewer_type': 'seller' if review.seller_id else 'buyer',
                'seller_name': review.seller_id and seller_alias.query.get(review.seller_id).name if review.seller_id else None
            }
            for review in reviews
        ]

        agent_details = {
            'id': agent.id,
            'name': agent.name,
            'email': agent.email,
            'phone_number': agent.phone_number
        }

        return review_list, agent_details

    def give_review(self, agent_id, user_id, star_rating, description, user_profile):
        # Validate star rating is in range 1 to 5
        if star_rating < 1 or star_rating > 5:
            raise ValueError("Star rating must be between 1 and 5.")

        # Ensure the agent exists
        agent = UserAccount.query.filter_by(id=agent_id, profile='usedCarAgent').first()
        if not agent:
            raise ValueError("Agent not found.")

        # Create a new review instance
        if user_profile == 'seller':
            new_review = Review(star_rating=star_rating, description=description, agent_id=agent_id, seller_id=user_id)
        elif user_profile == 'buyer':
            new_review = Review(star_rating=star_rating, description=description, agent_id=agent_id, buyer_id=user_id)
        else:
            raise ValueError("Invalid user profile for review. Only sellers and buyers can give reviews.")

        # Add and commit the review to the database
        db.session.add(new_review)
        db.session.commit()

        return "Review submitted successfully."
