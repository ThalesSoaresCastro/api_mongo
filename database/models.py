from database.db import db
#from app import db 

class Video(db.Document):
    name = db.StringField(required=True, unique=False)
    theme = db.StringField(required=True, unique=False)
    like = db.IntField(required=False, unique=False, default=0)
    dislike = db.IntField(required=False, unique=False, default=0)