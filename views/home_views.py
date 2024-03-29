import os

import flask
from flask import Blueprint, render_template, request, make_response, Response
from services import home_service
from utils.other_utilities import htmx_request
from datetime import date
from view_models.home.add_review_view_model import AddReviewViewModel
from view_models.home.add_reply_view_model import AddReplyViewModel
from flask_login import current_user, login_required

home = Blueprint("home", __name__, static_folder="static", template_folder="templates")


@home.get("/")
def index():
    top_rated = home_service.get_top_rated_movies()
    top_rated_images = []

    if top_rated:
        for movie in top_rated:
            image_path = os.path.join('static', 'media', 'posters', f"{movie['movie_id']}.png")
            if not os.path.isfile(image_path):
                image_path = "/static/media/placeholder.png"
            else:
                image_path = "/" + image_path
            top_rated_images.append(image_path)

    new_images = []
    new_movies = home_service.get_new_movies()
    if new_movies:
        for movie in new_movies:
            image_path = os.path.join('static', 'media', 'posters', f"{movie['movie_id']}.png")
            if not os.path.isfile(image_path):
                image_path = "/static/media/placeholder.png"
            else:
                image_path = "/" + image_path
            new_images.append(image_path)


    return render_template("home/index.html", top_images=top_rated_images, top_movies=top_rated,
                           new_images=new_images, new_movies=new_movies)




@home.get("/search")
def search():
    query = request.args.get("query", None)
    if "Hx-Request" in request.headers:
        movies = None
        if query:
            movies = home_service.get_movies(query)
        images = None
        ratings = None
        if movies:
            images = home_service.get_images(movies)
            ratings = []
            for movie in movies:
                avg, c = home_service.get_movie_stats(movie.id)
                ratings.append(avg)
        return render_template("home/partials/movie_search_result.html", movies=movies, images=images, ratings=ratings)
    return render_template("home/search.html")


@home.get("/search/page/<int:page>")
@htmx_request
def next_page(page):
    query = request.args.get("query", None)
    movies = None
    ratings = None
    if query:
        movies = home_service.get_movies(query, page)

    images = None
    if movies:
        images = home_service.get_images(movies)
        ratings = []
        for movie in movies:
            avg, c = home_service.get_movie_stats(movie.id)
            ratings.append(avg)
    return render_template("home/partials/movie_search_result.html", movies=movies, images=images, ratings=ratings)


@home.get("/movie/<int:m_id>")
def movie_page(m_id):

    movie = home_service.get_movie(m_id)

    if not movie:
        flask.abort(404)

    avg, rev_count = home_service.get_movie_stats(m_id)
    text_count = home_service.count_reviews(m_id)

    image_path = os.path.join('static', 'media', 'posters', f'{m_id}.png')
    if not os.path.isfile(image_path):
        image_path = "/static/media/placeholder.png"
    else:
        image_path = "/" + image_path

    return render_template("home/movie_page.html", movie=movie, image=image_path,  avg=avg, count=rev_count, text_count=text_count)


@home.get("/get_review_box/<int:m_id>")
@htmx_request
def get_review_box(m_id):

    movie = home_service.get_movie(m_id)
    today = date.today()

    if not current_user.is_authenticated:
        return render_template("home/partials/add_review.html", movie=movie, today=today)

    user_review = home_service.find_user_review(m_id, current_user.id)

    if user_review:
        return render_template("home/partials/user_review.html", movie=movie, review=user_review)

    return render_template("home/partials/add_review.html", movie=movie, today=today)


@home.post("/add_review/<int:m_id>")
@htmx_request
@login_required
def add_review(m_id):
    review = AddReviewViewModel()
    user_review=home_service.add_review(review, m_id)
    movie = home_service.get_movie(m_id)
    response = make_response(render_template("home/partials/user_review.html", movie=movie, review=user_review))
    response.headers["HX-Trigger"] = "ratingUpdate"
    return response


@home.get("/edit_review/<int:r_id>")
@htmx_request
@login_required
def edit_review(r_id):
    review = home_service.get_review(r_id)
    return render_template("home/partials/edit_review.html", review=review)


@home.post("/edit_review/<int:r_id>")
@htmx_request
@login_required
def edit_review_post(r_id):
    review_vm = AddReviewViewModel()
    review = home_service.edit_review(review_vm, r_id)
    response=make_response(render_template("home/partials/user_review.html", review=review))
    response.headers["HX-Trigger"] = "ratingUpdate"
    return response


