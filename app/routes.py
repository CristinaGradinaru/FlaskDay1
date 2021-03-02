from app import app
from flask import render_template, request
from app.forms import UserInfoForm, PostForm

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
        print(username, email, password)
        print('Welcome aboard!')
    return render_template('register.html', title = title, form=form)

@app.route('/createpost', methods = ['GET', 'POST'])
def createposts():
    post = PostForm()
    title = 'Kekembas Blog | Create Post'
    if request.method =='POST' and post.validate():
        post_title = post.title.data
        content = post.content.data
        print(post_title, content)
    return render_template('create_post.html', post=post, title=title)