from entity.UserAccount import UserAccount

class UserLoginController:
    
    def verify_account(self, email, password):
        # Pass data to the UserAccount entity's verify_account method
        is_verified, user = UserAccount.verify_account(email, password)
        
        if is_verified and user:
            return True, user
        else:
            return False, None
