from flask import render_template
from app import app


# @app.route('/')
# @app.route('/index')
# def index():
    # return "Welcome to the Order"
'''

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'toasterkief'}
    return render_template('index.html', title='The Great Hall', user=user)


@app.route('/index-w-posts')
def index_posts():
    user = {'username': 'toasterkief'}
    posts = [
        {
            'author': {'username': 'Zodin'},
            'body': 'Lorem ipsum dolor sit amet, consectetur adipisic'
        },
        {
            'author': {'username': "Michael Landon"},
            'body': """"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed doeiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enimad minim """
        }
    ]
    return render_template('index_w_posts.html', title='Round Table', user=user, posts=posts)

'''



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'toasterkief'}
    posts = [
        {
            'author': {'username': 'Zodin'},
            'body': 'Come not between a nazgul and his prey...'
        },
        {
            'author': {'username': 'Michael Landon'},
            'body': 'But I will hinder thee as I may!'
        }
    ]
    return render_template('index.html', title='The Echo Halls', user=user, posts=posts)


