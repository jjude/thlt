from app import app

# to run cli commands (esp runserver)
from flask.ext.script import Manager

manager = Manager(app)

# start the server with the 'run()' method (otherwise it is app.run())
# you can pass an ip (0.0.0.0) so that the app can be accessed by other devices
# in the same network
if __name__ == '__main__':
  manager.run()
