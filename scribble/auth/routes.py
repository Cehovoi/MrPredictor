from flask import render_template
from . import auth

@auth.route('/login_usr')
def login_usr()
    return render_template('auth/login_usr.html')