from flask import Blueprint, render_template, redirect, session

home = Blueprint("home", __name__, static_folder="static", template_folder="templates")


@home.get("/")
def index():
    session["test"] = "test"
    return render_template("home/index.html")
