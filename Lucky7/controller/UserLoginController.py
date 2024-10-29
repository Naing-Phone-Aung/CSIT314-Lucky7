from entity.UserAccount import UserAccount

class UserLoginController:

    def verify_account(self, email, password):
        # Verify account and get the profile from the UserAccount entity
        is_verified, user = UserAccount.verify_account(email, password)

        if is_verified and user:
            profile = user.profile  # Get the profile type from the UserAccount instance
            return True, user.id, profile
        else:
            return False, None, None
