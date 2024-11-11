from entity.Favourites import Favourites
from entity.Listing import Listing
from entity.Review import Review
from entity.UserAccount import UserAccount


class BuyerController:
    def get_buyer_detail(self, buyer_id):
        return UserAccount.get_buyer_detail(buyer_id)

class BuyerViewListing:
    def get_all_listings_buyer(self, search_query=None):
        return Listing.get_all_listings( search_query)

class BuyerSearchListing:
    def get_all_listings_buyer(self, search_query=None):
        return Listing.get_all_listings( search_query)

class BuyerViewOneListing:
    def get_listing_details(self, listing_id):
        return Listing.get_listing_details(listing_id)

class BuyerViewListingAgent:
    def get_agent_for_listing(self, agent_id):
        return Review.get_reviews_by_agent(agent_id, filter_by='all')

class BuyerViewReview:
    def get_reviews_by_agent(self, agent_id, filter_by='all'):
        reviews, agent_info = Review.get_reviews_by_agent(agent_id, filter_by)
        return reviews, agent_info


#38 Seller Give Review + Rating (to Agent)
class BuyerGiveReview:
    def give_review(self, agent_id, user_id, star_rating, description, user_profile):
        return Review.add_review(agent_id, user_id, star_rating, description, user_profile)

class BuyerFavourite:
    def check_buyer_favourite(self, listing_id, buyer_id):
      return Favourites.check_favourites(listing_id, buyer_id)

class BuyerAddFavourite:
    def add_to_fav(self, listing_id, buyer_id):
      return Favourites.add_to_favourites(listing_id, buyer_id)

class BuyerRemoveFavourite:
    def rem_from_fav(self, listing_id, buyer_id):
      return Favourites.remove_from_favourites(listing_id, buyer_id)

class BuyerViewFavourite:
    def get_favourites(self, buyer_id):
        return Favourites.get_favourite_listings_for_user(buyer_id)

class BuyerViewIncrement:
    def increment_listing_view(self, listing_id):
            """Calls the entity layer to increment the view count for a listing."""
            return Listing.increment_view_count(listing_id)

class fav_increment:
    def increment_fav(self, listing_id):
            """Calls the entity layer to increment the view count for a listing."""
            return Listing.increment_fav_count(listing_id)

class fav_decrement:
    def decrement_fav(self, listing_id):
            """Calls the entity layer to increment the view count for a listing."""
            return Listing.decrement_fav_count(listing_id)
