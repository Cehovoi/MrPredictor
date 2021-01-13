import pytest
from random import shuffle, randint, choice
from scribble.imager import drawing
from scribble.validator import validator 
from tests import valid_num, invalid_num


def prep():
    l = []
    p = ['ASIAN', 'NIGER', 'WHITE']
    shuffle(p)
    for i in p:
        l.append((i, randint(7,50)))
    gender = choice(['BOY','GIRL'])
    return (l[:-1], l[-1], gender)


def test_drawin_len_img():
    d = drawing( *prep()).split(',')
    length = len(d[0])
    for i in d[:-1]: # field with name not always the same len
        assert len(i) == length

def test_drawing_speed():
    r = 10000
    for _ in range(r):
        drawing(*prep())
        assert 1==1

@pytest.mark.parametrize('name, num, expected_result',[
    ('',valid_num(), not None),
    ('a', valid_num(), not None ),
    ('bob', invalid_num(), not None),
    ('bob', valid_num(), None),
    ('123', valid_num(), not None),
    ('!@#$^&*', valid_num(), not None),
    ('string with many many letters and spaces and and', valid_num(), not None),
    ('Simple Name', valid_num(), None),
    ('Name', invalid_num(), not None)])                             
def test_validator(name, num, expected_result):
    '''The function returns tuple with not None value in second place
        if input data is invalid'''
    if expected_result: assert validator(name, num)[1]
    else: assert not(validator(name, num)[1])

    
