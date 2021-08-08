from datetime import datetime
from flask_login import UserMixin, current_user, login_user, logout_user
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash

from scribble import db, admin, login

from random import choice, randint
from scribble.imager import drawing


def filler():
    comments = open('txt/comments.txt')
    keys = open('txt/keys.txt')
    prologue = open('txt/prologue.txt')
    epilogue = open('txt/epilogue.txt')
    while True:
        c = comments.readline()
        k = keys.readline()
        if c == '' or k == '':
            break
        try:
            ocassion = Occasion(comment=c, key=k)
            db.session.add(ocassion)
            db.session.commit()
        except Exception:
            return 'Error while adding  comments and keys to db in models.filler'
    if db.session.query(Collector).all() == []:
        try:
            db.session.add(Collector(prologue=prologue.read(), epilogue=epilogue.read()))
            db.session.commit()
        except Exception:
            return 'Error while adding collector to db in models.filler'


def predictor(your_size, name):
    if your_size < 0:
        sex = 'BOY';
        pronoun = 'he';
        measure = 'LONG'
    else:
        sex = 'GIRL';
        pronoun = 'she';
        measure = 'DEEP'

    value = abs(your_size)

    lovers = [('ASIAN', (randint(value // 3.2, value))),
              ('WHITE', (randint(value // 1.2, value // 0.8))),
              ('NIGER', (randint(value // 1.1, value // 0.7)))]

    person = choice(lovers)

    choice_race, choice_size = person[0], person[1]

    del (lovers[lovers.index(person)])

    if choice_size < value // 1.3:
        dimension = 'SMALL'
    elif choice_size > value // 0.7:
        dimension = 'BIG'
    else:
        dimension = 'MEDDLE'
    #important arg order in call collector_string
    prologue = collector_string(first_race=lovers[0][0], first_size=lovers[0][1],
                                second_race=lovers[1][0], second_size=lovers[1][1],
                                sex=sex, measure=measure, choice_race=choice_race,
                                dimension=dimension, your_size=your_size, pronoun=pronoun,
                                choice_size=choice_size)
    epilog = Collector.query.get(1).epilogue
    comment_num = comparative(your_size, choice_size, sex)
    picture = drawing(lovers, person, sex, value)#recive list of two values img and length
    exhibit = Exhibit(your_size=your_size, length=picture[1], name=name,
                      img=picture[0], prologue=prologue, occasion_id=comment_num)
    try:
        db.session.add(exhibit)
        db.session.commit()
    except Exception:
        return 'Somthing wrong with adding comlit exhibit to db'
    return exhibit.id


def collector_string(**kwargs):
    collector = Collector.query.get(1).prologue #hardcode id
    prologue = collector.format(**kwargs) #args = locals()
    return prologue


def comparative(your_size, choice_size, sex):
    your_size, choice_size = abs(your_size), abs(choice_size)
    counter = db.session.query(Occasion).count()
    for id in range(1, counter + 1):
        occasion = Occasion.query.get(id)
        if eval(occasion.key):
            return id


class Collector(db.Model):
    __tablename__ = 'collector'
    id = db.Column(db.Integer, primary_key=True)
    prologue = db.Column(db.Text, nullable=False)
    epilogue = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return '<Epilogue {} >'.format(self.epilogue)


class Occasion(db.Model):
    __teblename__ = 'occasions'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.Text, nullable=False)

    # exhibits = db.relationship('Exhibit', back_populates='occasion', lazy=True)
    def __repr__(self):
        return '<{} - Key {}  Occasion - {}>'.format(self.id, self.key, self.comment)


class Exhibit(db.Model):
    __tablename__ = 'exhibits'
    id = db.Column(db.Integer, primary_key=True)
    your_size = db.Column(db.Integer)
    length = db.Column(db.Integer)
    name = db.Column(db.String(64), nullable=False)
    img = db.Column(db.Text, nullable=False)
    prologue = db.Column(db.Text, nullable=False)
    occasion_id = db.Column(db.Integer, db.ForeignKey('occasion.id'))
    occasion = db.relationship('Occasion')  # ('Occasion', back_populates="exhibits")

    created_on = db.Column(db.DateTime, default=datetime.utcnow)

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


admin.add_view(MyModelView(Collector, db.session))
admin.add_view(MyModelView(Occasion, db.session))
admin.add_view(MyModelView(Exhibit, db.session))
admin.add_view(MyModelView(Owner, db.session))


