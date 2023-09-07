import re
import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError, BaseModel, EmailStr, validator
from typing import Optional, List
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from fastapi import Depends
from sqlalchemy import select
from pydantic import HttpUrl
from local.tables import tables
from local.repositories import dbrepository
from api.routes import apiroutes
from api.models.apimodels import UserCreate,ClothesCreate,ShoesCreate,HatsCreate, ShoesOut,ClothesOut,HatsOut
app = FastAPI(title='users')
# Валидация данных(проверка на корректность ввода)
@validator('user_name')
def validate_user_name(cls, value):
    if len(value) < 3:
        raise ValueError('Имя пользователя должно содержать не менее 3 символов')
    return value

@validator('password')
def validate_password(cls, value):
    if len(value) < 5:
        raise ValueError('Пароль должен содержать не менее 5 символов')
    if not any(char.isdigit() for char in value):
        raise ValueError('Пароль должен содержать хотя бы одну цифру')
    if not any(char.isupper() for char in value):
        raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
    return value

@validator('email')
def validate_email(cls, value):
        email_regex = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+')
        if not email_regex.match(value):
            raise ValueError('Некорректный адрес электронной почты')
        return value

# Валидаторы для height и shoe_size проверка на положительное значение
@validator('height')
def validate_height(cls, value):
    if value <= 0:
        raise ValueError('Рост должен быть положительным числом')
    return value
# проверка на положительное значение
@validator('shoe_size')
def validate_shoe_size(cls, value):
    if value <= 0:
        raise ValueError('Размер обуви должен быть положительным числом')
    return value
# POST-эндпоинты для создания записей в таблицах одежды, обуви и головных уборов
@app.post('/users')
def create_user(user_create: UserCreate):
    return dbrepository.insert_user(user_create)
@app.post("/clothes")
async def create_clothes(clothes_create:ClothesCreate):
    return dbrepository.insert_clothes(clothes_create)
@app.post("/shoes")
async def create_shoes(shoes_create: ShoesCreate):
    responce = await dbrepository.insert_shoes(shoes_create)
    return jsonable_encoder(response)
@app.post("/hats")
async def create_hats(hats_create:HatsCreate):
    responce = await dbrepository.insert_hats(hats_create)
    return jsonable_encoder(response)

# Получение списка пользователей из базы данных
@app.get('/users', response_model=List[UserCreate])
def get_users(skip: int = 0, limit: int = 10):
    return dbrepository.get_user(skip, limit)

# Получение списка одежды из базы данных
@app.get('/clothes', response_model=List[ClothesOut])
async def get_clothes(size: Optional[str] = None):
    responce = await dbrepository.get_cloth(create_clothes)
    return jsonable_encoder(response)

# Получение списка обуви из базы данных
@app.get('/shoes', response_model=List[ShoesOut])
async def get_shoes(size: Optional[int] = None):
    responce = await dbrepository.get_shoe(create_shoes)
    return jsonable_encoder(response)

# Получение списка головных уборов из базы данных
@app.get('/hats', response_model=List[HatsOut])
async def get_hats():
    responce = await dbrepository.get_hat(create_hats)
    return jsonable_encoder(response)


# Обработчик ошибок валидации данных
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    raise HTTPException(status_code=400, detail=str(exc.errors()))


# dbrepository.check_db_session()
