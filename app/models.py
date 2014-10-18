from app import db
from datetime import datetime
from slugify import slugify

#
# email is used for login
#
class User(db.Model):
  id        = db.Column(db.Integer, primary_key=True)
  email     = db.Column(db.String(120), index=True, unique=True)
  password  = db.Column(db.String(100))
  name      = db.Column(db.String(120))
  join_date = db.Column(db.DateTime)
  active    = db.Column(db.Boolean)
  twitter   = db.Column(db.String(20))
  fb        = db.Column(db.String(20))
  gplus     = db.Column(db.String(50))
  sites     = db.relationship('Site', backref='owner', lazy='dynamic', cascade="all,delete")
# for discussion about passing multiple arguments & handling them
# ref: http://stackoverflow.com/a/682513/770719 &
# http://stackoverflow.com/a/1098556/770719
  def __init__(self, **kwargs):
    self.email     = kwargs.get('email')
    self.password  = kwargs.get('password')
    self.name      = kwargs.get('name', '')
    self.join_date = datetime.now()
    self.active    = True
    self.twitter   = kwargs.get('twitter', '')
    self.fb        = kwargs.get('fb', '')
    self.gplus     = kwargs.get('gplus', '')

  def __repr__(self):
    return '<User %r>' % (self.name or self.email)

class Site(db.Model):
  id            = db.Column(db.Integer, primary_key=True)
  name          = db.Column(db.String(250))
  nickname      = db.Column(db.String(20))
  tagline       = db.Column(db.String(250))
  description   = db.Column(db.String(250))
  gTime         = db.Column(db.DateTime) #last generated time
  statcounterId = db.Column(db.String(20)) #projectid;securityid
  gAnalytics    = db.Column(db.String(20))
  disqusName    = db.Column(db.String(20))
  fbpageId      = db.Column(db.String(20))
  destDir       = db.Column(db.String(100))
  url           = db.Column(db.String(100), unique=True)
  active        = db.Column(db.Boolean)
  createdAt     = db.Column(db.DateTime)
  user_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
  entries       = db.relationship('Entry', backref='site', lazy='dynamic', cascade="all,delete")

  def __init__(self, **kwargs):
    self.name          = kwargs.get('name')
    self.nickname      = kwargs.get('nickname')
    self.tagline       = kwargs.get('tagline','')
    self.description   = kwargs.get('description','')
    self.gTime         = datetime.now()
    self.statcounterId = kwargs.get('statcounterId', '')
    self.gAnalytics    = kwargs.get('gAnalytics', '')
    self.disqusName    = kwargs.get('disqusName', '')
    self.fbpageId      = kwargs.get('fbpageId', '')
    self.destDir       = kwargs.get('destDir', '')
    self.url           = kwargs.get('url')
    self.active        = True
    self.createdAt     = datetime.now()
    self.user_id       = kwargs.get('owner')

  def __repr__(self):
    return '<Site %r>' % self.nickname

# TODO: find after_update / after_insert events to get tweetHTML
# TODO: short way for default values as in flask-peewee
# TODO: a way to indicate missing values and not allow to save
class Entry(db.Model):
  id        = db.Column(db.Integer, primary_key=True)
  title     = db.Column(db.String(50))
  subtitle  = db.Column(db.String(100))
  slug      = db.Column(db.String(50))
  tags      = db.Column(db.String(50))
  excerpt   = db.Column(db.String(500))
  tweetId   = db.Column(db.String(20))
  tweetHTML = db.Column(db.String(100))
  content   = db.Column(db.Text)
  publishAt = db.Column(db.DateTime) # publish at
  isPost    = db.Column(db.Boolean)
  createdAt = db.Column(db.DateTime)
  site_id   = db.Column(db.Integer, db.ForeignKey('site.id'))

  def __init__(self, **kwargs):
    self.title     = kwargs.get('title')
    self.subtitle  = kwargs.get('subtitle')
    self.slug      = kwargs.get('slug', slugify(self.title))
    self.tags      = kwargs.get('tags', '')
    self.excerpt   = kwargs.get('excerpt','')
    self.tweetId   = kwargs.get('tweetId', '')
    self.content   = kwargs.get('content','')
    self.publishAt = kwargs.get('publishAt', datetime.now())
    self.isPost    = kwargs.get('isPost', True)
    self.createdAt = datetime.now()
    self.site_id   = kwargs.get('site')

  def __repr__(self):
    return self.title
