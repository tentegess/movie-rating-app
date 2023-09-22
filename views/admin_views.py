import flask
from flask import Blueprint, render_template, redirect, request
from services import admin_service
from functools import wraps
from flask_login import current_user


from view_models.admin.search_user_view_model import SearchUserViewModel

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


@admin.get("/")
#@admin_required
def admin_main():
    stats = admin_service.get_site_stats()
    return render_template("admin/adm_index.html", stats=stats)


@admin.get("/users")
def admin_users():
    query_vm = SearchUserViewModel()
    users = admin_service.get_users(query_vm)

    if query_vm.htmx_req:
        return render_template("admin/partials/users/__user_list.html", users=users)

    return render_template("admin/adm_users.html", users=users)

@admin.get("/users/page/<int:page>")
def users_page(page):
    query_vm = SearchUserViewModel()
    if query_vm.htmx_req:
        # import time
        # time.sleep(2)
        users = admin_service.get_users(query_vm, page)
        return render_template("admin/partials/users/__users_next_page.html", users=users)

    return flask.abort(404)

# @admin.get("/debug1")
# def aaa():
#     admin_service.db_filler()


