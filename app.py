"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import Post, PostTag, Tag, db, connect_db, User
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
    tags = Tag.query.all()
    return render_template("new-post-form.html", userId=userId, tags=tags)

@app.route("/users/<int:userId>/posts/new", methods=["POST"])
def addNewPost(userId):
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")
    post = Post(title=title, content=content, created_at=datetime.datetime.now(), user_id=userId)
    db.session.add(post)
    db.session.commit()
    for tag in tags:
        tagObj = Tag.query.filter(Tag.name==tag).one()
        postTag = PostTag(post_id=post.id, tag_id=tagObj.id)
        db.session.add(postTag)
        db.session.commit()
    return redirect(f"/users/{userId}")

@app.route("/posts/<int:postId>")
def showPostDetail(postId):
    post = Post.query.filter(Post.id == postId).one()
    user = User.query.get(post.user_id)
    postTags = PostTag.query.filter(PostTag.post_id==post.id).all() 
    tags=[]
    for postTag in postTags:
        tag = Tag.query.get(postTag.tag_id)
        tags.append(tag)
    return render_template("post-detail.html", post=post, user=user, tags=tags)

@app.route("/posts/<int:postId>/edit")
def showPostEditForm(postId):
    tags = Tag.query.all()
    return render_template("edit-post-form.html", postId=postId, tags=tags)

@app.route("/posts/<int:postId>/edit", methods=["POST"])
def saveEditedPost(postId):
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")
    post = Post.query.get(postId)
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    PostTag.query.filter(PostTag.post_id==post.id).delete()
    db.session.commit()
    for tag in tags:
        tagObj = Tag.query.filter(Tag.name==tag).one()
        postTag = PostTag(post_id=post.id, tag_id=tagObj.id)
        db.session.add(postTag)
        db.session.commit()
    return redirect(f"/posts/{postId}")

@app.route("/posts/<int:postId>/delete")
def deletePost(postId):
    id = db.session.query(Post.user_id).filter(Post.id==postId).first()
    userId = id[0]
    Post.query.filter(Post.id==postId).delete()
    db.session.commit()
    url = f"/users/{userId}"
    return redirect(f"/users/{userId}")

@app.route("/tags")
def listTags():
    tags = Tag.query.all()
    return render_template("tag-listing.html",tags=tags)

@app.route("/tags/<int:tagId>")
def get_tag_details(tagId):
    tag = Tag.query.get(tagId)
    posts = tag.posts_for_tag
    return render_template("tag-details.html", posts=posts, tagId=tagId)

@app.route("/tags/new")
def showAddTagForm():
    return render_template("new-tag-form.html")

@app.route("/tags/new", methods=["POST"] )
def addNewTag():
    name = request.form["name"]
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tagId>/edit")
def showEditTagForm(tagId):
    return render_template("edit-tag-form.html", tagId=tagId)

@app.route("/tags/<int:tagId>/edit", methods=["POST"] )
def editTag(tagId):
    name = request.form["name"]
    tag = Tag.query.get(tagId)
    tag.name = name
    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tags/{tagId}")

@app.route("/tags/<int:tagId>/delete")
def deleteTag(tagId):
    Tag.query.get(tagId).delete()
    db.session.commit()
    return redirect("/tags")