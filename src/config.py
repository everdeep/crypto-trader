import os
from dotenv import load_dotenv

load_dotenv()


# Flask config class
class Config:
    SECRET = os.environ.get("SECRET")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

    # Global testing api key
    BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET")


class DevelopmentConfig(Config):
    DEBUG = True

    # Global testing api key
    BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY_DEV")
    BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET_DEV")

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

    # Global testing api key
    BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY_PROD")
    BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET_PROD")

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_PROD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


if os.environ.get("ENV") == "production":
    app_config = ProductionConfig()
else:
    app_config = DevelopmentConfig()
