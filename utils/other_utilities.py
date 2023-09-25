import secrets
import string

from models.user_tokens import Tokens


def generate_token(ln : int) -> str:
    base = string.ascii_lowercase + string.digits
    token = ''.join(secrets.choice(base) for i in range(ln))
    while Tokens.query.filter_by(token=token).first():
        token = ''.join(secrets.choice(base) for i in range(ln))
    return token