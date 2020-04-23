"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:41361@localhost/blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

db.drop_all()
db.create_all()

@app.route("/")
def home():
    """Redirect to users list"""
    return redirect("/users")

@app.route("/users/")
def list_users():
    """List users"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/new", methods=['GET', 'POST'])
def add_user():
    """Add user and redirect to user list"""
    if request.method == 'GET':
        return render_template("add-user.html")
    else:
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        image_url = request.form['image-url'] if request.form['image-url'] else None

        if first_name and last_name:
            user = User(first_name=first_name, last_name=last_name, image_url=image_url)
            db.session.add(user)
            db.session.commit()

            return redirect("/users")
        else:
            flash('Name fields cannot be blank')
            return render_template("add-user.html")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("user.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit info of a single user"""
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return render_template("edit-user.html", user=user)
    else:
        user.first_name = request.form['first-name']
        user.last_name = request.form['last-name']
        user.image_url = request.form['image-url'] if request.form['image-url'] else None

        if first_name and last_name:
            user = User(first_name=first_name, last_name=last_name, image_url=image_url)
            db.session.add(user)
            db.session.commit()

            return redirect("/users")
        else:
            flash('Name fields cannot be blank')
            return render_template("edit-user.html")

@app.route("/users/<int:user_id>/posts/new", methods=['GET', 'POST'])
def add_post(user_id):
    """Show add a post form and handle post submission"""
    user = User.query.get_or_404(user_id)
    #import pdb
    #pdb.set_trace()
    if request.method == 'GET':
        return render_template("add-post.html", user=user)
    else:
        title = request.form['title']
        content = request.form['content']

        if title and content:
            post = Post(title=title, content=content, user_id=user_id)

            db.session.add(post)
            db.session.commit()

            return redirect(f"/users/{user_id}")
        else:
            flash('Title and content cannot be blank')
            return render_template("add-post.html", user=user)

@app.route("/posts/<int:post_id>/edit", methods=['GET', 'POST'])
def edit_post(post_id):
    """Show edit a post form and handle editing post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    #import pdb
    #pdb.set_trace()
    if request.method == 'GET':
        return render_template("edit-post.html", user=user, post=post)
    else:
        title = request.form['title']
        content = request.form['content']

        if title and content:
            post = Post(title=title, content=content, user_id=user_id)

            db.session.add(post)
            db.session.commit()

            return redirect(f"/posts/{post_id}")
        else:
            flash('Title and content cannot be blank')
            return render_template("edit-post.html", user=user, post=post)

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show info on a single post."""
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template("post.html", user=user, post=post)

@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    """Delete the user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")

@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    """Delete the post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")