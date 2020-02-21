from app import db
from models import Post, Toolbelt, Project, Message

# create the database and the db table 
db.create_all()


# commit the changes
db.session.commit()



