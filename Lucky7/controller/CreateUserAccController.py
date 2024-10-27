from entity.UserAccount import UserAccount

class CreateUserAccController:

    def create_user_account(self, name, email, password, confirm_password, dob, phone_number):
        # Create a new user account using the UserAccount model
        result, message = UserAccount.create_account(name, email, password, confirm_password, dob, phone_number)
        
        # Return appropriate message based on result
        if result and message:
            return True, message
        else:
            return False, message
