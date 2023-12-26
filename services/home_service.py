import os

from models.Movies import Movies
from models.Users import Users
from models.Reviews import Reviews


def get_movies(query_req, page=1):

    query = f'%{query_req}%'

    result = Movies.query.with_entities(Movies.id, Movies.title, Movies.release) \
        .filter(Movies.title.ilike(query)).paginate(per_page=5, page=page, error_out=False)
    return result if result.items else None


def get_images(movies):
    images = []
    for movie in movies:
        image_path = os.path.join('static', 'media', 'posters', f'{movie.id}.png')
        if not os.path.isfile(image_path):
            image_path = "/static/media/placeholder.png"
        else:
            image_path = "/" + image_path
        images.append(image_path)
    return images


def get_movie(movie_id):
    movie = Movies.query.filter(Movies.id == movie_id).first()
    return movie
