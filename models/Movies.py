from utils.db_config import db
from sqlalchemy.sql import func, text



class Movies(db.Model):

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    desc = db.Column(db.Text)
    release = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())


