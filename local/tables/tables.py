import sqlalchemy as db
from sqlalchemy import Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()
# cоздание таблиц вещей
class Clothes(Base):
    __tablename__ = 'clothes'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.Text)
    size = db.Column(db.Text)
    image_url =db. Column(db.Text)

class Shoes(Base):
    __tablename__ = 'shoes'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.Text)
    size = db.Column(db.Integer)
    image_url = db.Column(db.Text)
class Hats(Base):
    __tablename__ = 'hats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    image_url = db.Column(db.Text)



# Создание таблицы
class User(Base):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    height = db.Column(db.Integer)
    shoe_size = db.Column(db.Integer)