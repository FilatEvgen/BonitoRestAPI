import sqlalchemy as db,select
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from typing import Optional, List
from fastapi import Depends
from local.tables.tables import User,Clothes,Shoes,Hats
from sqlalchemy import create_engine
from api.models.apimodels import UserCreate,ClothesCreate,ShoesCreate,HatsCreate, ShoesOut,ClothesOut,HatsOut
from contextlib import contextmanager


engine = create_engine('postgresql://postgres:89080620743@localhost:5432/postgres')
connection = engine.connect()
metadata = db.MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = Session()
Base = declarative_base()
Base.metadata.create_all(engine)

# Получение данных с помощью FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_user(user_create: UserCreate):
    insert_query = User.__table__.insert().values(
        user_name=user_create.user_name,
        password=user_create.password,
        email=user_create.email,
        height=user_create.height,
        shoe_size=user_create.shoe_size
    )
    connection.execute(insert_query)
    connection.commit()
    return  {"status": 200, "success": True}
# Добавление в БД одежды
def insert_clothes(clothes_create: ClothesCreate):
    insert_query = Clothes.__table__.insert().values(name=clothes_create.name, size=clothes_create.size, image_url=clothes_create.image_url)
    connection.execute(insert_query)
    connection.commit()
    return clothes_create
# Добавление в БД обуви
def insert_shoes(shoes_create: ShoesCreate):
    insert_query = Shoes.__table__.insert().values(name=shoes_create.name, size=shoes_create.size, image_url=shoes_create.image_url)
    connection.execute(insert_query)
    connection.commit()
    return shoes_create
#Добавление в БД головных уборов
def insert_hats(hats_create: HatsCreate):
    insert_query = Hats.__table__.insert().values(name=hats_create.name, size=hats_create.size, image_url=hats_create.image_url)
    connection.execute(insert_query)
    connection.commit()
    return hats_create
# Получение списка пользователей из базы данных
def get_user(skip: int = 0, limit: int = 10):
    result = SessionLocal.query(User).all()
    SessionLocal.close()
    return   result.index(0)
    # insert_query = User.__table__.
    # db: Session = Depends(get_db)
    # result = db.query(User).offset(skip).limit(limit).all()
    # user_list = [UserCreate(user_name=user[1], password=user[2], email=user[3]) for user in result]
    # return user_list
# Получение списка одежды из базы данных
def get_cloth(size: Optional[str] = None):
    db: Session = Depends(get_db)
    if size:
        clothes = db.query(Clothes).filter(Clothes.size == size).all()
    else:
        clothes = db.query(Clothes).all()
    return clothes

# Получение списка обуви из базы данных
def get_shoe(size: Optional[int] = None):
    db: Session = Depends(get_db)
    if size:
        shoes = db.query(Shoes).filter(Shoes.size == size).all()
    else:
        shoes = db.query(Shoes).all()
    return shoes

# Получение списка головных уборов из базы данных
def get_hat():
    db: Session = Depends(get_db)
    hats = db.query(Hats).all()
    return hats
# Проверка работы сессии базы данных
# def check_db_session():
#     db = SessionLocal()
#     try:
#         result = db.execute(select(1))
#         print(f"Результат проверки сессии БД: {result.scalar()}")
#         if result.scalar() == 1:
#             print("Сессия БД работает исправно.")
#         else:
#             print("Могут быть проблемы с сессией БД.")
#     except Exception as e:
#         print(f"Ошибка при проверке сессии БД: {str(e)}")
#     finally:
#         db.close()