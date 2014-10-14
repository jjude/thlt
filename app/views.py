#############
#Ref for sessions: http://stackoverflow.com/a/11785722/770719
#############
# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for, flash

# logging
import logging
import pprint

# sessions
from flask import session
from datetime import timedelta

# login_decorator
from functools import wraps

# flask-peewee database
from peewee import *
from flask_peewee.db import Database
from flask_peewee.utils import get_object_or_404, slugify

# import our app
from app import app, db

# import models
from models import User, Site, Entry
from auth import *
from hashlib import md5

# other python ops
from shutil import copytree, rmtree
import os
import datetime

# TODO: implement flash, csrf in forms

# decorator
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if "userId" in session and session["userId"] != 0:
			return f(*args, **kwargs)
		return redirect('/signin/')
	return decorated_function

def auth_user(user):
	session.permanent = True
	app.permanent_session_lifetime = timedelta(days=10)
	session['loggedIn'] = True
	session['userId'] = user.id
	flash("You are logged in")
	return

# create new Entry
# EntryValues as dict
def createEntry(siteId, entryValues):
	try:
		with db.database.transaction():
			newEntry = Entry.create(
					title		= entryValues['title'],
					subTitle = entryValues['subTitle'],
					slug		 = entryValues['slug'] if 'slug' in entryValues else slugify(title),
					tags		 = entryValues['tags'],
					excerpt	= entryValues['excerpt'],
					tweetId	= entryValues['tweetId'],
					content	= entryValues['content'],
					ptime		= entryValues['ptime'] if 'ptime' in entryValues else datetime.datetime.now(),
					isPage	 = 0 if entryValues['isPage'] == '0' else 1,
					site		 = siteId
					)
	except Exception as e:
		# TODO: logging
			print e.message
	return

# update existing entry
# EntryValues as dict
def updateEntry(entryId, entryValues):
	entry = Entry.get(Entry.id == entryId)
	if entry:
		try:
			with db.database.transaction():
				entry.title		= entryValues['title']
				entry.subTitle = entryValues['subTitle']
				entry.slug		 = entryValues['slug'] if 'slug' in entryValues else slugify(entryValues['title'])
				entry.tags		 = entryValues['tags']
				entry.excerpt	= entryValues['excerpt']
				entry.tweetId	= entryValues['tweetId']
				entry.content	= entryValues['content']
				entry.ptime		= entryValues['ptime'] if 'ptime' in entryValues else datetime.datetime.now()
				entry.isPage	 = entryValues['isPage']
				entry.save()
		except Exception as e:
			# TODO: logging
			print e
	return


##################################################
# Routing starts
##################################################

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email		= request.form['email']
		password = request.form['password']

		if email and password:
			try:
				with db.database.transaction():
					user = User.create(email = email,
							password = md5(password).hexdigest())
					auth_user(user) #sets user as authenticated in session
					return redirect('/mysites/')
			except IntegrityError:
				flash("Did you signup already? Try signin")

	return render_template('users/signup.html')

