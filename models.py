"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.Text, nullable=False, default='https://www.pngitem.com/pimgs/m/30-307416_profile-icon-png-image-free-download-searchpng-employee.png')
    
    posts = db.relationship( 'Post', backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f"<User id={u.id} first-name={u.first_name} last-name={u.last_name}>"
    
    @property
    def full_name(self):
        """Returns the full name"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(255), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship( 'Tag', secondary='post_tags', backref='posts')

    def __repr__(self):
        u = self
        return f"<Post id={u.id} title={u.title} created-at={u.created_at}>"

    @property
    def formatted_date(self):
        """Formats the date."""
        return self.created_at.strftime("%A %B %d, %I:%M %p")
    
class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(255), nullable=False, unique=True)