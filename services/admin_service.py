from utils.db_config import db
from models.Users import Users
from models.user_tokens import Tokens
from flask import flash, redirect, session, render_template, request
from utils import LANG

def get_site_stats():
    stats = {
        "user_count": Users.query.count(),
        "admins": Users.query.filter_by(is_admin=True).count(),
        "banned": Users.query.filter_by(suspended=True).count(),
    }
    return stats

def get_users():
    result = Users.query.with_entities(Users.id, Users.name, Users.email, Users.suspended, Users.is_admin).all()
    return result