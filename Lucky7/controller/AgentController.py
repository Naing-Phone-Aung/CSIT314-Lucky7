from entity.Listing import Listing
from entity.Review import Review
from entity.UserAccount import UserAccount


class AgentController:
    def get_agent_detail(self, agent_id):
        return UserAccount.get_agent_details(agent_id)

#24 Agent View Review
class AgentViewReview:
    def get_review_to_agent(self, agent_id, filter_by=None):
        return Review.get_reviews_with_names(agent_id, filter_by=filter_by)

class MarkSold:
    def mark_listing_sold(self, listing_id, buyer_email):
        return Listing.mark_listing_as_sold(listing_id, buyer_email)
