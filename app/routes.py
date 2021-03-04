from app import app, db, mail, Message
from flask import render_template, request, flash, redirect, url_for
from app.forms import UserInfoForm, PostForm, LoginForm
from app.models import User, Post
from flask_login import login_user,logout_user, login_required, current_user
from werkzeug.security import check_password_hash

@app.route('/')
@app.route('/index')
def hello_world():
    context = {
        'title': 'Kekembas Blog | HOME',
        'posts': Post.query.all()
    }
    return render_template('index.html', **context)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    title = 'Kekambas Blog | REGISTER'
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username= form.username.data
        email= form.email.data
        password= form.password.data
        # print(username, email, password)
        # create a new instance of User
        new_user= User(username, email, password)
        # add new instance of our database
        db.session.add(new_user)
        # commit database
        db.session.commit()
        # Send email to new user
        msg= Message(f'Welcome, {username}', [email])
        msg.body = 'Thank you for signing up for the Kekembas blog. I hope you enjoy our app!'
        msg.html = '<p> Thank you so much for signing up for the Kekemnbas blog. I hope you enjoy our app </p>'
        # send email

        mail.send(msg)

        flash('Welcome aboard!', 'success')
        return redirect(url_for("hello_world"))
    return render_template('register.html', title = title, form=form)

@app.route('/createpost', methods = ['GET', 'POST'])
@login_required
def createposts():
    post = PostForm()
    title = 'Kekembas Blog | Create Post'
    if request.method =='POST' and post.validate():
        post_title = post.title.data
        content = post.content.data
        user_id = current_user.id
        # print(post_title, content)
        # create new post instance
        new_post = Post(post_title, content, user_id)
        # add new post instance to database
        db.session.add(new_post)
        # commit
        db.session.commit()
        # flash a message
        flash("You have blabla", "success")
        # redirect back to create post
        return redirect(url_for('createposts'))
    return render_template('create_post.html', post=post, title=title)

@app.route('/login', methods = ["GET", "POST"])
def login():
    title = 'Kekembas Blog | LOGIN'
    form= LoginForm()
    if request.method=="POST" and form.validate():
        username = form.username.data
        password= form.password.data
        user = User.query.filter_by(username= username).first()

        if user is None or not check_password_hash(user.password, password):
            flash("Incorrect Email/Password. Try again", "danger")
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in!", 'success')
        return redirect(url_for('hello_world'))

    return render_template('login.html', title=title, form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out!", 'primary')
    return redirect(url_for('hello_world'))

@app.route('/myinfo')
@login_required
def myinfo():
    title=" Kekambas | MY INFO "
    return render_template('myinfo.html', title= title)

@app.route('/myposts')
@login_required
def mypost():
    title = " Kekembas | MY POSTS "
    posts = current_user.posts
    return render_template('myposts.html', title=title, posts=posts)

@app.route('/myposts/<int:post_id>')
@login_required
def post_detail(post_id):
    post= Post.query.get_or_404(post_id)
    title=f'Kekambas Blog | {post.title.upper()}'
    return render_template('post_detail.html', title=title, post=post)

@app.route('/myposts/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    update_form = PostForm()
    if post.author.id != current_user.id:
        flash("You can't do this!", "danger")
        return redirect(url_for('myposts'))
    if request.method=='POST' and update_form.validate():

        post_title = update_form.title.data
        content = update_form.content.data

        post.title = post_title
        post.content = content

        db.session.commit()
        flash("You have changed your sh*t", 'info')
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('post_update.html', form=update_form, post=post)

@app.route('/myposts/delete/<int:post_id>', methods=["POST"])
@login_required
def post_delete(post_id):
    if post.author.id != current_user.id:
        flash("You can't do this!", "danger")
        return redirect(url_for('myposts'))
    post= Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("This post has been deleted", "info")
    return redirect(url_for('hello_world'))