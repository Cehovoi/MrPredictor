from datetime import datetime
from flask_login import UserMixin, current_user, login_user, logout_user
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash

from scribble import db, admin, login

class Occasions(db.Model):
    __teblename__ = 'occasions'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.Integer)
    comment = db.Column(db.Text, nullable=False)
    def filler(self):
        if db.session.querry(Ocassions).all() == []
            pass
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

admin.add_view(MyModelView(Occasions, db.session))
admin.add_view(MyModelView(Exhibit, db.session))
admin.add_view(MyModelView(Owner, db.session))


