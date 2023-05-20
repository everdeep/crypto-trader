import os
from dotenv import load_dotenv

load_dotenv()


# Flask config class
class Config:
    DEBUG = True
    API_SANDBOX = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class DevelopmentConfig(Config):
    BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET")


class SandboxConfig(Config):
    API_SANDBOX = True

    BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY_SANDBOX")
    BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET_SANDBOX")


class ProductionConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_PROD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


if os.environ.get("ENV") == "prod":
    config = ProductionConfig()
elif os.environ.get("ENV") == "sandbox":
    config = SandboxConfig()
else:
    config = DevelopmentConfig()
