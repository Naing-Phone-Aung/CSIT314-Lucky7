from entity.UserAccount import UserAccount

#13 User Admin View Profile
#8 User Admin View Acc
class ViewAccount:
    @staticmethod
    def get_account_detail(account_id):
        return UserAccount.get_account_by_id(account_id)

#14 User Admin Update Profile   
#9 User Admin Update Acc
class UpdateAccount:
    @staticmethod
    def update_account(account_id, name, email, dob, phone_number, profile):
        return UserAccount.update_account_info(account_id, name, email, dob, phone_number, profile)
    
    @staticmethod
    def reset_password(account_id, new_password, confirm_password):
        # Call the entity method and return result
        return UserAccount.reset_password(account_id, new_password, confirm_password)

#14 UserAdmin Suspend Profile
#10 User Admin Suspend Acc
class SuspendAccount:
    @staticmethod
    def delete_account(account_id):
        success, message = UserAccount.delete_account(account_id)
        return success, message

#16 User Admin Search Profile
#11 User Admin Search Acc
class SearchAccount:
    @staticmethod
    def get_filtered_accounts(search_query='', profile_filter=''):
        # Calls the entity method with optional search and profile filter
        return UserAccount.get_filtered_accounts(search_query, profile_filter)


class AdminController:
    # @staticmethod
    # def get_all_accounts():
    #     return UserAccount.get_all_accounts()

    @staticmethod
    def get_profile_info(admin_id):
        return UserAccount.get_admin_detail(admin_id)


