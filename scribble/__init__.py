from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os, config


db = SQLAlchemy()
admin = Admin()
login = LoginManager()
migrate = Migrate()
login.login_view = 'main.login'

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    admin.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)
    
    return app
