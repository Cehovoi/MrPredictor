from flask import render_template, redirect, request, url_for, current_app
from flask_login import login_user, logout_user, current_user

from scribble import db
from .main import main
from scribble.models import Exhibit, Owner, Collector, filler, predictor
#from scribble.predictor import predictor
from scribble.validator import validator
from collections import OrderedDict
from itertools import zip_longest
'''
@main.route('/s')
def hello_world():
  return 'Hello PREDICTOR APP!'
'''
@main.route('/mysql')
def my_db():
  db.create_all()
  return "Create or not?"

@main.route('/oc_fill')
def oc_fill():
    filler()
    return 'Fill the Ocassion'

@main.route('/ex_fill',methods=['POST', 'GET'])
def ex_fill():
    if request.method == 'POST':
        from random import choice, randint
        from string import ascii_lowercase as low
        from string import ascii_uppercase as up
        latter = lambda: choice(low)
        amount = int(request.form['size'])
        name_length = 4
        ls = []
        for num in range(amount):
            s = choice(up)
            for _ in range(name_length):
                s += latter()
            if num%2 == 0:
                r = randint(-30, -7)
            else: r = randint(7, 30)

            ls.append((s, r))
        for name_size in ls:
            try:
                id = predictor(name_size[1], name_size[0])
            except Exception:
                return predictor(name_size[0],name_size[1]) or 'Dont add %s exemplars in %s step'% (amount, name_size[0], name_size[1])
        return redirect('/gallery')

    return render_template('you.html')


@main.route('/create_owner')
def owner():
    admin = Owner(username = 'Zhenya')
    admin.set_password='123'
    db.session.add(admin)
    db.session.commit()
    return 'ADD admin Zhenya'


@main.context_processor
def globs():
    counter = lambda: db.session.query(Exhibit).count()
    if current_user.is_authenticated:
        admin = current_user.username 
    else: admin = None
    return dict(count = counter(),
            admin = admin)


@main.route('/')
@main.route('/start')
def index():
    return render_template('start.html')


@main.route('/you', methods=['POST', 'GET'])
def you():
    if request.method == 'POST':
        name = request.form['name']
        size = request.form['size']

        size_and_comment = validator(name, size)
        
        if size_and_comment[1]: #check: size_and_comment[1] - field with error
            return render_template('error.html', 
                    comment=size_and_comment[1])
        try:
            id = predictor(size_and_comment[0], name)

            return redirect('/answer/%s' % id)
        except Exception:
            return 'Something went wrong with db'
    return render_template('you.html')


@main.route('/predictions')
def predictions():
    predictions = Exhibit.query.order_by(Exhibit.created_on.desc()).all()
    return render_template('predictions.html', predictions=predictions)


@main.route('/answer/<int:id>')
def answer(id):
    ans = Exhibit.query.get(id)
    epilogue = Collector.query.get(1).epilogue
    return render_template('answer.html', ans=ans, epilogue=epilogue)


@main.route('/gallery')
def gallery():
    predictions = sorted(Exhibit.query.all(), key = lambda x: x.length)
    boys, girls = [], []
    for person in predictions:
        if person.your_size > 0:
            boys.append(person)
        else:
            girls.append(person)
    ans = zip_longest(boys, girls)
    if predictions:
        bigest = predictions[-1].id
        smollest = predictions[0].id
    else: bigest, smollest = None, None
    return render_template('gallery.html', bigest=bigest, smollest=smollest, ans=ans)

@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        admin = db.session.query(Owner).filter(Owner.username == request.form['username']).first()
        if admin and admin.check_password(request.form['password']):
            login_user(admin)
            return redirect(url_for('admin.index'))
        else:
            return render_template('fail.html')
    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect('/start')