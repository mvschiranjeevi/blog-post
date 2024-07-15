import unittest
from src import create_app, db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            "SECRET_KEY" :"dev",
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use an in-memory database for testing
            "SQL_TRACK_MODIFICATIONS" : False,
            "JWT_SECRET_KEY" :"JWT_SECRET_KEY",
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
