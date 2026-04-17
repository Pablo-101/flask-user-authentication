from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    from app.config import Config

    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
    return app
