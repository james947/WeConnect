from source.api import app
from unittest import TestCase

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_users(self):
        response = self.app.get('http://127.0.0.1:5000/api/v1/users')
        self.assertEqual(response.status_code,404)

    def test_business(self):
        resposn