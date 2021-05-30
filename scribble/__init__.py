from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_script import Manager
from flask_migrate import Migrate
import os, config


db = SQLAlchemy()
admin = Admin()
migrate = Migrate()
login = LoginManager()
login.session_protection = 'strong'
login.login_view = 'main.login'
folder = os.path.dirname(os.path.abspath(__file__)) + '/static'

def create_app(config):
    app = Flask(__name__) #, static_folder = folder)
    app.config.from_object(config)
    
    db.init_app(app)
    admin.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    from . main import main as main_blueprint

    app.register_blueprint(main_blueprint)
    
    return app
