from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy

from config import app_config
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)



db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    CORS(app)
    ma.init_app(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    jwt.init_app(app)


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .product import product as product_blueprint
    app.register_blueprint(product_blueprint)

    from .configuration import configuration as config_blueprint
    app.register_blueprint(config_blueprint)

    from .image import image as image_blueprint
    app.register_blueprint(image_blueprint)


    @app.route('/')
    def index():
        db.create_all()
        return 'Server works'

    def init_users():
        from app import models
        user = models.User()
        user.id = 1
        user.username = 'uyen'
        user.first_name = 'Uyen'
        user.is_admin = True
        user.__setattr__('password', '1234qwer')
        db.session.add(user)
        db.session.commit()

    return app

