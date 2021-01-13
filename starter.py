import os
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand
from scribble import create_app, db
from scribble.models import User, Exhibit

app = create_app(os.getenv('FLASK_ENV') or 
        'config.DevelopmentConfig')
manager = Manager(app)
app.config['SECRET_KEY'] = 'mysecret'

def make_shell_context():
    return dict(app=app, db=db, User=User, Exhibit=Exhibit)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
