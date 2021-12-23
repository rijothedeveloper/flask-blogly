from unittest import TestCase
from app import app
from models import db, User, connect_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# connect_db(app)

db.drop_all()
db.create_all()

class test_app(TestCase):

    def setup(self):
        User.query.delete()


    def tearDown(self):
        db.session.rollback()
        User.query.delete()

    def test_list_users(self):
         with app.test_client() as client:
            res = client.get("/users")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            shouldContain = 'Users'
            self.assertIn(shouldContain, html)
            user = User(first_name="Rijo", last_name="George")
            db.session.add(user)
            db.session.commit()
            users = User.query.all()
            shouldContain = 'Rijo George'
            self.assertIn(shouldContain, users[0].fullName)

    def test_new_user_form(self):
        with app.test_client() as client:
            res = client.get("/users/new")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            shouldContain = '<button type="submit">Add</button>'
            self.assertIn(shouldContain, html)

    def test_edit_user_form(self):
        with app.test_client() as client:
            user = User(first_name="Rijo", last_name="George")
            db.session.add(user)
            db.session.commit()
            res = client.get("/users/1/edit")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            shouldContain = '<button type="submit">Save</button>'
            self.assertIn(shouldContain, html)

    def test_new_tag_form(self):
        with app.test_client() as client:
            res = client.get("/tags/new")
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            shouldContain = '<h1>Create a Tag</h1>'
            self.assertIn(shouldContain, html)