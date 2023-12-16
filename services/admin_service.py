import os
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from utils.db_config import db
from models.Users import Users
from models.user_tokens import Tokens
from models.Movies import Movies
from utils.mail_service import mail_sender
from utils.other_utilities import generate_token

from flask import flash, redirect, session, render_template, request
from utils import LANG


def get_site_stats():
    stats = {
        "user_count": Users.query.count(),
        "admins": Users.query.filter_by(is_admin=True).count(),
        "banned": Users.query.filter_by(suspended=True).count(),
    }
    return stats


##################################################
# users
##################################################

def get_users(query_model, page=1):

    query = f'%{query_model.query}%'
    filters = {}

    if query_model.admins : filters["is_admin"] = True

    if query_model.suspended : filters["suspended"] = True

    result = Users.query.with_entities(Users.id, Users.name, Users.email, Users.suspended, Users.is_admin) \
        .filter(Users.name.ilike(query) | Users.email.ilike(query)).filter_by(**filters).paginate(per_page=20, page=page, error_out=False)
    return result if result.items else None


def add_user(user_vm):
    user = Users()
    user.email = user_vm.email
    user.name = user_vm.name
    user.password = generate_password_hash(user_vm.password)
    user.is_active = user_vm.active
    user.is_admin = user_vm.admin

    try:
        db.session.add(user)
        if not user_vm.active:
            gen = generate_token(32)
            token = Tokens()
            token.token = gen
            token.type = "confirm"
            token.user = user
            token.expire_at = datetime.now() + timedelta(hours=48)
            db.session.add(token)
        db.session.commit()
        if not user_vm.active:
            activation_link = f"{request.url_root}confirm_account/{gen}"
            cf = render_template("email_templates/add_account.html", name=user_vm.name, ct="48", link=activation_link, passwd=user_vm.password)
            mail_sender(user_vm.email, "Potwierdzenie rejestracji", cf)
        flash(LANG.USER_ADDED.format(user_vm.name), "alert alert-success")
    except Exception as e:
        flash(LANG.UNEXPECTED_ERROR, "alert alert-danger")
        print(e)
        db.session.rollback()


def get_user(user_id):
    user = Users.query.filter(Users.id == user_id).first()
    return user


def suspend_user(user_id, user_vm):
    user = Users.query.filter(Users.id == user_id).first()
    if user:
        try:
            user.suspended = True
            if user_vm.permanent:
                user.suspended_to = None
            else:
                user.suspended_to = user_vm.ban_time
            user.suspension_reason = user_vm.reason
            db.session.commit()
            flash(LANG.USER_SUSPENDED.format(user.name), "alert alert-success")
        except Exception as e:
            print(e)
            flash(LANG.UNEXPECTED_ERROR, "alert alert-danger")
            db.session.rollback()


def unban_user(user_id):
    user = Users.query.filter(Users.id == user_id).first()
    if user:
        user.suspended = False
        user.suspended_to = None
        user.suspension_reason = None
        db.session.commit()
        flash(LANG.USER_UNSUSPENDED.format(user.name), "alert alert-success")


def edit_user(user_id, user_vm):
    errors = {}
    user = Users.query.filter(Users.id == user_id).first()

    if user_name_exist(user_id, user_vm):
        errors["name"] = LANG.LOGIN_EXIST

    if user_email_exist(user_id, user_vm):
        errors["email"] = LANG.EMAIL_EXIST

    if errors:
        return errors

    try:
        user.name = user_vm.name
        user.email = user_vm.email
        if user_vm.password:
            user.password = generate_password_hash(user_vm.password)
        user.is_active = user_vm.active
        user.is_admin = user_vm.admin
        flash(LANG.USER_EDITED.format(user_vm.name), "alert alert-success")
        db.session.commit()
    except Exception as e:
        pass


def delete_user(user_id):
    user = Users.query.filter(Users.id == user_id).first()
    if user:
        db.session.delete(user)
        flash(LANG.USER_DELETED.format(user.name), "alert alert-success")
        db.session.commit()

def user_name_exist(user_id, user_vm):
    user = Users.query.filter(Users.name == user_vm.name).first()
    if user:
        if user.id == user_id:
            return False
        return True
    return False


def user_email_exist(user_id, user_vm):
    user = Users.query.filter(Users.email == user_vm.email).first()
    if user:
        if user.id == user_id:
            return False
        return True
    return False


def db_filler():
    for i in range(100):
        user=Users()
        user.email = f'tester{i}@jdjd.com'
        user.name = f'tester{i}'
        user.password = generate_password_hash(user.name)
        db.session.add(user)
    db.session.commit()


#############################################################
# movies
#############################################################

def add_movie(movie_vm):
    movie = Movies()
    movie.title = movie_vm.title
    movie.desc = movie_vm.desc
    movie.release = movie_vm.release


    try:
        db.session.add(movie)
        db.session.commit()

        if movie_vm.poster:
            movie_vm.poster.save(os.path.join("static/media/posters", f"{movie.id}.png"))

        flash(LANG.MOVIE_ADDED.format(movie_vm.title), "alert alert-success")
    except Exception as e:
        flash(LANG.UNEXPECTED_ERROR, "alert alert-danger")
        print(e)
        db.session.rollback()


def get_movies(query_model, page=1):

    query = f'%{query_model.query}%'

    result = Movies.query.with_entities(Movies.id, Movies.title, Movies.release) \
        .filter(Movies.title.ilike(query)).paginate(per_page=20, page=page, error_out=False)
    return result if result.items else None


def get_movie(movie_id):
    movie = Movies.query.filter(Movies.id == movie_id).first()
    return movie
