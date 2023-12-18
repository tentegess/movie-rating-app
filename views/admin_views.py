import os

import flask
from flask import Blueprint, render_template, redirect, request, Response
from services import admin_service
from functools import wraps
from flask_login import current_user

from view_models.admin.search_user_view_model import SearchUserViewModel
from view_models.admin.add_user_view_model import AddUserViewModel
from view_models.admin.suspend_user_view_model import SuspendUserViewModel
from view_models.admin.edit_user_viev_model import EditUserViewModel

from view_models.admin.add_movie_view_model import AddMovieViewModel

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")


def admin_required(f):
    """
    A decorator that checks whether the current user is an authenticated admin.

    Parameters:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Example usage:
        @admin_required
        def admin_dashboard():
            # code for admin dashboard
            pass
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return flask.abort(404)
        if not current_user.is_admin:
            return flask.abort(404)
        return f(*args, **kwargs)

    return decorated_function


def htmx_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Hx-Request" in request.headers:
            return f(*args, **kwargs)
        return flask.abort(404)

    return decorated_function


@admin.get("/")
# @admin_required
def admin_main():
    stats = admin_service.get_site_stats()
    return render_template("admin/adm_index.html", stats=stats)


@admin.get("/users/page/<int:page>")
@admin.get("/users/page/")
@admin.get("/users")
# @admin_required
def admin_users(page=1):
    query_vm = SearchUserViewModel()
    users = admin_service.get_users(query_vm, page)

    if query_vm.htmx_req:
        return render_template("admin/partials/users/__user_list.html", users=users)

    return render_template("admin/adm_users.html", users=users)



@admin.get("/add_user")
@htmx_request
# @admin_required
def add_user():
    return render_template("admin/partials/users/__add_user_form.html")


@admin.post("/add_user")
@htmx_request
# @admin_required
def add_user_post():
    user_vm = AddUserViewModel.validate()
    if user_vm.errors:
        return render_template("admin/partials/users/__add_user_form.html", errors=user_vm.to_dict().get("errors"))
    admin_service.add_user(user_vm)
    response = Response(status = 204)
    response.headers["HX-Trigger"] = "listRefresh"
    return response


@admin.get("/get_user/<int:user_id>")
@htmx_request
def get_user(user_id):
    user = admin_service.get_user(user_id)
    return render_template("admin/partials/users/__user_profile.html", user=user)

@admin.get("/suspend_user/<int:user_id>")
def suspend_user(user_id):
    user = admin_service.get_user(user_id)
    return render_template("admin/partials/users/__suspend_user.html", user=user)

@admin.post("/suspend_user/<int:user_id>")
def suspend_user_post(user_id):
    user_vm = SuspendUserViewModel.validate()
    if user_vm.errors:
        user = admin_service.get_user(user_id)
        return render_template("admin/partials/users/__suspend_user.html", user=user, errors=user_vm.to_dict().get("errors"))
    admin_service.suspend_user(user_id, user_vm)
    response = Response(status=204)
    response.headers["HX-Trigger"] = "listRefresh"
    return response


@admin.get("/unban_user/<int:user_id>")
def unban_user(user_id):
    user = admin_service.get_user(user_id)
    return render_template("admin/partials/users/__unban_user.html", user=user)


@admin.post("/unban_user/<int:user_id>")
def unban_user_post(user_id):
    admin_service.unban_user(user_id)
    response = Response(status=204)
    response.headers["HX-Trigger"] = "listRefresh"
    return response


@admin.get("/edit_user/<int:user_id>")
def edit_user(user_id):
    user = admin_service.get_user(user_id)
    return render_template("admin/partials/users/__edit_user.html", user=user)


@admin.post("/edit_user/<int:user_id>")
def edit_user_post(user_id):
    user_vm = EditUserViewModel.validate()
    if user_vm.errors:
        user = admin_service.get_user(user_id)
        return render_template("admin/partials/users/__edit_user.html", user=user,
                               errors=user_vm.to_dict().get("errors"))

    errors = admin_service.edit_user(user_id, user_vm)

    if errors:
        user = admin_service.get_user(user_id)
        return render_template("admin/partials/users/__edit_user.html", user=user,
                               errors=errors)

    response = Response(status=204)
    response.headers["HX-Trigger"] = "listRefresh"
    return response

@admin.get("/delete_user/<int:user_id>")
def delete_user(user_id):
    user = admin_service.get_user(user_id)
    return render_template("admin/partials/users/__delete_user.html", user=user)


@admin.post("/delete_user/<int:user_id>")
def delete_user_post(user_id):
    admin_service.delete_user(user_id)
    response = Response(status=204)
    response.headers["HX-Trigger"] = "listRefresh"
    return response


@admin.get("/debug1")
def aaa():
    admin_service.db_filler()
    return redirect("admin/users")


@admin.get("/movies/page/<int:page>")
@admin.get("/movies/page/")
@admin.get("/movies")
# @admin_required
def admin_movies(page=1):
    query_vm = SearchUserViewModel()
    movies = admin_service.get_movies(query_vm, page)

    if query_vm.htmx_req:
        return render_template("admin/partials/movies/__movie_list.html", movies=movies)

    return render_template("admin/adm_movies.html", movies=movies)


@admin.get("/add_movie")
@htmx_request
# @admin_required
def add_movie():
    return render_template("admin/partials/movies/__add_movie_form.html")


@admin.post("/add_movie")
@htmx_request
# @admin_required
def add_movie_post():
    movie_vm = AddMovieViewModel.validate()
    if movie_vm.errors:
        return render_template("admin/partials/movies/__add_movie_form.html", errors=movie_vm.to_dict().get("errors"))
    admin_service.add_movie(movie_vm)
    response = Response(status = 204)
    response.headers["HX-Trigger"] = "listRefresh"
    return response

@admin.get("/get_movie/<int:movie_id>")
@htmx_request
def get_movie(movie_id):
    movie = admin_service.get_movie(movie_id)
    image_path = os.path.join('static', 'media', 'posters', f'{movie_id}.png')
    if not os.path.isfile(image_path):
        image_path = "/static/media/placeholder.png"
    else:
        image_path = "/"+image_path

    return render_template("admin/partials/movies/__movie_profile.html", movie=movie, image=image_path)


@admin.get("/edit_movie/<int:movie_id>")
@htmx_request
def edit_movie(movie_id):
    movie = admin_service.get_movie(movie_id)
    image_path = os.path.join('static', 'media', 'posters', f'{movie_id}.png')
    if not os.path.isfile(image_path):
        image_path = "/static/media/placeholder.png"
    else:
        image_path = "/"+image_path

    return render_template("admin/partials/movies/__edit_movie.html", movie=movie, image=image_path)


@admin.post("/edit_movie/<int:movie_id>")
def edit_movie_post(movie_id):
    movie_vm = AddMovieViewModel.validate()
    if movie_vm.errors:
        movie = admin_service.get_movie(movie_id)
        image_path = os.path.join('static', 'media', 'posters', f'{movie_id}.png')
        if not os.path.isfile(image_path):
            image_path = "/static/media/placeholder.png"
        else:
            image_path = "/" + image_path
        return render_template("admin/partials/movies/__edit_movie.html", movie=movie,
                               errors=movie_vm.to_dict().get("errors"), image=image_path)

    admin_service.edit_movie(movie_id, movie_vm)


    response = Response(status=204)
    response.headers["HX-Trigger"] = "listRefresh"
    return response


@admin.get("/delete_movie/<int:movie_id>")
def delete_movie(movie_id):
    movie = admin_service.get_movie(movie_id)

    image_path = os.path.join('static', 'media', 'posters', f'{movie_id}.png')
    if not os.path.isfile(image_path):
        image_path = "/static/media/placeholder.png"
    else:
        image_path = "/" + image_path

    return render_template("admin/partials/movies/__delete_movie.html", movie=movie, image=image_path)



@admin.post("/delete_movie/<int:movie_id>")
def delete_movie_post(movie_id):
    admin_service.delete_movie(movie_id)
    response = Response(status=204)
    response.headers["HX-Trigger"] = "listRefresh"
    return response