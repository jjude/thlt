from tests import TestCase
from flask import current_app, json

class TestAPI(TestCase):

    def test_1001_index(self):
        self._test_get_request('/api/v1/')

    def test_1002_404(self):
        self._test_get_404('/api/v1/1')

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

    def test_1020_signin_get_not_allowed(self):
        data = {'email': 'hello@gmail.com',
         'password': 'iamgreat'}
        response = self.client.get('/api/v1/signup', data=data, follow_redirects=True)
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

    def test_1030_get_site(self):
        pass

    def test_1040_create_site_with_empty_values(self):
        data = json.dumps({})
        response = self.client.post('/api/v1/createsite', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
        self.assertEquals(response.json['code'], 4003)

    def test_1041_create_site_with_wrong_token(self):
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
        response = self.client.post('/api/v1/createsite', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
        self.assertEquals(response.json['code'], 4003)

    def test_1042_create_site(self):
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
        response = self.client.post('/api/v1/createsite', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
        self.assertEquals(response.json['code'], 2001)

    def test_1043_create_site_with_incomplete_details(self):
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
        response = self.client.post('/api/v1/createsite', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
        self.assertEquals(response.json['code'], 4004)

    def test_1044_create_site_with_incomplete_details(self):
        site_details = {'sitename': 'testing api',
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
        response = self.client.post('/api/v1/createsite', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
        self.assertEquals(response.json['code'], 4004)

    def test_1050_get_sites_with_empty_values(self):
        data = json.dumps({})
        response = self.client.get('/api/v1/getsites', data=data, follow_redirects=True, headers={'Content-type': 'application/json'})
        print response.json