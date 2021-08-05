from datetime import datetime
from flask_login import UserMixin, current_user, login_user, logout_user
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash

from scribble import db, admin, login

from random import choice, randint
from scribble.imager import drawing

def predictor(organ):
    if organ < 0:
        gender = 'BOY';
        pronoun = 'he';
        measure = 'LONG'
    else:
        gender = 'GIRL';
        pronoun = 'she';
        measure = 'DEEP'

    value = abs(organ)

    lovers = [('ASIAN', (randint(value // 3.2, value))),
              ('WHITE', (randint(value // 1.2, value // 0.8))),
              ('NIGER', (randint(value // 1.1, value // 0.7)))]

    person = choice(lovers)

    race, size = person[0], person[1]

    del (lovers[lovers.index(person)])

    if size < value // 1.3:
        dimension = 'SMALL'
    elif size > value // 0.7:
        dimension = 'BIG'
    else:
        dimension = 'MEDDLE'
    return (lovers[0], lovers[1], gender, measure, race, dimension,
        organ, pronoun, size, value),  drawing(lovers, person, gender, value)
#predictions(size, value, gender))

def filler():
    comments = open('comments.txt')
    keys = open('keys.txt')
    epilogue = open('epilogue.txt')
    while True:
        c = comments.readline()
        k = keys.readline()
        if c == '' or k == '':
            break
        try:
            ocassion  = Occasion(comment = c, key = k)
            db.session.add(ocassion)
            db.session.commit()
        except Exception:
            print('Error while adding  comments and keys to db in models.filler')
    if db.session.query(Epilogue).all() == []:
        try:
            db.session.add(Epilogue(epilogue = epilogue.read()))
            db.session.commit()
        except Exception:
            print('Error while adding epilogue to db in models.filler')

def pointer(size, value, m):
    counter = db.session.query(Occasion).count()
    for id in range(counter + 1):
        occasion = Occasion.query.get(id)
        if eval(occasion.key):
            exhibit = Exhibit(size=size, length=predictions[1][1], name=name, predictions=predictions[0],
                              img=predictions[1][0])



class Epilogue(db.Model):
    __tablename__ = 'epilogue'
    id = db.Column(db.Integer, primary_key=True)
    epilogue = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Epilogue {} >'.format(self.epilogue)

class Occasion(db.Model):
    __teblename__ = 'occasions'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Occasion {} in {} place>'.format(self.comment, self.id)

class Exhibit(db.Model):
    __tablename__ = 'exhibits'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer)
    length = db.Column(db.Integer)
    name = db.Column(db.String(64), nullable=False)
    predictions = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Exhibit {} in {} place>'.format(self.name, self.id)




class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),nullable=False, unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    size = db.Column(db.Integer)
    pict = db.Column(db.String(512), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(512), nullable=False)
    exhibit_id = db.Column(db.Integer, db.ForeignKey('exhibits.id'))

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow,  onupdate=datetime.utcnow)

    @property
    def set_password(self):
        raise AttributeError('set_password is not readable attribute')

    @set_password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


class Owner(db.Model, UserMixin):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(512), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow,  onupdate=datetime.utcnow)

    @property
    def set_password(self):
        raise AttributeError('set_password is not readable attribute')

    @set_password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


'''
@login.user_loader
def load_user(id):
    return db.session.query(Owner).get(id) # Owner.query.get(id)
'''

@login.user_loader
def load_user(id):
    return db.session.query(User).get(id) # Owner.query.get(id

class MyModelView(ModelView):
    can_delete = True
    def is_accessible(self):
        return True #current_user.is_authenticated

admin.add_view(MyModelView(Occasion, db.session))
admin.add_view(MyModelView(Epilogue, db.session))
admin.add_view(MyModelView(Exhibit, db.session))
admin.add_view(MyModelView(Owner, db.session))


