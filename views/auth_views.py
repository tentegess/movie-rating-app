from flask import Blueprint, render_template, redirect, request
from view_models.auth.regiser_view_model import RegisterViewModel
from view_models.auth.login_view_model import LoginViewModel
from services import auth_service

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")


@auth.get("/login")
def login():
    return render_template("auth/login.html")


@auth.post("/login")
def login_post():
    user_vm = LoginViewModel.validate()
    if user_vm.errors:
        print(user_vm.to_dict())
        return render_template("auth/login.html", errors=user_vm.to_dict().get("errors"))

    return auth_service.login_user(user_vm)


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
    return auth_service.confirm_account(token)


