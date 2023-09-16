import os
from flask import Flask, flash, redirect
from flask_login import LoginManager
from dotenv import load_dotenv
from datetime import datetime, timedelta

from utils.db_config import db, migrate
from utils import LANG

from views.auth_views import auth
from views.home_views import home
from views.admin_views import admin

load_dotenv()


def create_app():
    """

    create_app()

    This method creates and configures a Flask application.

    Returns:
        Flask: The created Flask application.

    """
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

    app.config['CAPTCHA_SECRET_KEY'] = os.environ.get("CAPTCHA_SECRET_KEY")

    app.permanent_session_lifetime = timedelta(days=7)

    db.init_app(app)
    app.config['SESSION_SQLALCHEMY'] = db
    app.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"

    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from models.Users import Users

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    @login_manager.unauthorized_handler
    def login_required():
        flash(LANG.LOGIN_REQUIRED, "alert alert-primary")
        return redirect("/login")

    app.jinja_env.globals['current_year'] = datetime.now().year
    app.jinja_env.globals['site_key'] = os.environ.get("SITE_KEY")

    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(admin, url_prefix="/admin")

    return app


app = create_app()


@app.errorhandler(404)
def not_found(e):
    return "Page not found"


if __name__ == "__main__":
    app.run(debug=True)
