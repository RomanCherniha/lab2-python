from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, session_local
from typing import Annotated
import models

app = FastAPI()#створити фаст апі instance 
models.base.metadata.create_all(bind=engine)#створити таблиці якщо вони ще не були створені

def db_conn(): #отримання доступу до бд
    db = session_local()
    try:
        yield db
        
    finally:
        db.close()

#обидві моделі від бібліотеки pydantic
class Book_Base(BaseModel): # модель таблиці книги, колонка: її тип даних
    tittle: str
    content: str
    author: str

class User_Base(BaseModel): # модель таблиці юзер, колонка: її тип даних
    username: str
    email: str
    age: int


db_dependecy = Annotated[Session, Depends(db_conn)] # залежність для конекту до бд, використовується у ендпоінтах фаст апі

# @app.method - ендпоінт у фаст апі

@app.post('/book/') #створення запису про книгу
async def create_book(book: Book_Base, db: db_dependecy):
    db_book = models.Book(**book.dict()) # ** - розпаковує вміст словника book конструктора models.Book
    db.add(db_book)
    db.commit() # підтверджує зміни в бд


@app.post('/users/') # створити запис про користувача
async def create_user(user: User_Base, db: db_dependecy):
    db_user = models.User(**user.dict()) # те саме тільки для юзера
    db.add(db_user)
    db.commit() 

@app.get('/book/{book_id}') #читання запису про книгу
async def read_book(book_id: int, db: db_dependecy):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail='Книгу не знайдено')
    return book


@app.get('/users/{user_id}') #прочитати записпо користувача
async def read_user(user_id: int, db: db_dependecy):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='Користувача не знайдено')
    return user


@app.delete('/book/{book_id}')#видалити запис про книгу
async def delete_book(book_id: int, db: db_dependecy):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail='Книгу не знайдено')
    db.delete(db_book)
    db.commit()


@app.delete('/user/{user_id}') #видали запис про користувача
async def delete_user(user_id: int, db: db_dependecy):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Запис не знайдено')
    db.delete(db_user)
    db.commit()


@app.put('/book/{book_id}') #оновити дані про запис
async def update_book(book_id: int, book:Book_Base, db: db_dependecy):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail='Запис не знайдено')
    db.query(models.Book).filter(models.Book.id == book_id).update(book.dict(), synchronize_session=False)
    db.commit()


@app.put('/user/{user_id}') #оновити дані про користувача
async def update_user(user_id: int, user:User_Base, db: db_dependecy):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Запис не знайдено')
    db.query(models.User).filter(models.User.id == user_id).update(user.dict(), synchronize_session=False)
    db.commit()

if __name__ == '__main__': #перевіряє чи скрипт запускається як основна програма чи імпортується як модуль(наприклад models би не пройшов цей if)
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=1)