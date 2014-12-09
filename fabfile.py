from fabric.api import run, cd, env, lcd, put, local, abort, settings
from fabric.contrib.project import rsync_project
from fabric import utils
from fabric.decorators import hosts
import os
RSYNC_EXCLUDE = ('.DS_Store', '*.pyc', '*.db', '.git', '*.log', '.gitignore', 'local_settings.py', 'fabfile.py', 'README.md', 'run_dev.sh', 'requirements.txt', 'lib')
env.localDir = os.path.abspath(os.path.dirname(__file__)) + '/'

def d():
    """
    debug
    """
    activate_this = '../bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
    local('python manage.py runserver --host 0.0.0.0')


def t():
    """
    testing
    """
    activate_this = '../bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
    local('python -m unittest discover -v')
    
    
def clean():
    """
    clean .pyc files
    """
    local("find . -name '*.pyc' -delete")