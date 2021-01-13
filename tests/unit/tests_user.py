import pytest
from scribble.models import User


@pytest.fixture(scope='module')
def new_user():
    u1 = User(username = 'Polya')
    User.set_password(u1, '123')
    return u1

def test_new_user(new_user):
    assert new_user.username == 'Polya'
    assert len(new_user.password_hash) == 94
    assert new_user.check_password('123')
    assert new_user.is_authenticated
