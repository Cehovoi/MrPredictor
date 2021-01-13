from string import ascii_lowercase as low
from string import ascii_uppercase as up
from tests import valid_num
from random import choice
from scribble.predictor import predictor
from scribble.models import Exhibit
from scribble import db


ls = []
name_length = 4
ranger = 50
latter = lambda: choice(low)

def fill():
    for _ in range(ranger):
        s = choice(up)
        for _ in range(name_length):
            s += latter() 
        ls.append((s, valid_num()))
    for i in ls:
        prediction = predictor(i[1])
        e = Exhibit(name = i[0], predictions=prediction[0], img=prediction[1])
        db.session.add(e)
        db.session.commit()

    name_db = str(db)
    for i in range(len(name_db)-1, 0, -1):
        if name_db[i] == '/':
            answer = name_db[i+1:-4]
            break
            
    return 'The %s database has increased by %s exepmlars' % (answer, len(ls))

def devastator():
    Exhibit.query.delete()
    db.session.commit()
    return 'The current base erase'

