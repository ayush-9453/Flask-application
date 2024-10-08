from flask import Blueprint, render_template,request, flash ,url_for,redirect
from .models import User
from werkzeug.security import generate_password_hash , check_password_hash
from . import db   
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login' ,methods=['GET','POST'])
def login():
    if request.method =='POST':
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email = email).first()
            if user:
                if check_password_hash(user.password,password):
                    flash('Logged In Successful.',category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home')) 
                else:
                    flash("Incorrect password,try again.",category='error')
            else:
                flash("User doesn't exists.",category='error')

    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@auth.route('/register',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()

        if user:
            flash('Email already exists.' , category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif first_name is None or len(first_name) < 2:
            flash('Username must be greater than 2 characters.', category='error')
        elif len(password1) < 7:
            flash('Password should at least be 8 characters', category='error')
        elif password1 != password2:
            flash("Password doesn't match.", category='error')
        else:
            new_user = User(email = email, first_name= first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Success Account created',category='success')
            return redirect(url_for('views.index'))
        
    return render_template('register.html',user=current_user)