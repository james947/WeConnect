from source.api import app
from unittest import TestCase

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_users(self):
        response = self.app.get('http://127.0.0.1:5000/api/v1/users')
        self.assertEqual(response.status_code,200)

    def test_business(self):
        response=self.app.post('http://127.0.0.1:5000/api/auth/v1/register')
        self.assertEqual(response.status_code,201)

    def test_login(self):
        response= self.app.post('http://127.0.0.1:5000/api/auth/v1/login')
        self.assertEqual(response.status_code,201)

    def test_return_all_business(self):
        response =self.app.get('http://127.0.0.1:5000/api/v1/business')
        self.assertEqual(response.status_code,200)
