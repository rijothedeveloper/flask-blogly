"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import Post, db, connect_db, User
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.create_all()

@app.route("/")
def home_page():
    return redirect("/users")

@app.route("/users")
def showUsers():
    users = User.query.all()
    # import pdb
    # pdb.set_trace()
    return render_template("user-listing.html", users=users)

@app.route("/users/new", methods=["POST"])
def addUser():
    firstName = request.form["first-name"]
    lastName = request.form["last-name"]
    imgUrl = request.form["img-url"]
    user = User(first_name=firstName, last_name=lastName, image_url=imgUrl)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/new")
def add_user():
    return render_template("add-user-form.html")

@app.route("/users/<int:userId>")
def userDetails(userId):
    user = User.query.get(userId)
    posts = Post.query.filter(Post.id == userId).all()
    return render_template("user-detail.html", user=user, posts=posts)

@app.route("/users/<int:userId>/edit")
def editUser(userId):
    user = User.query.get(userId)
    return render_template("edit-user-form.html", user=user)

@app.route("/users/<int:userId>/edit", methods=["POST"])
def saveeditedUser(userId):
    firstName = request.form["first-name"]
    lastName = request.form["last-name"]
    imgUrl = request.form["img-url"]
    user = User.query.get(userId)
    user.first_name = firstName
    user.last_name = lastName
    user.image_url = imgUrl
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:userId>/delete")
def deleteUser(userId):
    User.query.filter_by(id=userId).delete()
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:userId>/posts/new")
def showNewPostForm(userId):
    return render_template("new-post-form.html", userId=userId)

@app.route("/users/<int:userId>/posts/new", methods=["POST"])
def addNewPost(userId):
    title = request.form["title"]
    content = request.form["content"]
    post = Post(title=title, content=content, created_at=datetime.datetime.now(), user_id=userId)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{userId}")