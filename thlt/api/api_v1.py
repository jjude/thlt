from flask import Blueprint, current_app, jsonify, json
import os

from ..base import *

# TODO: while deploying to prod, url_prefix has to be of subdomain
api = Blueprint('api', __name__, url_prefix='/api/v1')

###################################################
# Utilities
###################################################
# APIs will return response strings from base.py
# if there is a need to construct response from API, this method will be invoked
# returns JSONified result
def res_str(status_code, resp_code, message, results=None):
  """
  return string contains (read README.md for details)
  status: HTTP Status Codes (uses only subset of all codes)
  code: internal success & error codes. each operation should be tagged with 
  		a code, for easy debugging
  message: detailed message for display to user or debugging
  results: optional python list  
  """
  if results:
    ret_str = jsonify({'status': status_code, 'code': resp_code, 'message': message, 'results': results})
  else:
    ret_str = jsonify({'status': status_code, 'code': resp_code, 'message': message})
  return ret_str

# only 404 error handler
@api.app_errorhandler(404)
def page_not_found(error):
    return res_str(404, 4001, 'Check Your URL'), 404

###################################################
# Main methods
###################################################
@api.route('/')
def index():
  """
  shouldn't be called by any client; if called return a simple message
  """
  return res_str(200, 2001, 'hello from thlt')

@api.route('/signup', methods=['POST'])
def api_signup():
  """
  expects request data to be in json
  Content-type: application/json
  should be mentioned while invoking
  
  request.headers & request.json contain details
  """
  
  email = password = ''
  if request.json:
    email = request.json['email'] if 'email' in request.json else ''
    password = request.json['password'] if 'password' in request.json else ''
    
  ret_str = create_user(email, password)
  return jsonify(ret_str)
  
@api.route('/signin', methods=['POST'])
def api_signin():
  """
  expects request data to be in json
  Content-type: application/json
  should be mentioned while invoking
  
  request.headers & request.json contain details
  """
  email = request.json['email'] if 'email' in request.json else ''
  password = request.json['password'] if 'password' in request.json else ''
  ret_str = get_token(email, password)
  return jsonify(ret_str)
  
@api.route('/sites', methods=['POST'])
def api_create_site():
  """
  expects request data in json
  content-type: application/json  
  """
  token = request.json['token'] if 'token' in request.json else ''
  site_data = request.json['data'] if 'data' in request.json else ''
  ret_str = create_site(token, site_data)
  return jsonify(ret_str)

@api.route('/sites', methods=['PUT'])
def api_update_site():
  """
  expects request data in json
  content-type: application/json  
  """
  token = request.json['token'] if 'token' in request.json else ''
  site_id = request.args.get('siteId')
  site_data = request.json['data'] if 'data' in request.json else ''
  ret_str = update_site(token, site_id, site_data)
  return jsonify(ret_str)


@api.route('/sites')
def api_get_site():
  """
  expects request data in json
  content-type: application/json  
  """
  token = request.json['token'] if 'token' in request.json else ''  
  ret_str = get_sites_for_user(token)
  return jsonify(ret_str)

@api.route('/entries')
def api_get_entries_for_site():
  """
  expects request data in json
  content-type: application/json  
  """
  siteId = request.args.get('siteId')
  token = request.json['token'] if 'token' in request.json else ''  
  ret_str = get_entries_for_site(token, siteId)
  return jsonify(ret_str)

@api.route('/entries', methods=['POST'])
def api_create_entry():
  """
  expects request data in json
  content-type: application/json  
  """
  
  token = request.json['token'] if 'token' in request.json else ''
  entries_data = request.json['data'] if 'data' in request.json else ''
  ret_str = create_entry(token, entries_data)
  return jsonify(ret_str)