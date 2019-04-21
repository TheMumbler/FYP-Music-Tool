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
from flask_uploads import UploadSet, AUDIO

audio = UploadSet("song", AUDIO)


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
    # user = {'username': 'Paddy'}
    if request.method == 'POST':
        f = request.files['file']
        # wav = io.BytesIO(f.read())
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        # sr, song = read(wav)
        # print(sr)
        # length = (len(song)/sr)
        # print(length)
        print(current_user.username)
        # piano.piano_ver1(song, f.filename[:-4], "apps/static/" + current_user.username, 60, sr)
        print('file uploaded successfully')
        return redirect(url_for('results', user=current_user.username, filename=f.filename))
        # "results.html",
        #                        user=current_user.username,
        #                        length=length,
        #                        song=True,
        #                        data=list(song),
        #                        fname=f.filename[:-4] + ".mid")
    form = AddFile()
    return render_template("tool.html", user=current_user.username, form=form)


@app.route('/<user>/<filename>', methods=['GET', 'POST'])
def results(user, filename):
    location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(filename, "DSADSAD")
    sr, song = read(os.path.join(location))
    path = piano.piano_ver1(song, filename[:-4], "apps/static/" + current_user.username, 60, sr)
    print(path)
    return render_template("results.html", user=user, length=(len(song)/sr), wavfname=filename, fname=filename[:-4] + ".mid", location=location)


@app.route('/<user>/<path:filename>', methods=['GET', 'POST'])
def download(user, filename):
    uploads = os.path.join(current_app.root_path, "static", user)
    print(uploads)
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/user/<username>')
def user(user):
    return render_template("user.html", user=user)
# @app.route('/working')
# def uploaded():
#     user = {'username': 'Paddy'}
#     return render_template("results.html", user=user)
