from .extensions import db
from datetime import datetime
import string
from random import choices


from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    # links = db.relationship('Link', backref='user', lazy=True)

    def __repr__(self):
        return f'User: <{self.username}>'




class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255))
    short_url = db.Column(db.String(20), unique=True)
    views =db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()
        
    def generate_short_link(self):
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits 
        short_url = ''.join(choices(characters, k=6))
        
        link = self.query.filter_by(short_url=short_url).first()
        
        if link:
            return self.generate_short_link()
        return short_url
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# class Link(db.Model):
#     __tablename__ = 'links'
#     id = db.Column(db.Integer, primary_key=True)
#     url = db.Column(db.String(255), nullable=False)
#     short_url = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     def __init__(self, url, short_url):
#         self.url = url
#         self.short_url = short_url
#         def __repr__(self):
#             return '<Link %r>' % self.url
        