from utils.db_config import db
from sqlalchemy.sql import func, text


class Tokens(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    token = db.Column(db.String(32), unique=True, nullable=False)
    type = db.Column(db.String(16), nullable=False)
    expire_at = db.Column(db.DateTime, server_default=func.now())
    used = db.Column(db.Boolean, server_default=text('FALSE'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
