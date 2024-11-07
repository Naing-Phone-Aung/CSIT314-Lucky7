from entity.UserAccount import UserAccount


#5 UserAdmin Log in
#17 Agent Log in
#25 Buyer Log in
#34 Seller Log in

class UserLoginController:
    def verify_account(self, email, password):
        # Verify account and get the profile from the UserAccount entity
        is_verified, user = UserAccount.verify_account(email, password)

        if is_verified and user:
            profile = user.profile  
            return True, user.id, profile
        else:
            return False, None, None
