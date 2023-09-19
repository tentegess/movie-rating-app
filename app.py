import os
from flask import Flask, flash, redirect
from flask_login import LoginManager
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jinja_partials

# utilities import
from utils.db_config import db, migrate
from utils import LANG

# blueprints import
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

    # secret key used for session and db connection
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "notSecretKey")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_CONN", "mysql://root:@localhost/inz")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_PERMANENT'] = True

    # email service config
    app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
    app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSW0RD")

    # captcha keys config
    app.config['CAPTCHA_SECRET_KEY'] = os.environ.get("CAPTCHA_SECRET_KEY")

    # session lifetime
    app.permanent_session_lifetime = timedelta(days=7)

    # initialize database and migration service
    db.init_app(app)
    migrate.init_app(app, db)

    # initialize and config login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from models.Users import Users

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    # handle actions which require logged user
    @login_manager.unauthorized_handler
    def login_required():
        flash(LANG.LOGIN_REQUIRED, "alert alert-primary")
        return redirect("/login")

    jinja_partials.register_extensions(app)

    # config globals for jinja templates
    app.jinja_env.globals['current_year'] = datetime.now().year
    app.jinja_env.globals['site_key'] = os.environ.get("SITE_KEY")

    # register blueprints for templates
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