@home.get("/get_my_review/<int:r_id>")
@htmx_request
@login_required
def get_my_rev(r_id):
    review = home_service.get_review(r_id)
    return render_template("home/partials/user_review.html", review=review)


@home.get("/delete_review/<int:r_id>")
@htmx_request
@login_required
def delete_review(r_id):
    review = home_service.get_review(r_id)
    return render_template("home/partials/delete_review.html", review=review)


@home.post("/delete_review/<int:r_id>")
@htmx_request
@login_required
def delete_review_post(r_id):
    m_id = home_service.delete_review(r_id)
    today = date.today()
    movie = home_service.get_movie(m_id)
    response=make_response(render_template("home/partials/add_review.html", movie=movie, today=today))
    response.headers["HX-Trigger"] = "ratingUpdate"
    return response


@home.get("/update_reviews/<int:m_id>")
@htmx_request
def update_reviews(m_id):
    avg, rev_count = home_service.get_movie_stats(m_id)
    return render_template("home/partials/rating_card.html", avg=avg, count=rev_count)


###################################################
# Reviews
###################################################

@home.get("/reviews/<int:m_id>")
def get_reviews_for_movie(m_id):
    movie = home_service.get_movie(m_id)
    reviews = home_service.get_movie_reviews(m_id)
    avg, rev_count = home_service.get_movie_stats(m_id)
    image_path = os.path.join('static', 'media', 'posters', f'{m_id}.png')
    if not os.path.isfile(image_path):
        image_path = "/static/media/placeholder.png"
    else:
        image_path = "/" + image_path

    return render_template("home/movie_reviews.html", movie=movie, reviews=reviews, image=image_path, avg=avg)


@home.get("/review/<int:r_id>")
def review_page(r_id):
    review = home_service.get_review(r_id)
    if not review:
        flask.abort(404)
    movie = home_service.get_movie(review.movie_id)
    user = home_service.get_user(review.user_id)
    avg, rev_count = home_service.get_movie_stats(movie.id)
    image_path = os.path.join('static', 'media', 'posters', f'{movie.id}.png')
    if not os.path.isfile(image_path):
        image_path = "/static/media/placeholder.png"
    else:
        image_path = "/" + image_path

    return render_template("home/review_page.html", movie=movie, review=review, image=image_path, avg=avg, user=user)


@home.get("/user/<int:u_id>")
def user_profile(u_id):
    user = home_service.get_user(u_id)
    user_reviews = home_service.get_user_reviews(u_id)
    images=[]
    if user_reviews:
        for review in user_reviews:
            image_path = os.path.join('static', 'media', 'posters', f"{review['movie_id']}.png")
            if not os.path.isfile(image_path):
                image_path = "/static/media/placeholder.png"
            else:
                image_path = "/" + image_path
            images.append(image_path)


    return render_template("home/user_profile.html", user=user, reviews=user_reviews, images=images)


@home.get("/reply_box/<int:r_id>")
@htmx_request
def get_reply_box(r_id):
    return render_template("home/partials/add_reply.html", r_id=r_id)

@home.post("/add_reply/<int:r_id>")
@htmx_request
@login_required
def add_reply(r_id):
    reply_vm = AddReplyViewModel.validate()

    if reply_vm.errors:
        return render_template("home/partials/add_reply.html", r_id=r_id, errors=reply_vm.to_dict().get("errors"))

    home_service.add_reply(reply_vm,r_id)
    response = make_response(render_template("home/partials/add_reply.html", r_id=r_id, errors=reply_vm.to_dict().get("errors")))
    response.headers["HX-Trigger"] = "repliesUpdate"
    return response


@home.get("/get_replies/<int:r_id>")
@htmx_request
def get_replies(r_id):
    replies = home_service.get_replies_for_review(r_id)

    return render_template("home/partials/replies_for_review.html", replies=replies, rid=r_id)

@home.post("/delete_reply/<int:r_id>")
@htmx_request
@login_required
def delete_reply(r_id):

    home_service.delete_reply(r_id)
    response = Response(status = 204)
    response.headers["HX-Trigger"] = "repliesUpdate"
    return response


