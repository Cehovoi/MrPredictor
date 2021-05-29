from string import ascii_lowercase as low
from string import ascii_uppercase as up
from tests import valid_num
from random import choice
from scribble.predictor import predictor
from scribble.models import Exhibit
from scribble import db


ls = []
name_length = 4
latter = lambda: choice(low)
score = lambda: db.session.query(Exhibit).count()


def fill(amount):
    for _ in range(amount):
        s = choice(up)
        for _ in range(name_length):
            s += latter() 
        ls.append((s, valid_num()))
    for i in ls:
        prediction = predictor(i[1])
        e = Exhibit(name = i[0], predictions=prediction[0], img=prediction[1])
        db.session.add(e)
        db.session.commit()
    return printer(amount, 'increased')


def eraser(amount, direction='start'):
    if direction == 'start':
        exemplars = list(db.session.query(Exhibit).slice(0, amount))
    else:
        exemplars = list(db.session.query(Exhibit).slice(score()-amount, score()))

    for exemplar in exemplars:
        db.session.delete(exemplar)
        db.session.commit()
    return printer(amount, 'decreased')

def devastator():
    Exhibit.query.delete()
    db.session.commit()
    return 'The current base erase'


def printer(amount, state):
    name_db = str(db)
    for i in range(len(name_db)-1, 0, -1):
        if name_db[i] == '/':
            answer = name_db[i+1:-4]
            break
    return 'The %s database has %s by %s exemplars,%s records in total' % (answer, state, amount, score())