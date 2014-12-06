###################################################
# Base Methods for Frontend & other APIs
# Session mgmt is not handled here
# Session mgmt should be handled in respective modules
###################################################

from flask import current_app, jsonify, request
from sqlalchemy.exc import IntegrityError


# for token based authentication
# use serializer to generate & verify tokens
# ref: http://blog.miguelgrinberg.com/post/restful-authentication-with-flask
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from thlt.extensions import db
from models import User, Site, Entry

# other python ops
from shutil import copytree, rmtree, make_archive
import os
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from hashlib import md5
from slugify import slugify
import htmlmin
import pytz


TOKEN_LIFE = 86400

###################################################
# Utilities
###################################################
# token has userId embeded
# when we validate token, extract userId
###################################################
def generate_auth_token(userId, expiration = TOKEN_LIFE):
  s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
  return s.dumps({'userId': userId})

###################################################
# userId embeded in token
# extract & return
###################################################
def get_custid_from_token(token):
  s = Serializer(current_app.config['SECRET_KEY'])
  try:
    data = s.loads(token)
  except SignatureExpired :
    return None
  except BadSignature:
    return None
  return data['userId']

###################################################
# called by all methods to construct response
# returns JSONified result
###################################################
def res_str(status_code, resp_code, message, results=None):
  """
  return string contains
  status: HTTP Status Codes (uses only subset of all codes)
  code: internal success & error codes. each operation should be tagged with 
  		a code, for easy debugging
  message: detailed message for display to user or debugging
  results: optional python list  
  """
  if results:
    ret_str = {'status': status_code, 'code': resp_code, 'message': message, 'results': results}
  else:
    ret_str = {'status': status_code, 'code': resp_code, 'message': message}
  return ret_str

###################################################
# Main Methods
###################################################

def create_user(email=None, password=None):
  """ 
  input: email & password;
  create user id
  create directory for userId
  bulk insert & export site files will use this directory
  """
  if not email or not password:
    ret_str = res_str(400, 4001, "Email Id or Password Not Provided")
    print ret_str
  else:    
    try:
      new_user = User()
      new_user.email = email
      new_user.password = md5(password).hexdigest()
      db.session.add(new_user)
      db.session.commit()

      dir_to_create = os.path.join(current_app.config['BASE_DIR'],'user_files', str(new_user.id))
      if not os.path.exists(dir_to_create):
        os.makedirs(dir_to_create)
      ret_str = res_str(200, 2001, "User Created", {'userId': new_user.id})
    except IntegrityError as error:
      current_app.logger.error('Error while creating user: %s' % error)
      ret_str = res_str(500, 5001, "User Not Created", 'IntegrityError Error while inserting user %s' % new_user.email)
  return ret_str

def get_token(email=None, password=None):
  """
  input: email & password
  returns a token which has to be used for further calls
  """
  if not email and not password:
    ret_str = res_str(400, 4001, "Email Id or Password Not Provided")
  else:
    user = User.query.filter_by(email = email,
            password = md5(password).hexdigest()).first()
    if user is None:
      ret_str = res_str(400, 4002, "User Not Found Or Password Wrong")
    else:
      token = generate_auth_token(user.id)
      ret_str = res_str(200, 2001, "Token embeded. Use for further calls", {'token': token})    
  return ret_str

# TODO: is there a need for sign_out here in base?
def sign_out():
  return

def get_sites_for_user(token):
  """
  token: unexpired token; user id will be embeded
  """
  cust_id = get_custid_from_token(token)
  if not cust_id:
    ret_str = res_str(400, 4003, 'Check your token')
  else:
    my_sites = User.query.get(cust_id).sites.all()
    ret_str = res_str(200, 2001, 'Sites for user', {'sites': my_sites})
  print ret_str
  return ret_str

def create_site(token, site_details):
  """
  token: unexpired token; user id will be embeded
  site_details: details in json
  will contain (* indicates mandatory):
    site_name *
    nick_name *
    tagline
    description
    url *
    statcounter_id
    g_analytics_id
    clicky_id
    disqus_name
    dest_dir *
  """
  
  cust_id = get_custid_from_token(token)
  if not cust_id:
    ret_str = res_str(400, 4003, 'Check your token')
  else:
    if 'sitename' not in site_details or \
      'nickname' not in site_details or \
      'url' not in site_details or \
      'destDir' not in site_details:
      ret_str = res_str(400, 4004, 'Missing mandatory fields for create_site')
    else:
      try:
        new_site = Site(
          name          = site_details['sitename'],
          nickname      = site_details['nickname'],
          tagline       = site_details['tagline'],
          description   = site_details['description'],
          url           = site_details['url'],
          statcounterId = site_details['statcounterId'],
          gAnalytics    = site_details['gAnalytics'],
          clickyId      = site_details['clickyId'],
          disqusName    = site_details['disqusName'],
          destDir       = site_details['destDir'],
          owner         = cust_id
        )
        db.session.add(new_site)
        db.session.commit()      
        try:
          base_dir = current_app.config['BASE_DIR']
          template_dir = current_app.config['TEMPLATE_DIR']
          site_files_dir = os.path.join(base_dir, 'site_files', str(new_site.id), 'template')
          copytree(template_dir, os.path.join(base_dir,site_files_dir))
          ret_str = res_str(200, 2001, 'Site created successfully')
        except Exception as e:
          current_app.logger.error('Error while creating site:%s is:%s' % (site_details['sitename'], e.message))      
          ret_str = res_str(400, 4006, 'Error while creating new directory for new site')
      except Exception as e:
        current_app.logger.error('Error while creating site:%s is:%s' % (site_details['sitename'], e.message))
        ret_str = res_str(400, 4005, 'Error while creating new site')    
  return ret_str

def update_site():
  return

def delete_site():
  return

def create_entry():
  return

def update_entry():
  return

def delete_entry():
  return

def get_entries_for_site():
  return

def generate_a_site():
  return

def export_a_site():
  return

def insert_entries_from_files():
  return