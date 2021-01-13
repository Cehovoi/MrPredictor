import os
import pytest

from scribble.models import User
from scribble import db
app_dir=os.path.abspath(os.path.dirname(__file__))

print(os.environ.get('TESTING_DATABASE_URI'))


'''@pytest.fixture(scope='module')
def init_database():

    u1 = User(username = 'Polya')
    User.set_password(u1, '123')    
    db.session.add(u1)
    db.session.commit()
 
    yield db   
    db.drop_all()

def test_db(init_database):
    print('tests DB')
    assert init_database'''
