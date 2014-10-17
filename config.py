###############################################
# There are only two config - dev & prod
# if app is running on local laptop, configure env as dev
###############################################

# TODO: see how security/csrf protection works

#for generating uui as secret key
import uuid
import os
import socket

basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object):
	SECRET_KEY = str(uuid.uuid4())
	if '.local' in socket.gethostname():
		SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'thlt.db')
		DEBUG = True
		ENVIRONMENT = 'dev'
	else:
		try:
			from prod_settings import PRODDB_URI
			# currently only the below line
			# AZUREDB_URI = "mysql://...."
			SQLALCHEMY_DATABASE_URI = PRODDB_URI
			DEBUG = False
			ENVIRONMENT = 'prod'
		except ImportError as e:
			# TODO: this should log to loggly
			print "Error while connecting to production env: %s" % e
