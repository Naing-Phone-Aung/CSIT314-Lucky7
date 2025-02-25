from entity.UserAccount import UserAccount
from entity.Listing import Listing

#36 View Favorite
#37 View Count
class SellerController:
    def get_seller_details(self, seller_id):
        return UserAccount.get_seller_details(seller_id)

    def get_seller_listings(self, seller_id):
        return Listing.get_seller_listings(seller_id)
