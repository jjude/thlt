from flask import url_for, current_app
from tests import TestCase

class TestFrontEnd(TestCase):
  def test_2001_index_signup(self):
    """
    where there is no user, it should route to signup
    """
    TestFrontEnd.base_dir = current_app.config['BASE_DIR']
    response = self.client.get('/')
    self.assertRedirects(response, '/signin/')

  def test_2002_signup(self):
    pass