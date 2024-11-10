from controller.BuyerController import (BuyerAddFavourite, BuyerController,
                                        BuyerFavourite, BuyerGiveReview,
                                        BuyerRemoveFavourite,
                                        BuyerSearchListing, BuyerViewFavourite,
                                        BuyerViewIncrement, BuyerViewListing,
                                        BuyerViewListingAgent,
                                        BuyerViewOneListing, BuyerViewReview)
from controller.SellerController import SellerController
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, session, url_for)

# In boundary/buyer.py
buyer_app = Blueprint('buyer_app', __name__)

@buyer_app.route('/buyer/home')
def home_page():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['buyer', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    user_id = session.get('id')
    if not user_id:
        flash("User not logged in.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    Buyerviewcontroller = BuyerViewListing()
    # Fetch listings created by the agent
    listings = Buyerviewcontroller.get_all_listings_buyer()

    # Create a list of dictionaries to hold the listing data and is_favourite property
    listings_with_favourites = []
    fav = BuyerFavourite()

    for listing in listings:
        is_favourite = fav.check_buyer_favourite(listing.id, user_id)
        # Create a dictionary for each listing with the is_favourite attribute
        listing_dict = {
            'id': listing.id,
            'name': listing.name,
            'mileage': listing.mileage,
            'price': listing.price,
            'image_url': listing.image_url,
            'previous_owners': listing.previous_owners,
            'created_at': listing.created_at,
            'views': listing.views,
            'is_favourite': is_favourite,

        }
        listings_with_favourites.append(listing_dict)

    Buyercontroller = BuyerController()
    buyer_detail = Buyercontroller.get_buyer_detail(user_id)

    if buyer_detail:
        name = buyer_detail.name
    else:
        flash("Buyer details not found.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    return render_template('/buyer/buyer_home.html', listings=listings_with_favourites, name=name)

@buyer_app.route('/buyer/search')
def search_listings():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['buyer', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    user_id = session.get('id')
    if not user_id:
        flash("User not logged in.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    search_query = request.args.get('search', '').strip()
    controller = BuyerSearchListing()

    # Fetch all listings based on the search query
    listings = controller.get_all_listings_buyer(search_query)

    fav = BuyerFavourite()
    listings_data = []

    for listing in listings:
        is_favourite = fav.check_buyer_favourite(listing.id, user_id)
        listings_data.append({
            'id': listing.id,
            'name': listing.name,
            'mileage': listing.mileage,
            'price': listing.price,
            'image_url': listing.image_url,
            'previous_owners': listing.previous_owners,
            'created_at': listing.created_at,
            'views': listing.views,
            'is_favourite': is_favourite
        })

    return jsonify({'listings': listings_data})

@buyer_app.route('/buyer/view_profile')
def view_profile():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['buyer', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    controller = BuyerController()
    buyer_detail = controller.get_buyer_detail(session.get('id'))

    if buyer_detail:
        name = buyer_detail.name
    else:
        flash("Agent details not found.")
        return redirect(url_for('agent_app.home_page'))

    return render_template('/buyer/buyer_profile.html', buyer_detail=buyer_detail, name=name)

@buyer_app.route('/buyer/viewListing/<int:listing_id>', methods=['GET', 'POST'])
def view_listing(listing_id):
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['buyer', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    # Increment the view count when a user visits this page
    view_inc_controller = BuyerViewIncrement()
    if not session.get(f'viewed_{listing_id}'):  # Prevent spamming by checking session
        view_inc_controller.increment_listing_view(listing_id)
        session[f'viewed_{listing_id}'] = True  # Set a flag in the session

    fav_controller = BuyerFavourite()
    is_favourite = fav_controller.check_buyer_favourite(listing_id=listing_id, buyer_id=session.get('id'))
    fav_add = BuyerAddFavourite()
    fav_remove = BuyerRemoveFavourite()

    if request.method == 'POST':
    # Handle adding/removing from favourites
        if session.get('profile') == 'buyer':
            user_id = session.get('id')
            if user_id is None:
                flash("User not logged in.", "error")
                return redirect(url_for('UserLogin_app.login_page'))

            if is_favourite:
                # Remove from favourites
                if fav_remove.rem_from_fav(listing_id, user_id):
                    flash("Removed from favourites successfully.", "success")
                else:
                    flash("Failed to remove from favourites.", "error")
            else:
                # Add to favourites
                if fav_add.add_to_fav(listing_id, user_id):
                    flash("Added to favourites successfully.", "success")
                else:
                    flash("Failed to add to favourites.", "error")
        else:
            flash("Only buyers can add/remove favourites.", "error")

        return redirect(url_for('buyer_app.view_listing', listing_id=listing_id))

    controller = BuyerViewOneListing()
    result = controller.get_listing_details(listing_id)

    agent_controller = BuyerViewListingAgent()
    result1 = agent_controller.get_agent_for_listing(result[0].agent_id)

    if result1:
        reviews, agent = result1
    else:
        abort(404)  # Show a 404 error if the agent is not found

    # Calculate the average star rating
    if reviews:  # Check if there are any reviews
        total_rating = sum(review['star_rating'] for review in reviews)
        average_rating = total_rating / len(reviews)
    else:
        average_rating = 0  # No reviews, so set average to 0

    if result:
        listing, seller_name, seller_email, name = result
        return render_template('/buyer/buyer_view_listing.html', listing=listing, seller_name=seller_name, seller_email=seller_email, name=name, agent=agent, reviews=reviews, average_rating=average_rating, is_favourite=is_favourite)
    else:
        abort(404)  # Show a 404 error if the listing is not found

@buyer_app.route('/buyer/view_agent/<int:listing_id>/<int:agent_id>', methods=['GET', 'POST'])
def view_agent(agent_id, listing_id):

    GiveReview = BuyerGiveReview()
    ViewReview = BuyerViewReview()
    if session.get('profile') not in ['buyer', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    if request.method == 'POST':
        # Handle review submission
        if session.get('profile') == 'buyer':
            user_id = session.get('id')
            if user_id is None:
                flash("User not logged in.", "error")
                return redirect(url_for('UserLogin_app.login_page'))

            star_rating = int(request.form.get('star_rating'))
            description = request.form.get('description')
            try:
                GiveReview.give_review(agent_id, user_id, star_rating, description, 'buyer')
                flash("Review submitted successfully.", "success")
            except ValueError as e:
                flash(str(e))
        else:
            flash("Only buyers can give reviews.", "error")
        return redirect(url_for('buyer_app.view_agent', agent_id=agent_id, listing_id=listing_id))

    # Get filter type from request (default to 'all')
    filter_by = request.args.get('filter_by', 'all')
    # Get reviews for the specified agent, filtered by 'seller', 'buyer', or 'all'
    reviews, agent = ViewReview.get_reviews_by_agent(agent_id, filter_by=filter_by)

    if agent is None:
        flash("Agent not found.", "error")
        return redirect(url_for('buyer_app.view_listing', listing_id=listing_id))

    # Calculate the average star rating
    if reviews:  # Check if there are any reviews
        total_rating = sum(review['star_rating'] for review in reviews)
        average_rating = total_rating / len(reviews)
    else:
        average_rating = 0  # No reviews, so set average to 0

    controller = SellerController()
    seller_detail = controller.get_seller_details(session.get('id'))
    name= seller_detail.name

    return render_template('/buyer/buyer_view_agent.html', agent=agent, reviews=reviews, filter_by=filter_by, average_rating=average_rating, name=name, listing_id=listing_id)

@buyer_app.route('/buyer/toggle_favourite/<int:listing_id>', methods=['POST'])
def toggle_favourite(listing_id):
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] != 'buyer':
        flash("You do not have permission to access this feature.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    user_id = session.get('id')
    if not user_id:
        flash("User not logged in.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    # Check if the listing is already a favourite
    fav_check = BuyerFavourite()
    is_favourite = fav_check.check_buyer_favourite(listing_id, user_id)

    fav_add = BuyerAddFavourite()
    fav_remove = BuyerRemoveFavourite()

    if is_favourite:
        # Remove from favourites
        if fav_remove.rem_from_fav(listing_id, user_id):
            flash("Removed from favourites successfully.", "success")
        else:
            flash("Failed to remove from favourites.", "error")
    else:
        # Add to favourites
        if fav_add.add_to_fav(listing_id, user_id):
            flash("Added to favourites successfully.", "success")
        else:
            flash("Failed to add to favourites.", "error")

    return redirect(url_for('buyer_app.view_listing', listing_id=listing_id))

@buyer_app.route('/buyer/favourites')
def fav_page():
    # Check if the user is logged in and has the required profile
    if 'profile' not in session or session['profile'] not in ['buyer', 'Admin']:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    user_id = session.get('id')
    if not user_id:
        flash("User not logged in.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    fav_controller = BuyerViewFavourite()
    buyer_id= session.get('id')
    # Fetch listings created by the agent
    listings = fav_controller.get_favourites(buyer_id)

    # Create a list of dictionaries to hold the listing data and is_favourite property
    listings_with_favourites = []
    fav = BuyerFavourite()

    for listing in listings:
        is_favourite = fav.check_buyer_favourite(listing.id, user_id)
        # Create a dictionary for each listing with the is_favourite attribute
        listing_dict = {
            'id': listing.id,
            'name': listing.name,
            'mileage': listing.mileage,
            'price': listing.price,
            'image_url': listing.image_url,
            'previous_owners': listing.previous_owners,
            'created_at': listing.created_at,
            'views': listing.views,
            'is_favourite': is_favourite
        }
        listings_with_favourites.append(listing_dict)

    Buyercontroller = BuyerController()
    buyer_detail = Buyercontroller.get_buyer_detail(user_id)

    if buyer_detail:
        name = buyer_detail.name
    else:
        flash("Buyer details not found.", "error")
        return redirect(url_for('UserLogin_app.login_page'))

    return render_template('/buyer/buyer_favourites.html', listings=listings_with_favourites, name=name)

@buyer_app.route('/buyer/loan_calculator')
def view_loan_calculator():
    user_id = session.get('id')
    Buyercontroller = BuyerController()
    buyer_detail = Buyercontroller.get_buyer_detail(user_id)
    name = buyer_detail.name

    return render_template('/buyer/buyer_loan_calculator.html', name=name)
