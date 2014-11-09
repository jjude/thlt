###############################################
# There are only two config - dev & prod
# if app is running on local laptop, configure env as dev
###############################################

# TODO: see how security/csrf protection works

# for generating uui as secret key
import uuid
import os
import socket

basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object):
  # secret key has to be a static value; dont generate it dynamically
  # like os.urandom or uuid.uuid4()
  # if you set so, sessions will not be persisted
  # ref: http://stackoverflow.com/a/18709356/770719

    if '.local' in socket.gethostname():
        SECRET_KEY = '7ac8eb31-e96e-43d8-b587-5c7461e185c2'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
                'thlt.db')
        DEBUG = True
        ENVIRONMENT = 'dev'
    else:
        try:
            from prod_settings import PRODDB_URI, PRODSECRET_KEY
            SECRET_KEY = PRODSECRET_KEY
            SQLALCHEMY_DATABASE_URI = PRODDB_URI

            DEBUG = False
            ENVIRONMENT = 'prod'
        except ImportError, e:

            # TODO: this should log to loggly
            print 'Error while connecting to production env: %s' % e