import os
from sqlalchemy import Column, String, create_engine, Integer, Date
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Movies
have title and release date
'''

class Movies(db.Model):
    __tablename__ = "Movies"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    releaseDate = Column(Date)

    def __init__(self, title, releaseDate):
        self.title = title
        self.releaseDate = releaseDate

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'releaseDate': self.releaseDate
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

'''
Actors
have name, age, gender
'''

class Actors(db.Model):
    __tablename__ = "Actors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()