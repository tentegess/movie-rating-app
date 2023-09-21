from werkzeug.security import generate_password_hash

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


def get_users(query_model, page=1):
    query = f'%{query_model.query}%'

    result = Users.query.with_entities(Users.id, Users.name, Users.email, Users.suspended, Users.is_admin) \
        .filter(Users.name.ilike(query) | Users.email.ilike(query)).paginate(per_page=20, page=page)
    return result if result.items else None


# def db_filler():
#     for i in range(100):
#         user=Users()
#         user.email = f'tester{i}@jdjd.com'
#         user.name = f'tester{i}'
#         user.password = generate_password_hash(user.name)
#         db.session.add(user)
#     db.session.commit()