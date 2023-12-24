import os

from flask import Blueprint, render_template, redirect, session, request
from services import home_service
from utils.other_utilities import htmx_request

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

    image_path = os.path.join('static', 'media', 'posters', f'{m_id}.png')
    if not os.path.isfile(image_path):
        image_path = "/static/media/placeholder.png"
    else:
        image_path = "/" + image_path

    return render_template("home/movie_page.html", movie=movie, image=image_path)