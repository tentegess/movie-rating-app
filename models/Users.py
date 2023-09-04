from utils.db_config import db
from sqlalchemy.sql import func, text
from flask_login import UserMixin


class Users(UserMixin, db.Model):

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, server_default=text('FALSE'))
    is_admin = db.Column(db.Boolean, server_default=text('FALSE'))
    suspended = db.Column(db.Boolean, server_default=text('FALSE'))
    suspended_to = db.Column(db.Date)
    suspension_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    tokens = db.relationship('Tokens', backref='user', cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")


