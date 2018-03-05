from source.api import app
from unittest import TestCase
import json

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_register_business(self):
        