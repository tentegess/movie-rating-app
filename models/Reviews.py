from utils.db_config import db
from sqlalchemy.sql import func, text


class Reviews(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    header = db.Column(db.String(128), nullable=False)
    review_text = db.Column(db.Text)
    rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),nullable=False)
    movie_id = db.Column(db.BigInteger, db.ForeignKey('movies.id', ondelete='CASCADE', onupdate='CASCADE'),nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())