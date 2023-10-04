
import requests
from datetime import timedelta
from flask_login import login_user
from datetime import datetime
from utils.db_config import db
from models.Users import Users
from models.user_tokens import Tokens
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, session, render_template, request, current_app
from utils import LANG
from utils.mail_service import mail_sender
from utils.other_utilities import generate_token


def add_user(user_vm):
    user = Users()
    user.email = user_vm.email
    user.name = user_vm.name
    user.password = generate_password_hash(user_vm.password)

    try:
        db.session.add(user)
        gen = generate_token(32)
        token = Tokens()
        token.token = gen
        token.type = "confirm"
        token.user = user
        token.expire_at = datetime.now() + timedelta(hours=48)
        db.session.add(token)

        activation_link = f"{request.url_root}confirm_account/{gen}"

        cf = render_template("email_templates/confirm_account.html" ,name=user_vm.name, ct="48", link=activation_link)
        mail_sender(user_vm.email, "Potwierdzenie rejestracji", cf)
        db.session.commit()
        flash(LANG.CONFIRM_LINK_SEND, "alert alert-success")
        return Users()
    except Exception as e:
        flash(LANG.UNEXPECTED_ERROR, "alert alert-danger")
        print(e)
        db.session.rollback()


def login(user_vm):
    errors = {}
    user = Users.query.filter((Users.name == user_vm.name) | (Users.email == user_vm.name)).first()

    if not user:
        errors["validation"] = LANG.WRONG_DATA
    elif not check_password_hash(user.password, user_vm.password):
        errors["validation"] = LANG.WRONG_DATA
    elif not user.is_active:
        errors["validation"] = LANG.NOT_ACTIVATED_ACCOUNT
    elif user.suspended:
        errors["validation"] = "konto zawieszone"

    if errors:
        return render_template("auth/login.html", errors=errors)

    login_user(user, remember=user_vm.remember)
    return redirect("/")


def confirm_account(token : str):
    q = (db.session.query(Tokens).join(Users).filter(Tokens.token == token, Tokens.used == False,
                                                Tokens.type == "confirm",
                                                Tokens.expire_at >= datetime.now())).first()

    if q:
        try:
            user = q.user
            qtoken = q
            user.is_active = True
            qtoken.used = True
            db.session.commit()
            flash(LANG.ACC_CONFIRMED, "alert alert-success")
        except Exception as e:
            flash(LANG.UNEXPECTED_ERROR, "alert alert-danger")
            print(e)
            db.session.rollback()
    else:
        flash(LANG.INVALID_TOKEN, "alert alert-danger")
    return redirect("/")


def sent_reset_link(user_vm):

    try:
        user = Users.query.filter((Users.name == user_vm.name) | (Users.email == user_vm.name)).first()
        if user:
            gen = generate_token(32)
            token = Tokens()
            token.token = gen
            token.type = "reset_psd"
            token.user = user
            token.expire_at = datetime.now() + timedelta(hours=48)
            db.session.add(token)
            db.session.commit()

            reset_link = f"{request.url_root}reset_password/{gen}"

            cf = render_template("email_templates/forgot_password.html", name=user.name, ct="48", link=reset_link)
            mail_sender(user.email, "Resetowanie hasła", cf)
        flash(LANG.RESET_MAIL_SEND, "alert alert-success")
    except Exception as e:
        flash(LANG.UNEXPECTED_ERROR, "alert alert-danger")
        print(e)
        db.session.rollback()


def verify_token(token):
    isToken = Tokens.query.filter(Tokens.token == token, Tokens.used == False, Tokens.type == "reset_psd", Tokens.expire_at >= datetime.now()).first()
    if not isToken:
        flash(LANG.INVALID_TOKEN, "alert alert-danger")
    return isToken


def reset_password(token, user_vm):
    q = (db.session.query(Tokens).join(Users).filter(Tokens.token == token, Tokens.used == False,
                                                     Tokens.type == "reset_psd",
                                                     Tokens.expire_at >= datetime.now())).first()

    if q:
        try:
            user = q.user
            qtoken = q
            user.password = generate_password_hash(user_vm.password)
            qtoken.used = True
            db.session.commit()
            flash(LANG.PASSWORD_CHANGED, "alert alert-success")
            return redirect("/login")
        except Exception as e:
            flash(LANG.UNEXPECTED_ERROR, "alert alert-danger")
            print(e)
            db.session.rollback()
            return redirect("/")
    flash(LANG.INVALID_TOKEN, "alert alert-danger")
    return redirect("/")




def validate_captcha():
    captcha_res = request.form.get("g-recaptcha-response")
    captcha_key = current_app.config.get('CAPTCHA_SECRET_KEY')
    captcha_request = f'https://www.google.com/recaptcha/api/siteverify?secret={captcha_key}&response={captcha_res}'
    verify_res = requests.post(captcha_request).json()

    return verify_res['success']
