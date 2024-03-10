from sqlalchemy import Column, String, Integer
from database import base


class Book(base): #модель таблиці книги
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, index=True)
    tittle = Column(String(255))
    content = Column(String(255))
    author = Column(String(255))

class User(base): #модель таблиці юзер
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    email = Column(String(255), unique=True)
    age = Column(Integer)
