from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id=db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(80), unique=True,nullable= False)
    email = db.Column(db.String(120), unique=True,nullable= False)
    password = db.Column(db.Text(),nullable= False)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    posts = db.relationship('Posts', backref="user")

    def __repr__(self) -> str:
        return 'User>>> {self.username}'

class Posts(db.Model):
    id=db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())


    def __repr__(self) -> str:
        return 'Posts>>> {self.title}'