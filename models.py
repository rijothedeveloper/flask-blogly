"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """ connect to a database """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String,
                            nullable=False)

    last_name = db.Column(db.String,
                            nullable=False)

    image_url = db.Column(db.String,
                            default="")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def set_full_name(self, name):
        names = name.split()
        if len(names) > 1:
            self.first_name = names[0]
            self.last_name = names[1]

    def del_full_name(self):
        self.first_name = ""
        self.last_name = ""

    fullName = property(get_full_name, set_full_name, del_full_name, doc="full name of the person")

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.String,
                        nullable=False)

    content = db.Column(db.String,
                        nullable=False)

    created_at = db.Column(db.Date,
                            nullable=False)

    user_id = db.Column(db.Integer,
                            db.ForeignKey('users.id', ondelete="CASCADE"))

    
    

class Tag(db.Model):
    __tablename__ = "tags"
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    name = db.Column(db.String,
                     nullable=False)
    
    
    
class PostTag(db.Model):
    
    __tablename__ = "posttags"
    
    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id", ondelete="CASCADE"),
                        primary_key=True)
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id", ondelete="CASCADE"),
                       primary_key=True)
    
    