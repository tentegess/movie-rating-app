from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, logout_user

from view_models.auth.regiser_view_model import RegisterViewModel
from view_models.auth.login_view_model import LoginViewModel
from view_models.auth.forgot_psd_view_model import ForgotPsdViewModel
from services import auth_service

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")


@auth.get("/login")
def login():
    return render_template("auth/login.html")


@auth.post("/login")
def login_post():
    user_vm = LoginViewModel.validate()
    if user_vm.errors:
        return render_template("auth/login.html", errors=user_vm.to_dict().get("errors"))

    return auth_service.login(user_vm)


@auth.get("/register")
def register():
    return render_template("auth/register.html")


@auth.post("/register")
def register_post():
    user_vm = RegisterViewModel().validate()
    if user_vm.errors:
        return render_template("auth/register.html", errors=user_vm.to_dict().get("errors"))
    auth_service.add_user(user_vm)

    return redirect('login')


@auth.get("/confirm_account/<token>")
def confirm_acc(token=""):
    return auth_service.confirm_account(str(token))


@auth.get("/forgot_password")
def forgot_password():
    return render_template("auth/forgot_password.html")


@auth.post("/forgot_password")
def forgot_password_post():
    user_vm = ForgotPsdViewModel.validate()
    if user_vm.errors:
        return render_template("auth/forgot_password.html", errors=user_vm.to_dict().get("errors"))
    auth_service.sent_reset_link(user_vm)
    return redirect("/")

@auth.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')
