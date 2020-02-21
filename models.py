from app import db


class Post(db.Model):

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, title, text, date):
        self.title = title
        self.text = text 
        self.date = date 


    def __repr__(self):
        return f'<title {self.body}>'

class Toolbelt(db.Model):
    __tablename__ = 'skills'

    skill_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    about = db.Column(db.Text, nullable=False)
    frameworks = db.Column(db.String, nullable=True)

    def __init__(self, title, category, about, frameworks):
        self.title = title
        self.category = category
        self.about = about
        self.frameworks = frameworks

    def __repr__(self):
        return f'<{self.title}\n-----------\n{self.category}\n{self.frameworks}\n\n-----------\n{self.about}>'


class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    about = db.Column(db.Text, nullable=False)
    libraries = db.Column(db.Text, nullable=True)
    github = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime, nullable=True)

    def __init__(self, title, category, about, libraries, github, date):
        self.title = title
        self.category = category
        self.about = about
        self.libraries = libraries
        self.github = github
        self.date = date 

    def __repr__(self):
        return f'<{self.title}\n----------\n{self.category}\n{self.github}\n\n{self.about}>'


