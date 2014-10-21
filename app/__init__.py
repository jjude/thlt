# import the Flask class from the flask module
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# initial setup
app = Flask(__name__)
app.config.from_object('config.Configuration')
db = SQLAlchemy(app)

import views, models
db.create_all()

# this should be loggly later
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('thltapp.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('thlt startup')
