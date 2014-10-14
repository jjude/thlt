"""
a single entry-point that resolves the import dependencies.
ref: http://charlesleifer.com/blog/structuring-flask-apps-a-how-to-for-those-coming-from-django/
run using main.py or main.app
"""
from app import app

from app.auth import *
from app.models import *
from app.views import *

# to run cli commands (esp runserver)
from flask.ext.script import Manager

manager = Manager(app)

# start the server with the 'run()' method (otherwise it is app.run())
# you can pass an ip (0.0.0.0) so that the app can be accessed by other devices
# in the same network
if __name__ == '__main__':
    auth.User.create_table(fail_silently=True)
    Site.create_table(fail_silently=True)
    Entry.create_table(fail_silently=True)
    manager.run()
