from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from controller.AgentListingController import AgentListingController
from controller.SellerController import SellerController

seller_app = Blueprint('seller_app', __name__)

# Create an instance of AgentListingController
agent_controller = AgentListingController()

@seller_app.route('/seller')
def home_page():
    if 'profile' not in session or session['profile'] not in ['seller', 'Admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    # Get all agents along with their reviews
    agents = agent_controller.get_all_agents_with_reviews()
    seller_controller = SellerController()
    name = seller_controller.get_seller_details(session.get('id'))[0].name

    return render_template('/seller/seller_home.html', agents=agents, name=name)

@seller_app.route('/seller/profile')
def view_profile():
    if 'profile' not in session or session['profile'] not in ['seller', 'Admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = SellerController()
    seller_detail = controller.get_seller_details(session.get('id'))
    name= seller_detail[0].name
    return render_template('/seller/seller_profile.html', seller_detail=seller_detail[0], name=name)

@seller_app.route('/seller/view_agent/<int:agent_id>', methods=['GET', 'POST'])
def view_agent(agent_id):
    if session.get('profile') not in ['seller', 'Admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    if request.method == 'POST':
        # Handle review submission
        if session.get('profile') == 'seller':
            user_id = session.get('id')
            if user_id is None:
                flash("User not logged in.")
                return redirect(url_for('UserLogin_app.login_page'))

            star_rating = int(request.form.get('star_rating'))
            description = request.form.get('description')
            try:
                agent_controller.give_review(agent_id, user_id, star_rating, description, 'seller')
                flash("Review submitted successfully.", "success")
            except ValueError as e:
                flash(str(e))
        else:
            flash("Only sellers can give reviews.")
        return redirect(url_for('seller_app.view_agent', agent_id=agent_id))

    # Get filter type from request (default to 'all')
    filter_by = request.args.get('filter_by', 'all')
    # Get reviews for the specified agent, filtered by 'seller', 'buyer', or 'all'
    reviews, agent = agent_controller.get_reviews_by_agent(agent_id, filter_by=filter_by)

    if agent is None:
        flash("Agent not found.")
        return redirect(url_for('seller_app.home_page'))

    # Calculate the average star rating
    if reviews:  # Check if there are any reviews
        total_rating = sum(review['star_rating'] for review in reviews)
        average_rating = total_rating / len(reviews)
    else:
        average_rating = 0  # No reviews, so set average to 0

    controller = SellerController()
    seller_detail = controller.get_seller_details(session.get('id'))
    name= seller_detail[0].name

    return render_template('/seller/view_agent.html', agent=agent, reviews=reviews, filter_by=filter_by, average_rating=average_rating, name=name)

@seller_app.route('/seller/mylistings')
def view_my_listings():
    if 'profile' not in session or session['profile'] not in ['seller', 'Admin']:
        flash("You do not have permission to access this page.")
        return redirect(url_for('UserLogin_app.login_page'))

    seller_controller = SellerController()
    listings = seller_controller.get_seller_listings(session.get('id'))

    name= listings[0].seller_name
    print (name)


    return render_template('/seller/seller_listings.html', listings=listings, name=name)
