#Imports 
import os
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from smtp_utils import deliver_mail 

#Get app directory 
basedir = os.path.abspath(os.path.dirname(__file__))

#Configuration
SECRET_KEY = 'monolith'
USERNAME = 'admin'
PASSWORD = 'admin'
DEV_MAIL = 'michael.landon@zodin.dev'

# Database config
SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(basedir, "zodin.db")}'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False



# create app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import models


# Login required decorator function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in.')
            return jsonify({'status': 0, 'message': 'Please log in.'}), 401
        return f(*args, **kwargs)
    return decorated_function


# App routes
@app.route('/')
def index():
    """Render the cover page, as well as all microblog entries by myself."""
    entries = db.session.query(models.Post)
    return render_template('index.html', entries=entries)

@app.route('/philosophy')
def zodin_way():
    """Render a more indepth biographical page."""
    return render_template('zodin_way.html')


@app.route('/skillset')
def skill_page():
    """Render a portfolio of my current capabilities and abilities as a developer."""
    tools = db.session.query(models.Toolbelt)
    return render_template('toolbelt.html', tools=tools)

@app.route('/projects')
def projects():
    """Render a page with current projects and ideas"""
    projects = db.session.query(models.Project)
    return render_template('projects.html', projects=projects)




@app.route('/add', methods=['POST'])
@login_required
def add_entry():
    """Adds a new post to db to be displayed in index page."""
    
    new_entry = models.Post(request.form['title'], request.form['text'], datetime.now().ctime())
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted.')
    return redirect(url_for('index'))

@app.route('/update-skills', methods=['POST'])
@login_required
def update_skills():
    """Add a new skill for the portfolio."""
    new_entry = models.Toolbelt(request.form['title'], request.form['category'], request.form['about'], request.form['frameworks'])
    db.session.add(new_entry)
    db.session.commit()
    flash('Skills successfully updated.')
    return redirect(url_for('skill_page'))

@app.route('/new-project', methods=['POST'])
@login_required
def new_project():
    """Add a new project or development to the projects page."""
    new_entry = models.Project(request.form['title'], request.form['category'], request.form['about'], request.form['libraries'], request.form['github'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New project successfully added to portfolio.')
    return redirect(url_for('projects'))


@app.route('/admin', methods=['GET', 'POST'])
def login():
    """Admin login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Admin not found.'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password.'
        else:
            session['logged_in'] = True
            flash('Logged in as admin')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """Admin logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('Admin logged out.')
    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>', methods=['GET'])
@login_required
def delete_entry(post_id):
    """Deletes post from database"""
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Post).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Post Deleted"}
        flash('Entry deleted from database.')

    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)

@app.route('/delete-skill/<int:skill_id>', methods=['GET'])
@login_required
def delete_skill(skill_id):
    """Deletes skill from portfolio."""
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = skill_id
        db.session.query(models.Toolbelt).filter_by(skill_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Skill Deleted"}
        flash('Skill deleted from portfolio.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Form based contact page that will show up in my email inbox."""
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        body_text = request.form['body']

        message = models.Message(name, email, phone, subject, body_text, datetime.now().ctime())
        db.session.add(message)
        db.session.commit()
        deliver_mail(message)
        flash('Your message will be promptly delivered! Thank you for your time!')
        return(url_for('index'))
    return render_template('contact.html', error=error)


id __name__ == '__main__':
    app.run()


