from pydantic import  BaseModel
#Создание схемы для отправки данных с помощью POST-запроса
class ClothesCreate(BaseModel):
    name: str
    size: int
    image_url: str

class ShoesCreate(BaseModel):
    name: str
    size: int
    image_url: str

class HatsCreate(BaseModel):
    name: str
    image_url: str
class UserCreate(BaseModel):
    user_name: str
    password: str
    email: str
    height: int
    shoe_size: int

# Создание схем для чтения
class ClothesOut(BaseModel):
        id: int
        name: str
        size: str
        image_url: str

class ShoesOut(BaseModel):
        id: int
        name: str
        size: int
        image_url: str

class HatsOut(BaseModel):
        id: int
        name: str
        image_url: str