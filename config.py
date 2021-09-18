import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = 'mysecret'#os.environ.get('mysecret')
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

class ProductionConfigPostgres(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://splmwtmlfpydec:08c251c0332480445243a388f76f46b2cfd787b4116aa4e5750b0718f6a3fdca@ec2-54-74-60-70.eu-west-1.compute.amazonaws.com:5432/dbvaoqla3vesf9'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
                              "mysql+mysqlconnector://root:root@mysqldb/predictor_base"


