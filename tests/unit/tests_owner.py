import pytest
from scribble.models import Owner


@pytest.fixture(scope='module')
def new_owner():
    u1 = Owner(username = 'Polya', set_password = '123')
    return u1

def test_new_owner(new_owner):
    with pytest.raises(AttributeError): new_owner.set_password
    assert new_owner.username == 'Polya'
    assert len(new_owner.password_hash) == 94
    assert new_owner.check_password('123')
    assert not(new_owner.check_password('321'))
    assert new_owner.is_authenticated
