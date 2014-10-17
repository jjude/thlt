##########################################
# Deploy to webfaction
##########################################

# execute: fab prod deploy

# Steps
# =====
# 1. pull sources from git (deploy only from vcs)
# 2. add un-checked files like prodsettings
# 3. install/update dependencies
# 4. modify db, if required
# 5. restart apache

# Assumptions & pre-requisites
# ============================
# git is installed locally
# all sources are checked in git
# all tests are already executed & the code is ready to deploy

# Notes
# =====
# DO NOT STORE USERNAMES OR PASSWORDS IN THIS FILE. INSTEAD
# CREATE fabfile.yaml AND USE THAT FOR STORING SENSITIVE DATA

# fabric uses ssh & I've already created SSH key on the local machine
# SSH key is the prefered way to connect;
# if not use .yaml file to specify passwords

# default rsync options:
# -pthrvz
# -p preserve permissions
# -t preserve times
# -h output numbers in a human-readable format
# -r recurse into directories
# -v increase verbosity
# -z compress file data during the transfer

# ref: http://ewong.me/automate-deployment-of-flask-application-using-fabric/
# ref: https://bitbucket.org/copelco/caktus-deployment/src/tip/example-django-project/caktus_website/fabfile.py
# ref: http://aaronpresley.com/deploying-a-flask-project-on-webfaction/
# ref: https://www.digitalocean.com/community/tutorials/how-to-use-fabric-to-automate-administration-tasks-and-deployments

# TODO: install virtualenv on webfaction & install using setup tools
# TODO: deploy only from master branch
# TODO: fail if there is no prod_settings.py

from fabric.api import run, cd, env, lcd, put, local, abort, settings
from fabric.contrib.project import rsync_project
from fabric import utils
from fabric.decorators import hosts

localAppDir = '/Users/cephire/code/thltpy/thlt'

RSYNC_EXCLUDE = (
    '.DS_Store',
    '*.pyc',
    '*.db',
    '.git',
    '.gitignore',
    'local_settings.py',
    'fabfile.py',
    'README.md',
    'siteFiles',
    'userFiles',
    'run_dev.sh',
    'requirements.txt',
    'lib',
)

# the user for remote commands
env.user = 'id804097'
# server(s) where commands are executed
env.hosts = ['id804097.webfactional.com']
env.remoteVEnvRoot = '/home/id804097/webapps/thltflask'
env.remoteRoot = '/home/id804097/webapps/thltflask/thltapp'
# end with trailing slash so that it is a dir-to-dir sync
# without /, thlt directory will be created in remoteRoot
env.localDir = '/Users/cephire/code/thltpy/thlt/'


def deploy():
  print_header('Staring to deploy')
  with cd(env.remoteVEnvRoot):
    print_info ('Deploying in ...%s' % run('pwd'))
    #activate corresponding virtualenv and install required modules
    run('source thltenv/bin/activate')
    put('requirements.txt', 'requirements.txt')
    pipinstall = run('pip install -r requirements.txt')
    if pipinstall.succeeded:
      # by default, rsync will create a directory by name of local directory
      # in the remote root
      rsync_project(
        env.remoteRoot,
        env.localDir,
        exclude=RSYNC_EXCLUDE,
        delete=True,
      )
      run('apache2/bin/restart')
      print_success('deployment completed')
    else:
      print_error('pip installed failed')
      abort()

# ------------------- FANCY PRINTING -------------------------
# copied from jamie curlie
HEADER = '\033[42;30m'
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def print_header(msg):
    print HEADER + ' ' + msg + ' ' + ENDC

def print_error(msg):
    print RED + msg + ENDC

def print_info(msg):
    print BLUE + msg + ENDC

def print_success(msg):
    print GREEN + msg + ENDC
