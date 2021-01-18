import pytest
from scribble import create_app

@pytest.mark.parametrize('route, response_code, some_text',[
    ('/', 200, 'Do you want to know'), 
    ('/gallery', 200, '..........'),
    ('/login', 200,'Authentification'),
    ('/admin/', 200, 'Logout and Start page'),
    ('/admin', 308, 
        'You should be redirected automatically to target URL'),
    ('/fail', 404,'The requested URL was not found')])
def test_index(route, response_code, some_text):  
    tester = create_app('config.DevelopmentConfig').test_client()
    assert tester.get(route, 
            content_type='html/test').status_code == response_code  
    assert bytes(some_text, 'utf -8') in tester.get(route,
            content_type='html/test').data
