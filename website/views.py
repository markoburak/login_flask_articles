from flask import Blueprint, render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Post, User
from . import db
import os

views = Blueprint('views', __name__)

img = os.path.join('static', 'images/posts/')

@views.route('/')
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts, user=current_user)

@views.route('/user_profile', methods=['GET','POST'])
@login_required
def user_profile():
    if request.method == "POST":
        new_email = request.form.get('email')
        new_name = request.form.get('firstName')
        if not new_email or not new_name:
            flash('User email or name cannot be empty', category='error')
        else:
            user_to_update = User.query.filter_by(email=new_email).first()
            user_to_update.email = new_email
            user_to_update.first_name = new_name
            db.session.commit()
            flash('Updated!', category='success')
    
    return render_template("user_profile.html", user=current_user)


@views.route('/posts/<int:post_id>')
def get_page(post_id):
    postid = post_id
    post = Post.query.get(postid)
    return render_template("post_separate.html", post=post, user=current_user)

