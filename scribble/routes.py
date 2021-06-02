from flask import render_template, redirect, request, url_for, current_app
from flask_login import login_user, logout_user, current_user

from scribble import db
from .main import main
from scribble.models import Exhibit, Owner
from scribble.predictor import predictor
from scribble.validator import validator


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

        predictions = predictor(size_and_comment[0]) # send name and size to predictor recive predictions and image
        exhibit = Exhibit(size=size, name=name, predictions=predictions[0], img =predictions[1])
        try:
            db.session.add(exhibit)
            db.session.commit()
            id = exhibit.id
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
    return render_template('answer.html', ans=ans)


@main.route('/gallery')
def gallery():
    predictions = sorted(Exhibit.query.all(), key = lambda x: len(x.img))
    boys, girls = [], []
    for person in predictions:
        if person.size > 0:
            boys.append(person)
        else: girls.append(person)
    diff = len(boys) - len(girls)
    remainder_b, remainder_g = [], []
    if diff > 0:
        boys, remainder_b = boys[:-diff], boys[-diff:]
    if diff < 0:
        girls, remainder_g = girls[:diff], girls[diff:]
    all =[]
    for boy, girl in zip(boys, girls):
        all.append(girl)
        all.append(boy)
    print('remainder_b---',remainder_b,'\n','remainder_g---', remainder_g)
    if predictions:
        bigest = predictions[-1].id
        smollest = predictions[0].id
    else: bigest, smollest = None, None
    return render_template('gallery.html', predictions = all,
                            bigest = bigest, smollest = smollest, remainder_b = remainder_b,remainder_g = remainder_g)


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


