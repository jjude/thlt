from tests import TestCase
from flask import current_app, json

class TestAPI(TestCase):
  def test_1001_index(self):
    TestAPI.base_dir = current_app.config['BASE_DIR']
    self._test_get_request('/api/v1/')

  def test_1002_404(self):
    self._test_get_404('/api/v1/1')

###################################################
# signup
###################################################
  def test_1010_signup(self):
    data = json.dumps({'email': 'hello@gmail.com',
     'password': 'iamgreat'})
    response = self.client.post('/api/v1/signup', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 2001)

  def test_1011_signup_again(self):
    data = json.dumps({'email': 'hello@gmail.com',
     'password': 'iamgreat'})
    response = self.client.post('/api/v1/signup', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 5001)

  def test_1012_signup_with_incomplete_details(self):
    data = json.dumps({'email': 'hello@gmail.com'})
    response = self.client.post('/api/v1/signup', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4001)
    data = json.dumps({'password': '1234'})
    response = self.client.post('/api/v1/signup', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4001)
    data = json.dumps({})
    response = self.client.post('/api/v1/signup', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4001)

  def test_1013_signup_get_not_allowed(self):
    data = {'email': 'hello@gmail.com',
     'password': 'iamgreat'}
    response = self.client.get('/api/v1/signup', data=data, follow_redirects=True)
    self.assert_405(response)

