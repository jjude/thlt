# import the Flask class from the flask module
from flask import Flask

# flask-peewee database
from flask_peewee.db import Database

# initial setup
app = Flask(__name__)
app.config.from_object('config.Configuration')
db = Database(app)
