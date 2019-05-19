from . import app
from flask import render_template, url_for, request, redirect, flash, send_from_directory, session, stream_with_context, request, Response
from flask_login import current_user, login_user, logout_user, login_required
from .models import User
from .forms import LoginForm, RegistrationForm, AddFile, YouTubeLink
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from . import db
import time
import io
import os
from src import piano
from src.song import beat
from librosa.beat import tempo
from src.song import structure
from src.song import read
from src.song import drum
from src.song import utils


tools = {"piano": piano.piano,
         "drum": drum.drum_tool}


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


@app.route('/tool/<type>', methods=['GET', 'POST'])
@login_required
def tool(type):
    form = AddFile()
    form2 = YouTubeLink()
    session["type"] = type
    if request.method == "POST":
        user = current_user.username
        path = os.path.join(app.config['UPLOAD_FOLDER'], user)
        os.makedirs(path, exist_ok=True)
        if len(os.listdir(path)) > 0:
            todel = os.path.join(path, os.listdir(path)[0])
            os.remove(todel)

        if form.validate_on_submit():
            f = request.files['file']
            name = secure_filename(f.filename)
            f.save(os.path.join(path, name))
            session["segmented"] = form.segmented.data
            print('file uploaded successfully for user {}'.format(user))
            return redirect(url_for('results', user=user))

        elif form2.validate_on_submit():
            link = request.form.get('link')
            session["segmented"] = form2.segmented.data
            read.get_youtube(link, path)
            return redirect(url_for('results', user=user))

    return render_template("tool.html", type=type.title(), user=current_user.username, fileform=form, youtubeform=form2)


# @app.route('/tool', methods=['GET', 'POST'])
# @login_required
# def drumtool():
#     pass


@app.route('/<user>/results', methods=['GET', 'POST'])
@login_required
def results(user):
    userpath = os.path.join(app.config['UPLOAD_FOLDER'], user)
    currfile = os.listdir(userpath)[0]
    fileloc = os.path.join(userpath, currfile)
    downloads = os.path.join(app.config['DOWNLOAD_FOLDER'], user)
    func = tools[session["type"]]
    os.makedirs(downloads, exist_ok=True)
    if len(os.listdir(downloads)) > 0:
        files = os.listdir(downloads)
        for file in files:
            todel = os.path.join(downloads, file)
            os.remove(todel)

    func(fileloc, name=session["type"], user=downloads, sections=session["segmented"])
    utils.zipFiles(downloads, session["type"])
    # session['bpm'] = 123213
    # def generate():
    session['bpm'] = str(beat.get_bpm(fileloc))[:5]

    #     yield render_template("results.html", wavpath=currfile)
    #     time.sleep(1)
    #     yield "ujj"
    #     time.sleep(1)
    #     yield '!'
    # sr, song = read(os.path.join(location))
    if session.get("segmented", None):
        session.pop("segmented")
    if session.get("type", None):
        session.pop("type")
    return render_template("results.html", wavpath=currfile)


@app.route('/<user>/<path:filename>', methods=['GET', 'POST'])
def download(user, filename):
    uploads = os.path.join(app.config['UPLOAD_FOLDER'], user)
    print(uploads, "UPLOADS")
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/<user>/<path:filename>', methods=['GET', 'POST'])
def downloadMidi(user, filename):
    uploads = os.path.join(app.config['DOWNLOAD_FOLDER'], user)
    print(uploads, "DOWNLOADS")
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/user/<username>')
def user(user):
    return render_template("user.html", user=user)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        time.sleep(1)
        yield "ujj"
        time.sleep(1)
        yield '!'
    return Response(stream_with_context(generate()))
