import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    print("LALALALA", os.environ.get('DATABASE_URL'))
    UPLOAD_FOLDER = os.path.abspath("apps\\static\\uploads\\")
    DOWNLOAD_FOLDER = os.path.abspath("apps\\static\\downloads\\")
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
