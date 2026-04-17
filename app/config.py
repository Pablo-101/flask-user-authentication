import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "123")
    SQLALCHEMY_DATABASE_URI = "sqlite:///./user_pass.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
