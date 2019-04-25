from . import app
from flask import render_template, url_for, request, redirect, flash, send_from_directory, current_app
from flask_login import current_user, login_user, logout_user, login_required
from .models import User
from .forms import LoginForm, RegistrationForm, AddFile
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from . import db
import io
import os
from src import piano

from src.song.read import read


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/tool', methods=['GET', 'POST'])
@login_required
def tool():
    if request.method == 'POST':
        f = request.files['file']
        name = secure_filename(f.filename)
        user = current_user.username
        path = os.path.join(app.config['UPLOAD_FOLDER'], user)
        os.makedirs(path, exist_ok=True)
        # os.makedirs(path, exist_ok=True)
        print(path)
        if len(os.listdir(path)) > 0:
            print("FASFEGEASDGDSGDS WAAJA")
            todel = os.path.join(path, os.listdir(path)[0])
            os.remove(todel)
        f.save(os.path.join(path, name))
        # f.save(name)
        print(current_user.username)
        print('file uploaded successfully')
        return redirect(url_for('results', user=user))
                              # filename=f.filename)
    form = AddFile()
    return render_template("tool.html", user=current_user.username, form=form)


@app.route('/<user>/results', methods=['GET', 'POST'])
def results(user):
    userpath = os.path.join(app.config['UPLOAD_FOLDER'], user)
    currfile = os.listdir(userpath)[0]
    # sr, song = read(os.path.join(location))
    return render_template("results.html", wavpath=currfile)


@app.route('/<user>/<path:filename>', methods=['GET', 'POST'])
def download(user, filename):
    uploads = os.path.join(app.config['UPLOAD_FOLDER'], user)
    print(uploads, "UPLOADS")
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/user/<username>')
def user(user):
    return render_template("user.html", user=user)
# @app.route('/working')
# def uploaded():
#     user = {'username': 'Paddy'}
#     return render_template("results.html", user=user)
