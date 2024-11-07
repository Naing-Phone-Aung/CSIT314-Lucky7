from flask import redirect, session, Blueprint, flash

UserLogout_app = Blueprint('UserLogout_app', __name__)

#6 UserAdmin Log out
#18 Agent Log out
#26 Buyer Log out
#35 Seller Log out
@UserLogout_app.route("/Logout", methods=["POST", "GET"])
def logout_page():
    
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/')
