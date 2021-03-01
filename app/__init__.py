from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def hello_world():
    title = "kekembas blog" 
    return render_template('base.html', title=title)