"""
models imports app, but app does not import models so we haven't created
any loops.
"""
import datetime

from flask_peewee.auth import BaseUser  # provides password helpers..
from peewee import *

from app import db


class User(db.Model, BaseUser):
  email     = CharField(unique = True) #used for login
  password  = CharField()
  name      = CharField(null = True)
  join_date = DateTimeField(default = datetime.datetime.now)
  active    = BooleanField(default = True)
  twitter   = CharField(null = True)
  fb        = CharField(null = True)
  gplus     = CharField(null = True)

  def __unicode__(self):
    return self.name

class Site(db.Model):
  name          = CharField(null = False)
  nickname      = CharField(null = False)
  tagline       = CharField(null = True)
  description   = CharField(null = True)
  gTime         = DateTimeField(null = True) #last generated time
  statcounterId = CharField(null = True) #projectid;securityid
  gAnalytics    = CharField(null = True)
  disqusName    = CharField(null = True)
  fbpageId      = CharField(null = True)
  destDir       = CharField(null = True)
  url           = CharField(unique = True, null = False)
  active        = BooleanField(default = True)
  createdAt     = DateTimeField(default = datetime.datetime.now)
  user          = ForeignKeyField(User, related_name = 'sites')

  def __unicode__(self):
    return self.nickname

class Entry(db.Model):
  title     = CharField(null = False)
  subTitle  = CharField(null = True)
  slug      = CharField(null = False)
  tags      = CharField(null = True)
  excerpt   = CharField(null = True)
  tweetId   = CharField(null = True)
  tweetHTML = CharField(null = True)
  content   = TextField(null=False)
  ptime     = DateTimeField(default = datetime.datetime.now)
  isPage    = BooleanField(default = False)
  createdAt = DateTimeField(default = datetime.datetime.now)
  site      = ForeignKeyField(Site, related_name = 'entries')

  def __unicode__(self):
    return self.slug
