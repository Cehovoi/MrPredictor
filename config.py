import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('mysecret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
        'sqlite:///exhibits_box_dev.db'


class TestingConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
	'sqlite:///exhibits_box_test.db'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
	'sqlite:///exhibits_box.db'
