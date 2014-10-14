# TODO: see how security/csrf protection works
# TODO: separate dev & prod configs
# TODO: postgresql for prod

#for generating uui as secret key
import uuid

class Configuration(object):
	DATABASE = {
		'name': 'thlt.db',
		'engine': 'peewee.SqliteDatabase',
		'check_same_thread': False,
	}
	DEBUG = True
	ENVIRONMENT = 'dev'
	SECRET_KEY = str(uuid.uuid4())
