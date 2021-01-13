import pytest
from scribble.models import Exhibit
from scribble.predictor import predictor
from scribble import db
from tests import valid_num


@pytest.fixture(scope='module')
def new_exhibit():
    """If you want to see picture don\'t forget use pytest -s"""
    num = valid_num()
    predictions = predictor(num) 
    e1 = Exhibit(name = 'Sam', 
            predictions = predictions[0], img =predictions[1])
    picture = predictions[1].split(',')
    print('\n')
    for i in picture:
        print(i)
    return e1

def test_new_exhibit(new_exhibit):
    assert new_exhibit.name == 'Sam'
    assert new_exhibit.predictions.__class__ == str
    assert len(new_exhibit.img) > 200

