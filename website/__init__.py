from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database_login.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "asdfghkl;"
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgres://pzbivfoqweowud:605f03fb62c332436f18a481c0cb20fb8d9816f927a5d180f196e1992ee88018@ec2-3-234-204-26.compute-1.amazonaws.com:5432/d2jouh3ihigios"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin_views import admin_views

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(admin_views, url_prefix="/")

    from . import models

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')