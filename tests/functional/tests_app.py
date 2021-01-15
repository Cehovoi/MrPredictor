import pytest
from scribble import create_app
from scribble.models import User
from scribble import db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('config.TestingConfig')

    testing_client = flask_app.test_client()
 
 
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client
 
    ctx.pop()

@pytest.fixture(scope='module')
def init_db():
    pass


@pytest.mark.parametrize('route, response_code, some_text',[
    ('/', 200, 'Do you want to know'), 
    ('/gallery', 200, '..........'),
    ('/login', 200,'Authentification'),
    ('/admin/', 200, 'Logout and Start page'),
    ('/admin', 308, 
        'You should be redirected automatically to target URL'),
    ('/fail', 404,'The requested URL was not found')])
def test_index(test_client, route, response_code, some_text):  
    assert test_client.get(route, 
            content_type='html/test').status_code == response_code  
    assert bytes(some_text, 'utf -8') in test_client.get(route,
            content_type='html/test').data




