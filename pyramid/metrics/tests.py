import unittest

from pyramid import testing
from metrics.views import metrics


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        request = testing.DummyRequest()
        info = metrics.metric(request)
        self.assertEqual(info['project'], 'metrics')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from metrics import main
        app = main({})

    def test_root(self):
        pass
