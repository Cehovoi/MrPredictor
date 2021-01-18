import pytest
from scribble import create_app
from scribble.models import User
from scribble.models import Exhibit
from scribble.predictor import predictor
from scribble import db
from tests import valid_num


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('config.TestingConfig')
    flask_app.config['SECRET_KEY'] = 'mysecret'
    
    testing_client = flask_app.test_client()
 
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client
 
    ctx.pop()

@pytest.fixture(scope='module')
def init_db():
    
    db.create_all()

    u1 = User(username = 'Polya')
    User.set_password(u1, '123')    
    
    num = valid_num()
    predictions = predictor(num) 
    e1 = Exhibit(name = 'Sam', 
            predictions = predictions[0], img =predictions[1])
    picture = predictions[1].split(',')

    db.session.add_all([u1, e1])
    db.session.commit()
 
    yield db

    db.drop_all()


def test_admin(test_client, init_db):
    response = test_client.post('/login',
                                data=dict(username='Polya', password='123'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout and Start page' in response.data


def test_exhibit(test_client, init_db):
    response = test_client.post('/you',
                                data=dict(name='Pit', size='12'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'love makes the world go round' in response.data
    
    response = test_client.get('/predictions', follow_redirects=True)
    
    assert b'Pit' in response.data
    assert b'Sam' in response.data

