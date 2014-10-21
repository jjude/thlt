# thlt - static blog engine for the rest of us


###What is this?
Thlt is a static blog engine that sits somewhere between wordpress and static generators like Jekyll. Static generators lack flexibility like posting via email, APIs, clients etc. Currently static generators are only for geeks. Thlt is an experiement to bring that to masses.

Even if that experiment fails, I hope I would've learnt development, deployment and ops of cloud based apps.

###How to use


###Features implemented

1. new user signup
2. signin
3. signout
4. create new sites
5. configure output folder for a site
6. delete a site
7. create, modify & delete an entry
8. generate static htmls, including feeds.xml and sitemap. these are stored in the output folder configured earlier
9. import entries from files    

###Laundry List of features to be implemented (in no particular order)
1. forgot password
2. confirm user account
3. xmlrpc api
4. read templates from git repo
5. transport htmls to google appspot & amazon s3
6. use dockers to deploy
7. support promotional messages on top bar
8. import from wordpress
9. export to wordpress
10. preview
11. check output to git repo
12. post by email

13. hot-deploy
14. have deployment in two PaSS and using loadbalancer to route
15. automate testing, deployment, post-deployment testing
16. monitoring (pingdom?)
17. auto-restart after failures
18. transfer generated html to ftp of destination site
19. read from dropbox

###Technologies used
Flask
Jinja2
SQLite (for development)
ClearDB on Azure

###What's in a name
thlt = தாலாட்டு
