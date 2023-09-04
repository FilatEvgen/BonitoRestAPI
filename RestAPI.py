import re
import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, Text
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError, BaseModel, EmailStr, validator
from typing_extensions import List
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from sqlalchemy.orm import declarative_base

app = FastAPI(title='users'
    )

# Создание соединения с базой данных
engine = create_engine('postgresql://postgres:89080620743@localhost:5432/postgres')
connection = engine.connect()
Base = declarative_base()
metadata = db.MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Создание таблицы
users = db.Table('users1', metadata,
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
        email_regex = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+')
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
    print(user_create.user_name)
    print(user_create.password)
    print(user_create.email)
    connection.execute(insert_query)
    connection.commit()

    return {'status': 200, 'success': True}
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/users', response_model=List[UserCreate])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(users).offset(skip).limit(limit).all()
    user_list = [UserCreate(user_name=user[1], password=user[2], email=user[3]) for user in result]
    return user_list
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    raise HTTPException(status_code=400, detail=str(exc.errors()))
from sqlalchemy import select

from sqlalchemy import select

def check_db_session():
    db = SessionLocal()
    try:
        result = db.execute(select(1))
        print(f"Check DB session result: {result.scalar()}")
        if result.scalar() == 1:
            print("DB session is working fine.")
        else:
            print("There might be an issue with the DB session.")
    except Exception as e:
        print(f"Error while checking DB session: {str(e)}")
    finally:
        db.close()

# Call the function to check the session
check_db_session()


