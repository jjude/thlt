from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

from config import DefaultConfig

# blueprints
from api import api_v1
from frontend import frontend

from extensions import db

"""
only create_app will be imported when someone does,

import app

created as the last statement

"""
__all__ = ['app']

def create_app(config=DefaultConfig):
  # initial setup
  app = Flask(__name__)
  configure_app(app, config)
  register_blueprints(app)
  configure_extensions(app)
  configure_logging(app)
  configure_template_filters(app)
  
  return app

def configure_app(app, config=DefaultConfig):
  app.config.from_object(config)
  # toolbar = DebugToolbarExtension(app)
  # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

def register_blueprints(app):
  app.register_blueprint(api_v1)
  app.register_blueprint(frontend)

def configure_extensions(app):
  # flask-sqlalchemy
  db.init_app(app)
  with app.app_context():
    from base import models
    db.create_all()
  
  # bootstrap
  Bootstrap(app)


def configure_template_filters(app):
  # jinja2 filter
  @app.template_filter('datefilter')
  def _jinja2_filter_datetime(date, fmt=None):
      from dateutil.parser import parse
      date = parse(date)
      native = date.replace(tzinfo=None)
      format='%b %d, %Y %I:%M:%S %p'
      return native.strftime(format) 

def configure_logging(app):  
  # FUTURE: this should be loggly later
  import logging
  logging.basicConfig()
  from logging.handlers import RotatingFileHandler
  file_handler = RotatingFileHandler('thltapp.log', 'a', 1 * 1024 * 1024, 10)
  file_handler.setLevel(logging.INFO)
  file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  app.logger.addHandler(file_handler)
  app.logger.setLevel(logging.INFO)
  app.logger.info('thlt app started')
      
# app = create_app()