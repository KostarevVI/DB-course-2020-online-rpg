from os import path
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    global db
    app = Flask(__name__)

    app.config['SECRET_KEY'] = ';lkjr-fj3 984paijOIjd123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:6559@localhost/database_for_game_big'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app, session_options={"expire_on_commit": False})

    from .auth import auth
    from .game_menu import game_menu
    from .play_screen import play_screen

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(game_menu, url_prefix='/')
    app.register_blueprint(play_screen, url_prefix='/')

    from .models import UserDatum

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return UserDatum.query.get(int(id))

    return app
