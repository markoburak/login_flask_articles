from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import Post
from . import db

admin_views = Blueprint('admin_views', __name__)

@admin_views.route('/admin_page', methods=['GET', 'POST'])
@login_required
def admin():
    posts = Post.query.all()
    if current_user.email != "admin@gmail.com":
         flash('You don\'t have a permission here', category='error')
    return render_template("admin.html", posts=posts, user=current_user)

@admin_views.route('/admin_page/posts/<int:post_id>')
@login_required
def get_post(post_id):
    postid = post_id
    post = Post.query.filter_by(id=postid).first()
    if not post:
        flash('Post does not exist', category='error')
        return redirect(url_for('admin_views.admin'))
    else:
        return render_template("admin_post_separate.html", post=post, user=current_user)

@admin_views.route('/admin_page/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    postid = post_id
    post = Post.query.filter_by(id=postid).first()
    if not post:
        flash('Post does not exist', category='error')
    elif current_user.email != "admin@gmail.com":
        flash('You don\'t have a permission to delete a post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash(f'Post {post.title} is deleted', category='success')

    return redirect(url_for('admin_views.admin'))

@admin_views.route('/admin_page/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')
        price = request.form.get('price')
        img_path_name = request.form.get('img_path_name')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            new_post = Post(title=title, text=text, price=price, img_path_name=img_path_name, author=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Posted!', category='success')

    return render_template("admin_create_post.html", user=current_user)

