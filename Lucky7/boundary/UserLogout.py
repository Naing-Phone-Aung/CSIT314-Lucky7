from flask import redirect, session, Blueprint, flash

UserLogout_app = Blueprint('UserLogout_app', __name__)

@UserLogout_app.route("/Logout", methods=["POST", "GET"])
def logout_page():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/')
