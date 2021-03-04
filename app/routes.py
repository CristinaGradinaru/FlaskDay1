from app import app, db, mail, Message
from flask import render_template, request, flash, redirect, url_for
from app.forms import UserInfoForm, PostForm, LoginForm
from app.models import User
from flask_login import login_user,logout_user, login_required
from werkzeug.security import check_password_hash

@app.route('/')
@app.route('/index')
def hello_world():
    context = {
        'title': 'Kekembas Blog | HOME',
        'customer_name': 'Cristina',
        'customer_username': 'cgradinaru',
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
        print(post_title, content)
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

