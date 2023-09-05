import re
import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError, BaseModel, EmailStr, validator
from typing import Optional, List
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from sqlalchemy.orm import declarative_base
from sqlalchemy import select

app = FastAPI(title='users')

# Создание соединения с базой данных
engine = create_engine('postgresql://postgres:89080620743@localhost:5432/postgres')
connection = engine.connect()
Base = declarative_base()
metadata = db.MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблицы
class User(Base):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    height = db.Column(db.Integer)
    shoe_size = db.Column(db.Integer)

class UserCreate(BaseModel):
    user_name: str
    password: str
    email: EmailStr
    height: int
    shoe_size: int
# Добавление валидации к UserCreate
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

# Создание таблиц вещей
class Clothes(Base):
    __tablename__ = 'clothes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(String)

class Shoes(Base):
    __tablename__ = 'shoes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(Integer)

class Hats(Base):
    __tablename__ = 'hats'

    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)
# Создание схем для чтения
class ClothesOut(BaseModel):
    id: int
    name: str
    size: str

class ShoesOut(BaseModel):
    id: int
    name: str
    size: int

class HatsOut(BaseModel):
    id: int
    name: str
# Создание нового пользователя в базе данных
@app.post('/users')
def create_user(user_create: UserCreate):
    insert_query = User.__table__.insert().values(
        user_name=user_create.user_name,
        password=user_create.password,
        email=user_create.email,
        height=user_create.height,
        shoe_size=user_create.shoe_size
    )
    connection.execute(insert_query)
    connection.commit()

    return {"status": 200, "success": True}

# Получение подключения к базе данных через FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Получение списка пользователей из базы данных
@app.get('/users', response_model=List[UserCreate])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(users).offset(skip).limit(limit).all()
    user_list = [UserCreate(user_name=user[1], password=user[2], email=user[3]) for user in result]
    return user_list
# Получение списка одежды из базы данных
@app.get('/clothes', response_model=List[ClothesOut])
async def get_clothes(size: Optional[str] = None, db: Session = Depends(get_db)):
    if size:
        clothes = db.query(Clothes).filter(Clothes.size == size).all()
    else:
        clothes = db.query(Clothes).all()
    return clothes
# Получение списка обуви из базы данных
@app.get('/shoes', response_model=List[ShoesOut])
async def get_shoes(size: Optional[int] = None, db: Session = Depends(get_db)):
    if size:
        shoes = db.query(Shoes).filter(Shoes.size == size).all()
    else:
        shoes = db.query(Shoes).all()
    return shoes
 # Получение списка головных уборов из базы данных
@app.get('/hats', response_model=List[HatsOut])
async def get_hats(db: Session = Depends(get_db)):
    hats = db.query(Hats).all()
    return hats
# Обработчик ошибок валидации данных
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    raise HTTPException(status_code=400, detail=str(exc.errors()))
# Проверка работы сессии базы данных
def check_db_session():
    db = SessionLocal()
    try:
        result = db.execute(select(1))
        print(f"Результат проверки сессии БД: {result.scalar()}")
        if result.scalar() == 1:
            print("Сессия БД работает исправно.")
        else:
            print("Могут быть проблемы с сессией БД.")
    except Exception as e:
        print(f"Ошибка при проверке сессии БД: {str(e)}")
    finally:
        db.close()

check_db_session()
