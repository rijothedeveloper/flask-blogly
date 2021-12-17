"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    return render_template("user-detail.html", user=user)

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
