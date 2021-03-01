from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def hello_world():
    context = {
        'title': 'Kekembas Blog | HOME',
        'customer_name': 'Cristina',
        'customer_username': 'cgradinaru',
        'items': {
            1: 'ice cream',
            2: 'lemons',
            3: 'cereal',
            4: 'bread',
            5: 'apples'
        }
    }
    return render_template('index.html', **context)

@app.route('/register')
def register():
    title = 'Kekambas Blog | REGISTER'
    return render_template('register.html', title = title)