from flask import render_template, redirect, request, url_for, current_app
from flask_login import login_user, logout_user, current_user

from scribble import db
from .main import main
from scribble.models import Exhibit, Owner, Collector, filler, predictor
#from scribble.predictor import predictor
from scribble.validator import validator
from collections import OrderedDict

'''
@main.route('/s')
def hello_world():
  return 'Hello PREDICTOR APP!'
'''
@main.route('/mysql')
def my_db():
  db.create_all()
  return "Create or not?"

@main.route('/fill')
def fill():
    filler()
    return 'fill or not to fill'

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
    predictions = Exhibit.query.order_by(Exhibit.date.desc()).all()
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
        if person.size > 0:
            boys.append(person)
        else: girls.append(person)
    all_persons = OrderedDict()
    if len(girls) > len(boys):
        longest, shortest = iter(girls), iter(boys)
        ranger = range(len(girls))
        sex_1, sex_2 = 'girl', 'boy'
    else:
        longest, shortest = iter(boys), iter(girls)
        ranger = range(len(boys))
        sex_1, sex_2 = 'boy', 'girl'
    for _ in ranger:
        try:
            long = next(longest)
            short= next(shortest)
            l_1, l_2 = long.length - short.length, short.length - long.length

            all_persons.update({long: [sex_1, l_1]})
            all_persons.update({short: [sex_2, l_2]})
        except(StopIteration):
            if len(girls) - len(boys) == 0:
                break
            try:
                all_persons.update({long: [sex_1, 0]})
            except(StopIteration):
                break
    if predictions:
        bigest = predictions[-1].id
        smollest = predictions[0].id
    else: bigest, smollest = None, None
    return render_template('gallery.html', bigest = bigest, smollest = smollest, all_persons = all_persons)


@main.route('/admin')
def admin():
    return redirect(url_for('admin.index'))

@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':        
        user = db.session.query(Owner).filter(Owner.username == request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('admin.index'))
        else: 
            return render_template('fail.html')
    return render_template('login.html')


@main.route('/logout')
def logout():
    logout_user()
    return redirect('/start')
