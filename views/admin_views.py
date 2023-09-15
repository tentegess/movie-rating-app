from flask import Blueprint, render_template, redirect, request
from services import admin_service

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")


@admin.get("/")
def admin_main():
    stats = admin_service.get_site_stats()
    return render_template("admin/adm_index.html", stats=stats)
