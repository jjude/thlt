from flask import url_for
from tests import TestCase

class TestFrontEnd(TestCase):

    def test_2001_index_signup(self):
        """
        where there is no user, it should route to signup
        """
        response = self.client.get('/')
        self.assertRedirects(response, '/signin/')

    def test_2002_signup(self):
        pass