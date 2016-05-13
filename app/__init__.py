from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
app = Flask(__name__)
uri = 'mysql://admin:admin@localhost/redditreader'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
db = SQLAlchemy(app)
from app import models, redditreader, dbProc, redditsearcher