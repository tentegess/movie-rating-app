import os
from flask import Flask
from dotenv import load_dotenv
from datetime import timedelta
from flask_session import Session

from utils.db_config import db, migrate

from views.auth_views import auth
from views.home_views import home

from datetime import datetime

load_dotenv()



def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "notSecretKey")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_CONN", "mysql://root:@localhost/inz")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_PERMANENT'] = True

    app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
    app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSW0RD")

    app.permanent_session_lifetime = timedelta(days=7)

    db.init_app(app)
    app.config['SESSION_SQLALCHEMY'] = db
    app.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"

    migrate.init_app(app, db)

    app.jinja_env.globals['current_year'] = datetime.now().year

    app.register_blueprint(auth)
    app.register_blueprint(home)

    return app


app = create_app()

with app.app_context():
    Session(app)


@app.errorhandler(404)
def not_found(e):
    return "Page not found"

if __name__ == "__main__":
    app.run(debug=True)
