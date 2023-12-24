import secrets
import string
from functools import wraps

import flask
from flask import request
from models.user_tokens import Tokens


def generate_token(ln : int) -> str:
    base = string.ascii_lowercase + string.digits
    token = ''.join(secrets.choice(base) for i in range(ln))
    while Tokens.query.filter_by(token=token).first():
        token = ''.join(secrets.choice(base) for i in range(ln))
    return token


def htmx_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Hx-Request" in request.headers:
            return f(*args, **kwargs)
        return flask.abort(404)

    return decorated_function
