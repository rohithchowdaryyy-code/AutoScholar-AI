import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is not set")

    SQLALCHEMY_DATABASE_URI = "sqlite:///autoscholar.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False