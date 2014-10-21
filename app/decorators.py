from threading import Thread
# login_decorator
from functools import wraps
from flask import session, redirect

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if "userId" in session and session["userId"] != 0:
      return f(*args, **kwargs)
    return redirect('/signin/')
  return decorated_function

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper
