from unittest import TestCase
from app import app
from models import db, User


class test_user(TestCase):

    def test_full_name(self):
        user = User(first_name="Rijo", last_name="George")
        self.assertEqual(user.fullName, "Rijo George")