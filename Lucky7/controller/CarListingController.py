from entity.Listing import Listing
from entity.UserAccount import UserAccount

#19 Agent Create Listing
class AgentCreatListing:
    def create_listing(self, form_data, agent_id):
        seller_id = UserAccount.validate_seller_email(form_data['seller_email'])
        if not seller_id:
            return False, ["Seller email not found in the system."]
        return Listing.create_listing(form_data, agent_id, seller_id)    

#21 Agent Update Listing
class AgentUpdateListing:
    def update_listing(self, listing_id, form_data):
        Listing.process_update(listing_id, form_data)

#22 Agent Delete Listing
class AgentDeleteListing:
    def remove_listing(self, listing_id):
        return Listing.remove_listing(listing_id)

#23 Agent Search Listing
class AgentSearchListing:
    def get_listings_by_agent(self, agent_id, search_query=None):
        return Listing.get_listings_by_agent(agent_id, search_query)

#20 Agent View Listing
class AgentViewListing:
    def get_listing_details(self, listing_id):
        return Listing.get_listing_details(listing_id)

