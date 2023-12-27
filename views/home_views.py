import os

import flask
from flask import Blueprint, render_template, redirect, session, request, Response
from services import home_service
from utils.other_utilities import htmx_request
from datetime import date
from view_models.home.add_review_view_model import AddReviewViewModel

home = Blueprint("home", __name__, static_folder="static", template_folder="templates")


@home.get("/")
def index():
    return render_template("home/index.html")




@home.get("/search")
def search():
    query = request.args.get("query", None)
    if "Hx-Request" in request.headers:
        movies = None
        if query:
            movies = home_service.get_movies(query)
        images = None
        if movies:
            images = home_service.get_images(movies)
        return render_template("home/partials/movie_search_result.html", movies=movies, images=images)
    return render_template("home/search.html")


@home.get("/search/page/<int:page>")
@htmx_request
def next_page(page):
    query = request.args.get("query", None)
    movies = None
    if query:
        movies = home_service.get_movies(query, page)
    images = None
    if movies:
        images = home_service.get_images(movies)
    return render_template("home/partials/movie_search_result.html", movies=movies, images=images)


@home.get("/movie/<int:m_id>")
def movie_page(m_id):

    movie = home_service.get_movie(m_id)

    if not movie:
        flask.abort(404)

    avg, rev_count = home_service.get_movie_stats(m_id)

    image_path = os.path.join('static', 'media', 'posters', f'{m_id}.png')
    if not os.path.isfile(image_path):
        image_path = "/static/media/placeholder.png"
    else:
        image_path = "/" + image_path

    return render_template("home/movie_page.html", movie=movie, image=image_path,  avg=avg, count=rev_count)


@home.get("/get_review_box/<int:m_id>")
@htmx_request
def get_review(m_id):

    movie = home_service.get_movie(m_id)
    today = date.today()
    return render_template("home/partials/add_review.html", movie=movie, today=today)

@home.post("/add_review/<int:m_id>")
@htmx_request
def add_review(m_id):
    review = AddReviewViewModel()
    home_service.add_review(review, m_id)
    response = Response(status=204)
    return response