@app.route('/signin/', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		email		= request.form['email']
		password = request.form['password']

		if email and password:
			try:
				user = User.get(email = email,
						password = md5(password).hexdigest())
				flash("Did you already signup? Try to signin")
			except User.DoesNotExist:
				flash("User Id or Password is Incorrect")
			else:
				auth_user(user)
				return redirect('/mysites/')
	return render_template('/users/signin.html')

@app.route('/signout/')
def signout():
	session.clear()
	return redirect('/')

##################################################
# Site Routing
##################################################

@app.route('/newsite/', methods=['GET', 'POST'])
@login_required
def newsite():
	if request.method == 'POST':
		if not request.form['sitename']:
			flash ("Sitename is required")
		if not request.form['url']:
			flash ("URL is required")

		try:
			with db.database.transaction():
				newSite = Site.create(
					name					= request.form['sitename'],
					nickname			= request.form['nickname'],
					tagline			 = request.form['tagline'],
					description	 = request.form['description'],
					url					 = request.form['url'],
					statcounterId = request.form['statcounterId'],
					gAnalytics		= request.form['gAnalytics'],
					disqusName		= request.form['disqusName'],
					destDir			 = request.form['destDir'],
					user					= session["userId"]
					)
				siteFilesDir = 'siteFiles/' + str(newSite.id) + '/template'
				copytree ('siteTemplate', siteFilesDir)
		except Exception as e:
			# TODO: logging
			print e.message
		else:
			return redirect('/mysites/')
	return render_template('/sites/newsite.html')

@app.route('/mysites/')
@login_required
def mysites():
	mySites = Site.select().join(User).where(User.id == session["userId"])
	return render_template('/sites/mysites.html', mySites = mySites)

@app.route('/deleteSite/<int:siteId>/')
@login_required
def deleteSite(siteId):
	try:
		with db.database.transaction():
			siteToDelete = Site.get(Site.id == siteId)
			# delete all entries too
			siteToDelete.delete_instance(recursive=True)

			siteFilesDir = 'siteFiles/' + str(siteId)
			if os.path.isdir(siteFilesDir):
				rmtree(siteFilesDir)
	except Exception as e:
		# TODO: logging
		print e.message

	return redirect('/mysites/')

@app.route('/editSite/<int:siteId>/', methods=['GET','POST'])
@login_required
def editSite(siteId):
	site = get_object_or_404(Site, Site.id == siteId)
	if request.method == 'POST':
		if not request.form['sitename']:
			flash ("Sitename is required")

		try:
			with db.database.transaction():
				site.name					= request.form['sitename']
				site.tagline			 = request.form['tagline']
				site.description	 = request.form['description']
				site.statcounterId = request.form['statcounterId']
				site.gAnalytics		= request.form['gAnalytics']
				site.disqusName		= request.form['disqusName']
				site.destDir			 = request.form['destDir']
				site.save()
				flash("Your changes are saved")
		except Exception as e:
			# TODO: logging
				print e.message
		else:
			return redirect('/mysites/')

	return render_template('/sites/editsite.html', site = site)

@app.route('/displaySite/<int:siteId>/')
@login_required
def displaySite(siteId):
	entries = Entry.select().join(Site).where(Site.id == siteId).order_by(Entry.ptime.desc())
	site = Site.get(Site.id == siteId)
	session['siteId'] = siteId
	session['siteNickName'] = site.nickname
	return render_template('/sites/displaysite.html', entries = entries, site = site)

@app.route('/generateSite/<int:siteId>/')
@login_required
def generateSite(siteId):
	# flask by default looks for template in /template folder
	# so we need to create a new environment
	from jinja2 import Environment, FileSystemLoader
	import markdown2 as md

	site = Site.get(Site.id == siteId)

	# site details
	siteDetails							 = {}
	siteDetails['name']			 = site.name
	siteDetails['url']				= site.url
	siteDetails['tagline']		= site.tagline
	siteDetails['gAnalytics'] = site.gAnalytics if site.gAnalytics else ''
	siteDetails['disqusName'] = site.disqusName if site.disqusName else ''
	if site.statcounterId:
		projectId, securityId = site.statcounterId.split(';')
		siteDetails['statcounterProjectId']	= projectId
		siteDetails['statcounterSecurityId'] = securityId
	else:
		siteDetails['statcounterId'] = ''

	# user details
	userDetails						= {}
	userDetails['name']		= site.user.name
	userDetails['twitter'] = site.user.twitter
	userDetails['gplus']	 = site.user.gplus

	envDetails = {}
	# TODO: this needs to be magically set
	envDetails['env'] = app.config['ENVIRONMENT']
	# generated time
	envDetails['gTime'] = datetime.datetime.now()

	templateBaseDir = os.path.join('siteFiles', str(site.id), 'template')
	outDir          = os.path.join('output', str(site.id), 'html')
	assetsDir       = os.path.join(templateBaseDir, 'assets')

	if os.path.exists(outDir):
		print "%s path exists" % outDir
		rmtree(outDir, ignore_errors=True)
	else:
		print "%s path doesnt exists" % outDir

	#os.makedirs(outDir)
	# copy assets dir
	copytree(assetsDir, outDir)

	# it is expected that this directory exists
	destDir = site.destDir

	thltEnv = Environment(loader=FileSystemLoader(templateBaseDir))

	# has unique tags
	siteTags = {}
	# siteTags will look like
	# {'tag1': ['first-post', 'third-post'], 'tag2': ['third-post]'}

	# allEntries contains both posts & pages (used for sitemap etc)
	allEntries = []
	# onlyposts excludes pages (used for index & feeds)
	onlyPosts = []
	# TODO: sqlite as in-momory db

	for entry in site.entries.order_by(Entry.ptime.desc()):
		print "generating %s" % entry.title
		if entry.tags and entry.tags is not None and entry.tags != 'None':
			tagsHTML = '|'.join(["<a href=/tags/%s/>%s</a>" % (tag.strip(), tag.strip()) \
													for tag in entry.tags.split(",")])
		else:
			tagsHTML = ''

		# this dict is writen into siteTags
		# so content is writen into this dict after
		# inserting into siteTags
		# as content is not needed for siteTags
		entryDetails = {}
		entryDetails['title'] = entry.title
		if entry.subTitle is not None or entry.subTitle != 'null':
			entryDetails['subTitle'] = entry.subTitle
		else:
			entryDetails['subTitle'] = ''
		entryDetails['slug'] = entry.slug
		entryDetails['url'] = site.url + '/' + entry.slug + '/'
		entryDetails['type'] = 'post' if entry.isPage == 0 else 'page'
		entryDetails['excerpt'] = entry.excerpt
		entryDetails['ptime'] = entry.ptime
		entryDetails['tagsHTML'] = tagsHTML
		entryDetails['tags'] = entry.tags

		# push tags into siteTags
		# TODO: check if this can be done by in-memory sqlite
		if entry.tags is not None:
			for tag in entry.tags.split(','):
				tag = tag.strip()
				if tag in siteTags:
					siteTags[tag].append(entryDetails)
				else:
					siteTags[tag] = []
					siteTags[tag].append(entryDetails)

		# now add content before generating the html
		# convert content to markdown with extensions
		entryDetails['content'] = md.markdown(entry.content,
				extras=["fenced-code-blocks", "footnotes", "wiki-tables", "tables"])

		# push to allEntries
		# this is used to generate both main index & sitemap
		allEntries.append(entryDetails)
		if entry.isPage == 0:
			onlyPosts.append(entryDetails)

		# create individual posts
		currentTemplate = thltEnv.get_template('post.html')
		dirToCreate = os.path.join(outDir, entry.slug)
		if not os.path.exists(dirToCreate):
			os.makedirs(dirToCreate)
		HTMLToStore = currentTemplate.render(site=siteDetails, entry=entryDetails, \
									user=userDetails, envDetails=envDetails)
		with open(os.path.join(outDir, entry.slug, 'index.html'), "wb") as fileToSave:
			fileToSave.write(HTMLToStore.encode('utf-8'))

	# once done with individual entries, create other ones
	# create sitemaps
	currentTemplate = thltEnv.get_template('sitemap.html')
	HTMLToStore = currentTemplate.render(site=siteDetails, entries=allEntries, \
								tags=siteTags.keys(), envDetails=envDetails)
	with open(os.path.join(outDir, 'sitemap.xml'), "wb") as fileToSave:
		fileToSave.write(HTMLToStore)

	# index
	currentTemplate = thltEnv.get_template('index.html')
	HTMLToStore = currentTemplate.render(site=siteDetails, entries=onlyPosts, \
								 user=userDetails, envDetails=envDetails)
	with open(os.path.join(outDir, 'index.html'), "wb") as fileToSave:
		fileToSave.write(HTMLToStore.encode('utf-8'))

	# tags
	dirToCreate = os.path.join(outDir, 'tags')
	if not os.path.exists(dirToCreate):
		os.makedirs(dirToCreate)
	currentTemplate = thltEnv.get_template('tags.html')
	HTMLToStore = currentTemplate.render(site=siteDetails, user=userDetails, \
									envDetails=envDetails, tags=siteTags)
	with open(os.path.join(outDir, 'tags', 'index.html'), "wb") as fileToSave:
		fileToSave.write(HTMLToStore.encode('utf-8'))

	# individual tag
	for tag in siteTags:
		dirToCreate = os.path.join(outDir, 'tags', tag)
		if not os.path.exists(dirToCreate):
			os.makedirs(dirToCreate)
		currentTemplate = thltEnv.get_template('tag.html')
		HTMLToStore = currentTemplate.render(site=siteDetails, user=userDetails, \
										envDetails=envDetails, tag=tag, entries=siteTags[tag])
		with open(os.path.join(outDir, 'tags', tag, 'index.html'), "wb") as fileToSave:
			fileToSave.write(HTMLToStore.encode('utf-8'))

	# archives
	dirToCreate = os.path.join(outDir, 'archives')
	if not os.path.exists(dirToCreate):
		os.makedirs(dirToCreate)
	currentTemplate = thltEnv.get_template('archives.html')
	HTMLToStore = currentTemplate.render(site=siteDetails, user=userDetails, \
									envDetails=envDetails, entries=onlyPosts)
	with open(os.path.join(outDir, 'archives', 'index.html'), "wb") as fileToSave:
		fileToSave.write(HTMLToStore.encode('utf-8'))

	# feeds
	# only 10 posts
	currentTemplate = thltEnv.get_template('feeds.html')
	HTMLToStore = currentTemplate.render(site=siteDetails, user=userDetails, \
									envDetails=envDetails, entries=onlyPosts[:10])
	with open(os.path.join(outDir, 'feed.xml'), "wb") as fileToSave:
		fileToSave.write(HTMLToStore.encode('utf-8'))

	# now start transfering the files to destDir
	# using subprocess to sync two folders
	# TODO: will have to use ssh to sync a remote folder
	# Ref: https://code.google.com/p/remotefoldersync/source/browse/trunk/ssh.py
	# or fabric project

	import subprocess
	logFile = str(site.id) + 'sync.log'
	dirToCreate = 'synclogs'
	if not os.path.exists(dirToCreate):
		os.makedirs(dirToCreate)

	# ref: http://stackoverflow.com/a/22757221/770719
	# ref: http://sharats.me/the-ever-useful-and-neat-subprocess-module.html
	# rsyncArguments = ["-avzr", "--delete", "--exclude='.*'"]
	rsyncArguments = ["-avzr", "--delete"]
	rsyncArguments.append("--log-file=" + os.path.join(dirToCreate, logFile))
	localFolder = outDir + '/'
	remoteFolder = destDir + '/'
	rsyncArguments.append(localFolder)
	rsyncArguments.append(destDir)
	print rsyncArguments
	returncode = subprocess.call(["rsync"] + rsyncArguments)
	if returncode == 0:
		print "sync successfull"
	else:
		print "sync failed with %s " % str(returncode)

	return redirect('/mysites/')

@app.route('/insertFromFiles/')
@login_required
def insertFromFiles():

	import yaml

	"""
	Start creating the post
	File contents will be in below template; <content> is always in md
	Meta data can be in any order but should be delimitted by ==== in end
	If permalink is given it will overwrite the existing one

	Blog:
	Title:
	subTitle:

	date: <datetime> #publish at this time(Jun 1 2005	24:33);
				if not present, publish immediately
	tags: <comma separated tags>
	slug: <slug can be provided to override;
					if slug is not in db for this blog, new entry will be created>
	tweetId:
	type: <post or page>
	excerpt:
	---
	<content>
	"""

	dirToRead = 'userFiles/%s' % session['userId']
	for fileName in os.listdir(dirToRead):
		fileName = os.path.join(dirToRead, fileName)
		print "dealing with %s" % fileName
		if fileName.endswith('.md'):
			with open(fileName, 'r') as entry:
				fileContent = entry.read()
				metadata, postContent = fileContent.split('---')
				postMeta = yaml.load(metadata)

				blogName = postMeta['blog'] if 'blog' in postMeta else ''
				# sitesUpdated will contain list of sites into which entries were
				# inserted. this is used to generate these sites once insertion is
				# complete
				sitesUpdated = []
				EntryValues  = {}
				EntryValues['title']    = postMeta['title'] if 'title' in postMeta else ''
				EntryValues['subTitle'] = postMeta['subtitle'] if 'subtitle' in postMeta else ''
				EntryValues['ptime']    = datetime.datetime.strptime(postMeta['date'][:16], '%Y-%m-%d %H:%M') if 'date' in postMeta else ''
				EntryValues['slug']     = postMeta['slug'] if 'slug' in postMeta else slugify(EntryValues['title'])
				EntryValues['tags']     = postMeta['tags'] if 'tags' in postMeta else ''
				EntryValues['tweetId']  = postMeta['tweetId'] if 'tweetId' in postMeta else ''
				EntryValues['excerpt']  = postMeta['excerpt'] if 'excerpt' in postMeta else ''
				#if there was empty lines in the begining or at the end
				EntryValues['content']	= postContent.strip()
				EntryValues['isPage']	 = 0 if postMeta['type'] == 'post' else 1

				try:
					site = Site.get(Site.nickname == blogName)
				except Site.DoesNotExist:
					site = None
				if site:
					try:
						entry = Entry.get(Entry.slug == EntryValues['slug'])
					except Entry.DoesNotExist:
						entry = None
					sitesUpdated.append(site.id)
					if entry:
						# existing entry; update it
						updateEntry(entry.id, EntryValues)
					else:
						# create a new entry
						createEntry(site.id, EntryValues)
					# os.remove(fileName)
	print "sites inserted: %s" % sitesUpdated
	return redirect('/mysites/')

@app.route('/exportSite/<int:siteId>/')
@login_required
def exportSite(siteId):
	import os

	site = Site.get(Site.id == siteId)

	outDir = os.path.join('output', str(siteId), 'export')
	if os.path.exists(outDir):
		print "%s exists, going to delete it" % outDir
		rmtree(outDir)

	os.makedirs(outDir)

	for entry in site.entries.order_by(Entry.ptime.desc()):
		if entry.isPage == '1':
			entryType = 'page'
		else:
			entryType = 'post'

		entryFileName = "%s-%s.md" % (datetime.datetime.strftime(entry.ptime, '%Y'), entry.slug)
		exportContent = """blog: %s
id: %s
title: %s
subtitle: %s
date: %s
slug: %s
tags: %s
tweetId: %s
type: %s
excerpt: %s
---
%s
""" % (site.nickname, entry.id, entry.title, entry.subTitle, entry.ptime,
					entry.slug, entry.tags, entry.tweetId, entryType, entry.excerpt,
					entry.content)
		with open(os.path.join(outDir, entryFileName), "wb") as fileToSave:
			fileToSave.write(exportContent.encode('utf-8'))

	return redirect('/mysites/')

##################################################
# Entry Routing
##################################################

@app.route('/newEntry/', methods = ['GET', 'POST'])
@login_required
def newEntry():
	if not session['siteId']:
		return redirect('/mysites/')

	if request.method == 'POST':
		if not request.form['title']:
			flash('Title is required')
			return render_template('/entries/newEntry.html', siteNickName = session['siteNickName'])

		entryValues = {}
		entryValues['title']		= request.form['title']
		entryValues['subTitle'] = request.form['subTitle']
		entryValues['slug']		 = request.form['slug'] if request.form['slug'] else slugify(request.form['title'])
		entryValues['tags']		 = request.form['tags']
		entryValues['excerpt']	= request.form['excerpt']
		entryValues['tweetId']	= request.form['tweetId']
		entryValues['content']	= request.form['content']
		entryValues['ptime']		= datetime.datetime.strptime(request.form['ptime'][:16], '%Y-%m-%d %H:%M') if request.form['ptime'] else datetime.datetime.now()
		entryValues['isPage']	 = request.form['type'] if request.form['type'] == '0' else 1

		createEntry(session['siteId'], entryValues)

		siteURL = '/displaySite/%s' % session['siteId']
		return redirect(siteURL)

	return render_template('/entries/newEntry.html', siteNickName = session['siteNickName'])

@app.route('/editEntry/<int:entryId>/', methods = ['GET', 'POST'])
@login_required
def editEntry(entryId):
	if not session['siteId']:
		return redirect('/mysites/')

	if request.method == 'POST':
		if not request.form['title']:
			flash('title is mandatory')

	entry = get_object_or_404(Entry, Entry.id == entryId)
	if request.method == 'POST':
		if not request.form['title']:
			flash("title is mandatory")
			siteURL = '/displaySite/%s' % session['siteId']
			return redirect(siteURL)

		EntryValues						 = {}
		EntryValues['title']		= request.form['title']
		EntryValues['subTitle'] = request.form['subTitle']
		EntryValues['slug']		 = request.form['slug'] if request.form['slug'] else slugify(request.form['title'])
		EntryValues['tags']		 = request.form['tags']
		EntryValues['excerpt']	= request.form['excerpt']
		EntryValues['tweetId']	= request.form['tweetId']
		EntryValues['content']	= request.form['content']
		EntryValues['ptime']		= datetime.datetime.strptime(request.form['ptime'][:16], '%Y-%m-%d %H:%M') if request.form['ptime'] else datetime.datetime.now()
		EntryValues['isPage']	 = 0 if request.form['type'] == '0' else 1

		updateEntry(entryId, EntryValues)

		siteURL = '/displaySite/%s' % session['siteId']
		return redirect(siteURL)
	return render_template('/entries/editentry.html', entry = entry)

@app.route('/deleteEntry/<int:entryId>/')
@login_required
def deleteEntry(entryId):
	try:
		with db.database.transaction():
			entryToDelete = Entry.get(Entry.id == entryId)
			entryToDelete.delete_instance()

	except Exception as e:
		# TODO: logging
		print e.message

	siteURL = '/displaySite/%s' % session['siteId']
	return redirect(siteURL)
