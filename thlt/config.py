###############################################
# There are only two config - dev & prod
# if app is running on local laptop, configure env as dev
###############################################

#for generating uui as secret key
import uuid
import os
import socket


class BaseConfig(object):
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))
  # secret key has to be a static value; dont generate it dynamically
  # like os.urandom or uuid.uuid4()
  # if you set so, sessions will not be persisted
  # ref: http://stackoverflow.com/a/18709356/770719
  SECRET_KEY = '7ac8eb31-e96e-43d8-b587-5c7461e185c2'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'thlt.db')
  DEBUG = True
  ENVIRONMENT = 'dev'
  TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'default_template'))
  

class DefaultConfig(BaseConfig):
  if '.local' not in socket.gethostname():
    try:
      from prod_settings import PROD_DB_URI, PROD_SECRET_KEY
      SECRET_KEY = PROD_SECRET_KEY
      SQLALCHEMY_DATABASE_URI = PROD_DB_URI
      DEBUG = False
      ENVIRONMENT = 'prod'
    except ImportError as e:
      # FUTURE: this should log to loggly
      print "Error while connecting to production env: %s" % e

class TestConfig(BaseConfig):
  TESTING = True
  ENVIRONMENT = 'test'
  WTF_CSRF_ENABLED = False
  PRESERVE_CONTEXT_ON_EXCEPTION = False
  # create test.db in base_dir of the dev environment
  # since test_folders won't be created until tests are runs
  # but db will have to be created prior to running any tests
  BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_folders'))
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'test.db')