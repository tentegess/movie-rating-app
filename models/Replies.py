from utils.db_config import db
from sqlalchemy.sql import func, text


class Replies(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    reply_text = db.Column(db.Text)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    review_id = db.Column(db.BigInteger, db.ForeignKey('reviews.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
