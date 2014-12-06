#############
#Ref for sessions: http://stackoverflow.com/a/11785722/770719
#############

from flask import Blueprint, current_app
from flask import Flask, render_template, request, redirect, url_for, flash, g

# decorators
from functools import wraps

# sessions
from flask import session
from datetime import timedelta

from thlt.base import *
import json

frontend = Blueprint('frontend', __name__)

################################################################
# Utility Methods
################################################################

def auth_user(token):
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(minutes=15)
    session['loggedIn'] = True
    session['token'] = token
    flash("You are logged in")
    return

# error handlers
# for blueprints you can mention only 404
@frontend.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# decorator
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if "token" in session and session["token"] != 0:
      return f(*args, **kwargs)
    return redirect('/signin/')
  return decorated_function

################################################################
# Main Methods
################################################################

@frontend.route('/')
def index():
  #destroy session when brower closed
  session.permanent = True
  g.env = current_app.config['ENVIRONMENT']
  if 'loggedIn' in session and session['loggedIn']:
    return redirect('/mysites/')
  else:
    return redirect('/signin/')

@frontend.route('/signout/')
def signout():
  session.clear()
  return redirect("/")