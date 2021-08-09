import os
#from flask_migrate import MigrateCommand
from scribble import create_app, db
from scribble.models import Owner, Exhibit
from flask.cli import FlaskGroup

app = create_app()


cli = FlaskGroup(app)
'''
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Owner=Owner, Exhibit=Exhibit)
'''


if __name__ == '__main__':
    cli()
