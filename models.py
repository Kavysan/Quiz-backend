from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from sqlalchemy.orm import relationship


db=SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True, unique = True, default=get_uuid)
    name = db.Column(db.String(150), default='')
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False) 
    phone = db.Column(db.String, nullable = False) 
    results = relationship('Results', back_populates='user')
    
    # token = db.Column(db.String, default = '', unique = True )
    
class Results(db.Model):
    __tablename__ = "results"
    id = db.Column(db.String, primary_key=True, unique = True, default=get_uuid)
    total = db.Column(db.Integer, nullable=False)
    questions = db.Column(db.Integer, nullable=False)
    attend = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    quiz_result= db.Column(db.String(10))
    user_email = db.Column(db.String(150), db.ForeignKey('users.email'), nullable=False)
    user = relationship('User', back_populates='results')
    
    
    