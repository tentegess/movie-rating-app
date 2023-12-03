import flask
from flask import Blueprint, render_template, redirect, request, Response
from services import admin_service
from functools import wraps
from flask_login import current_user

from view_models.admin.search_user_view_model import SearchUserViewModel
from view_models.admin.add_user_view_model import AddUserViewModel
from view_models.admin.suspend_user_view_model import SuspendUserViewModel
from view_models.admin.edit_user_viev_model import EditUserViewModel

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


@admin.get("/movies")
# @admin_required
def admin_movies(page=1):
    query_vm = SearchUserViewModel()
    users = admin_service.get_users(query_vm, page)

    if query_vm.htmx_req:
        return render_template("admin/partials/users/__user_list.html", users=users)

    return render_template("admin/adm_movies.html", users=users)