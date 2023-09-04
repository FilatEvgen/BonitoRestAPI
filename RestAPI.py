import re
import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, Text
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError, BaseModel, EmailStr, validator

app = FastAPI(title='users')

# Создание соединения с базой данных
engine = create_engine('postgresql://postgres:89080620743@localhost:5432/postgres')
connection = engine.connect()

metadata = db.MetaData()

# Создание таблицы
users = db.Table('users', metadata,
    db.Column('user_id', db.Integer, primary_key=True),
    db.Column('user_name', db.Text),
    db.Column('password', db.Text),
    db.Column('email', db.Text)
    )
# создание таблицы в базе данных
metadata.create_all(engine)

class UserCreate(BaseModel):
    user_name: str
    password: str
    email: EmailStr

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
        email_regex = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        if not email_regex.match(value):
            raise ValueError('Некорректный адрес электронной почты')
        return value

@app.post('/users')
def create_user(user_create: UserCreate):
    # Проверка валидности данных
    try:
        user_create.validate(user_create.dict())
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e.errors()))

    # Вставка данных в таблицу
    insert_query = users.insert().values(user_name=user_create.user_name, password=user_create.password, email=user_create.email)
    connection.execute(insert_query)

    return {'status': 200, 'success': True}

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    raise HTTPException(status_code=400, detail=str(exc.errors()))