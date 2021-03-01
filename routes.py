from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def hello_world():
    title = "kekembas blog | HOME" 
    return render_template('base.html', title=title)

@app.route('/register')
def register():
    title = 'Kekambas Blog | REGISTER'
    return render_template('register.html', title = title)