###################################################
# signin
###################################################
  def test_1020_signin_get_not_allowed(self):
    data = {'email': 'hello@gmail.com',
     'password': 'iamgreat'}
    response = self.client.get('/api/v1/signin', data=data, follow_redirects=True)
    self.assert_405(response)

  def test_1021_signin_wrong_email(self):
    data = json.dumps({'email': 'hell@gmail.com',
     'password': 'wrongpwd'})
    response = self.client.post('/api/v1/signin', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4002)

  def test_1022_signin_wrong_password(self):
    data = json.dumps({'email': 'hello@gmail.com',
     'password': 'wrongpwd'})
    response = self.client.post('/api/v1/signin', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4002)

  def test_1023_signin_get_token(self):
    data = json.dumps({'email': 'hello@gmail.com',
     'password': 'iamgreat'})
    response = self.client.post('/api/v1/signin', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    TestAPI.token_for_testing = response.json['results']['token']
    self.assertEquals(response.json['code'], 2001)
    self.assertIn('token', response.json['results'])

###################################################
# sites
###################################################
  def test_1030_create_site_with_empty_values(self):
    data = json.dumps({})
    response = self.client.post('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4003)

  def test_1031_create_site_with_wrong_token(self):
    site_details = {'sitename': 'testing api',
     'nickname': 'api testing',
     'tagline': 'Spread the awareness of API creation',
     'description': 'We can talk about creating API all day long',
     'url': 'http://api.apitalks.com',
     'destDir': '/Users/apitester/Downloads',
     'statcounterId': 'p1234',
     'gAnalytics': 'UA-1234',
     'clickyId': '09080',
     'disqusName': 'apiblog'}
    data = json.dumps({'token': '1234',
     'data': site_details})
    response = self.client.post('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4003)

  def test_1032_create_site(self):
    site_details = {'sitename': 'testing api',
     'nickname': 'api testing',
     'tagline': 'Spread the awareness of API creation',
     'description': 'We can talk about creating API all day long',
     'url': 'http://api.apitalks.com',
     'destDir': '/Users/apitester/Downloads',
     'statcounterId': 'p1234',
     'gAnalytics': 'UA-1234',
     'clickyId': '09080',
     'disqusName': 'apiblog'}
    data = json.dumps({'token': TestAPI.token_for_testing,
     'data': site_details})
    response = self.client.post('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 2001)

  def test_1033_create_site_with_duplicate_url(self):
    site_details = {'sitename': 'testing api',
     'nickname': 'api testing',
     'tagline': 'Spread the awareness of API creation',
     'description': 'We can talk about creating API all day long',
     'url': 'http://api.apitalks.com',
     'destDir': '/Users/apitester/Downloads',
     'statcounterId': 'p1234',
     'gAnalytics': 'UA-1234',
     'clickyId': '09080',
     'disqusName': 'apiblog'}
    data = json.dumps({'token': TestAPI.token_for_testing,
     'data': site_details})
    response = self.client.post('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4005)    

  def test_1034_create_site_with_incomplete_details(self):
    site_details = {'nickname': 'api testing',
     'tagline': 'Spread the awareness of API creation',
     'description': 'We can talk about creating API all day long',
     'url': 'http://api.apitalks.com',
     'destDir': '/Users/apitester/Downloads',
     'statcounterId': 'p1234',
     'gAnalytics': 'UA-1234',
     'clickyId': '09080',
     'disqusName': 'apiblog'}
    data = json.dumps({'token': TestAPI.token_for_testing,
     'data': site_details})
    response = self.client.post('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4004)

  def test_1035_update_site(self):
    data = json.dumps({'token': TestAPI.token_for_testing})
    response = self.client.get('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    site_id = response.json['results']['sites'][0]['id']

    site_details = {'sitename': 'updated site api',
     'tagline': 'Spread the awareness of API creation',
     'description': 'We can talk about creating API all day long',
     'destDir': '/Users/apitester/Downloads',
     'statcounterId': 'p1234',
     'gAnalytics': 'UA-9999',
     'clickyId': '09080',
     'disqusName': 'apiblog2'}
    data = json.dumps({'token': TestAPI.token_for_testing,
     'data': site_details})
    response = self.client.put('/api/v1/sites?siteId=%s' % (site_id), data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 2001)
    
    data = json.dumps({'token': TestAPI.token_for_testing})
    response = self.client.get('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['results']['sites'][0]['disqusName'], 'apiblog2')
    self.assertEquals(response.json['results']['sites'][0]['gAnalytics'], 'UA-9999')
    self.assertEquals(response.json['results']['sites'][0]['name'], 'updated site api')
    
  def test_1036_get_sites_with_empty_values(self):
    data = json.dumps({})
    response = self.client.get('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4003)

  def test_1037_get_sites(self):
    data = json.dumps({'token': TestAPI.token_for_testing})
    response = self.client.get('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 2001)    
###################################################
# entries
###################################################
  def test_1050_get_entries_before_creating_any_entry(self):
    data = json.dumps({'token': TestAPI.token_for_testing})
    response = self.client.get('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    site_id = response.json['results']['sites'][0]['id']

    response = self.client.get('/api/v1/entries?siteId=%s' % (site_id), data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    # since we haven't yet created any entries, results should be empty
    self.assertEquals(response.json['code'], 2001)
    self.assertEquals(len(response.json['results']['entries']), 0)

  def test_1051_create_entry_with_empty_token(self):
    data = json.dumps({})
    response = self.client.post('/api/v1/entries', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4003)
    
  def test_1051_create_entry_with_empty_site(self):
    data = json.dumps({'token': TestAPI.token_for_testing})
    response = self.client.post('/api/v1/entries', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4007)    

  def test_1051_create_entry_with_empty_entry_values(self):
    data = json.dumps({'token': TestAPI.token_for_testing})
    response = self.client.get('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    site_id = response.json['results']['sites'][0]['id']
    
    data = json.dumps({'token': TestAPI.token_for_testing, 'data':{'siteId':site_id}})
    response = self.client.post('/api/v1/entries', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 4007)    
    
  def test_1051_create_entry(self):
    data = json.dumps({'token': TestAPI.token_for_testing})
    response = self.client.get('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    site_id = response.json['results']['sites'][0]['id']
    
    data = json.dumps({'token': TestAPI.token_for_testing, 
                       'data':{'siteId':site_id,
                              'title':'let us rock the world man',
                              'content': 'do you think it will?'}})
    response = self.client.post('/api/v1/entries', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    self.assertEquals(response.json['code'], 2001)
    
  def test_1053_get_entries_after_creating_entry(self):
    data = json.dumps({'token': TestAPI.token_for_testing})
    response = self.client.get('/api/v1/sites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    site_id = response.json['results']['sites'][0]['id']
    
    response = self.client.get('/api/v1/entries?siteId=%s' % (site_id), data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
    # since we haven't yet created any entries, results should be empty
    self.assertEquals(response.json['code'], 2001)
    print response.json
    self.assertEquals(len(response.json['results']['entries']), 1)
    