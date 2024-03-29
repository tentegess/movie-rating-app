import os
from datetime import date

from flask import flash
from flask_login import current_user
from sqlalchemy import func, or_

from models.Movies import Movies
from models.Users import Users
from models.Reviews import Reviews
from models.Replies import Replies

from utils import LANG
from utils.db_config import db


def get_movies(query_req, page=1):

    query = f'%{query_req}%'

    result = Movies.query.with_entities(Movies.id, Movies.title, Movies.release) \
        .filter(Movies.title.ilike(query)).paginate(per_page=5, page=page, error_out=False)
    return result if result.items else None


def get_images(movies):
    images = []
    for movie in movies:
        image_path = os.path.join('static', 'media', 'posters', f'{movie.id}.png')
        if not os.path.isfile(image_path):
            image_path = "/static/media/placeholder.png"
        else:
            image_path = "/" + image_path
        images.append(image_path)
    return images


def get_movie(movie_id):
    movie = Movies.query.filter(Movies.id == movie_id).first()
    return movie

def get_movie_stats(movie_id):

    rating_stats = db.session.query(
        func.avg(Reviews.rating).label('average_rating'),
        func.count(Reviews.id).label('total_reviews')
    ).filter(Reviews.movie_id == movie_id).first()

    if rating_stats.total_reviews == 0:
        av_rating = None
        reviews_count = 0
    else:
        av_rating = float(rating_stats.average_rating)
        reviews_count = rating_stats.total_reviews

    return av_rating, reviews_count


def add_review(review_vm, movie_id):
    review = Reviews()
    review.header = review_vm.header
    review.review_text = review_vm.review
    review.rating = review_vm.rating
    review.user_id = current_user.id
    review.movie_id = movie_id
    db.session.add(review)
    db.session.commit()
    flash(LANG.REVIEW_ADD, "alert alert-success")
    return review


def add_reply(reply_vm, review_id):
    reply = Replies()
    reply.reply_text = reply_vm.reply
    reply.user_id = current_user.id
    reply.review_id = review_id
    db.session.add(reply)
    db.session.commit()




def find_user_review(movie_id, user_id):
    try:
        review = Reviews.query.filter_by(movie_id=movie_id, user_id=user_id).first()

        if review:
            return review
        else:
            return None
    except Exception as e:
        print(f"Błąd podczas wyszukiwania recenzji: {e}")
        return None


def get_review(review_id):
    review = Reviews.query.filter(Reviews.id == review_id).first()
    return review


def get_user(user_id):
    user = Users.query.filter(Users.id == user_id).first()
    return user


def edit_review(review_vm, review_id):
    review = Reviews.query.filter(Reviews.id == review_id).first()
    review.header = review_vm.header
    review.review_text = review_vm.review
    review.rating = review_vm.rating
    db.session.commit()
    flash(LANG.REVIEW_EDITED, "alert alert-success")
    return review


def delete_review(review_id):
    review = Reviews.query.filter(Reviews.id == review_id).first()
    idd = review.movie_id
    db.session.delete(review)
    db.session.commit()
    flash(LANG.REVIEW_DELETED, "alert alert-success")
    return idd


def count_reviews(movie_id):
    return db.session.query(Reviews, Users).join(Users, Reviews.user_id == Users.id).filter(
        Reviews.movie_id == movie_id, or_(Reviews.header != '', Reviews.review_text != '')).count()


def get_movie_reviews(movie_id):
    reviews = db.session.query(Reviews, Users).join(Users, Reviews.user_id == Users.id).filter(
        Reviews.movie_id == movie_id, or_(Reviews.header != '', Reviews.review_text != '')).all()

    if not reviews:
        return None

    result = []
    for review, user in reviews:
        result.append({
            "review_id": review.id,
            "header": review.header,
            "review_text": review.review_text,
            "rating": review.rating,
            "created_at": review.created_at,
            "user_id": user.id,
            "user_name": user.name,
            "user_email": user.email
        })

    return result


def get_user_reviews(user_id):
    user_reviews = db.session.query(
        Reviews.id, Movies.id.label('movie_id'), Movies.title, Reviews.review_text, Reviews.rating, Reviews.created_at
    ).join(Movies, Reviews.movie_id == Movies.id
           ).filter(Reviews.user_id == user_id).all()

    result = []
    for review_id, movie_id, movie_title, review_text, rating, created_at in user_reviews:
        result.append({
            "review_id": review_id,
            "movie_id": movie_id,
            "movie_title": movie_title,
            "review_text": review_text,
            "rating": rating,
            "created_at": created_at,
        })

    return result


def get_top_rated_movies():
    top_movies = (db.session.query(
        Movies.id, Movies.title, func.avg(Reviews.rating).label('average_rating')
    ).join(Reviews, Movies.id == Reviews.movie_id)
                  .group_by(Movies.id, Movies.title)
                  .order_by(func.avg(Reviews.rating).desc())
                  .limit(10)
                  .all())

    result = [{'movie_id': movie_id, 'title': title, 'average_rating': round(average_rating, 2)} for
              movie_id, title, average_rating in top_movies]

    return result


def get_new_movies():
    newest_movies = (db.session.query(
        Movies.id,
        Movies.title,
        Movies.release,
        func.avg(Reviews.rating).label('average_rating')
    ).outerjoin(Reviews, Movies.id == Reviews.movie_id)
                     .filter(Movies.release <= date.today())
                     .group_by(Movies.id, Movies.title, Movies.release)
                     .order_by(Movies.release.desc())
                     .limit(10)
                     .all())

    result = [{
        'movie_id': movie_id,
        'title': title,
        'release_date': release_date,
        'average_rating': round(average_rating, 2) if average_rating is not None else None
    } for movie_id, title, release_date, average_rating in newest_movies]

    return result


def get_replies_for_review(review_id):
    comments_query = db.session.query(
        Replies.id,
        Replies.reply_text,
        Users.id.label('user_id'),
        Users.name,
        Replies.created_at
    ).join(Users, Replies.user_id == Users.id
    ).filter(Replies.review_id == review_id
    ).order_by(Replies.created_at.asc()).all()

    comments = []
    for comment_id, reply_text, user_id, user_name, created_at in comments_query:
        comments.append({
            "comment_id": comment_id,
            "reply_text": reply_text,
            "user_id": user_id,
            "user_name": user_name,
            "created_at": created_at
        })

    return comments


def delete_reply(r_id):
    reply = Replies.query.filter(Replies.id == r_id).first()
    db.session.delete(reply)
    db.session.commit()
