from flask import Blueprint, render_template, redirect, request


admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")



@admin.get("/")
def admin_main():
    return render_template("admin/adm_index.html")
