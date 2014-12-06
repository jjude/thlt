"""
    Unit Tests
    ~~~~~~~~~~

    Define TestCase as base class for unit tests.
    Ref: http://packages.python.org/Flask-Testing/
"""
from flask import current_app as app
from flask.ext.testing import TestCase as Base
from thlt import create_app
from thlt.base import User, Site, Entry
from thlt.config import TestConfig
from thlt.extensions import db
import os

class TestCase(Base):
    """Base TestClass for your application."""

    @classmethod
    def setUpClass(cls):
        token_for_testing = 0
        base_dir = ''

    @classmethod
    def tearDownClass(cls):
        import shutil
        try:
            base_dir = getattr(cls, 'base_dir')
        except AttributeError:
            base_dir = None

        print '***********in teardown %s' % base_dir
        if base_dir:
            if os.path.exists(cls.base_dir):
                shutil.rmtree(cls.base_dir)
                os.unlink(os.path.join(cls.base_dir, '..', 'test.db'))

    def create_app(self):
        """
        Create and return a testing flask app.
        Required method for flask-testing extension
        """
        app = create_app(TestConfig)
        return app

    def setUp(self):
        pass

    def tearDown(self):
        """ this is called after EVERY test """
        pass

    def _test_get_request(self, endpoint, template = None):
        response = self.client.get(endpoint)
        self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response

    def _test_get_404(self, endpoint, template = None):
        response = self.client.get(endpoint)
        self.assert_404(response)
        return response


if __name__ == '__main__':
    unittest.main()