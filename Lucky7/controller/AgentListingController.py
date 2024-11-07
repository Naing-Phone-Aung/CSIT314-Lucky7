from entity.Review import Review

#206 Seller View Reivew (to Agent)
class SellerViewReview:
    def get_reviews_by_agent(self, agent_id, filter_by='all'):
        reviews, agent_info = Review.get_reviews_by_agent(agent_id, filter_by)
        return reviews, agent_info
    
    def get_all_agents_with_reviews(self):
        return Review.get_all_agents_with_reviews() 

#38 Seller Give Review + Rating (to Agent)
class SellerGiveReview:
    def give_review(self, agent_id, user_id, star_rating, description, user_profile):
        return Review.add_review(agent_id, user_id, star_rating, description, user_profile)
