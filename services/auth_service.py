import secrets
import string
from datetime import timedelta
from flask_login import login_user
from datetime import datetime
from utils.db_config import db
from models.Users import Users
from models.user_tokens import Tokens
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, session, render_template, request
from utils import LANG
from utils.mail_service import mail_sender

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
        db.session.commit()

        activation_link = f"{request.url_root}confirm_account/{gen}"

        cf = render_template("email_templates/confirm_account.html" ,name=user_vm.name, ct="48", link=activation_link)
        mail_sender(user_vm.email, "Potwierdzenie rejestracji", cf)
        flash(LANG.CONFIRM_LINK_SEND, "alert alert-success")
        return Users()
    except Exception as e:
        flash(LANG.UNEXPECTED_ERROR, "alert alert-danger")
        print(e)
        db.session.rollback()


def login(user_vm):
    errors = {}
    user = Users.query.filter((Users.name == user_vm.name) | (Users.email == user_vm.name)).one_or_none()

    if not user:
        errors["validation"] = LANG.WRONG_DATA
    elif not check_password_hash(user.password, user_vm.password):
        errors["validation"] = LANG.WRONG_DATA
    elif not user.is_active:
        errors["validation"] = LANG.NOT_ACTIVATED_ACCOUNT

    if errors:
        return render_template("auth/login.html", errors=errors)

    login_user(user, remember=user_vm.remember)
    return redirect("/")


def confirm_account(token : str):
    user = Users.query.join(Tokens, Users.tokens).filter(Tokens.token == token, Tokens.used == False, Tokens.type == "confirm" ,Tokens.expire_at >= datetime.now()).one_or_none()
    if user:
        try:
            user.is_active = True
            user.tokens[0].used = True
            db.session.commit()
            flash(LANG.ACC_CONFIRMED, "alert alert-success")
        except Exception as e:
            flash(LANG.UNEXPECTED_ERROR, "alert alert-danger")
            print(e)
            db.session.rollback()
    else:
        flash(LANG.INVALID_TOKEN, "alert alert-danger")
    return redirect("/")

def generate_token(ln : int) -> str:
    base = string.ascii_lowercase + string.digits
    token = ''.join(secrets.choice(base) for i in range(ln))
    while Tokens.query.filter_by(token=token).first():
        token = ''.join(secrets.choice(base) for i in range(ln))
    return token
