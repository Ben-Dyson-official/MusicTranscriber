from dotenv import load_dotenv
load_dotenv()

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #variables below set up the secret key and database
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PIECES_PER_PAGE = 5

    #variables below set up the mail server
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 's00136@reading-school.co.uk'
    MAIL_PASSWORD = 'Germany88'
    ADMINS = ['s00136@reading-school.co.uk']

