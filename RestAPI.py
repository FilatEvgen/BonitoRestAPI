from fastapi import FastAPI
from typing import List, Optional
from pydantic import Field,BaseModel
from enum import Enum
from datetime import datetime
app = FastAPI()

# @app.get('/')
# def hello():
#     return 'Hello World'
#
# print('Hello world')
#
app = FastAPI(
        title='Trading APP'
)



# база данных(массив из строк)
fake_users = [
    {'id': 1, 'role': 'admin','name':'Bob'},
    {'id': 2, 'role': 'Investor','name':'John'},
    {'id': 3, 'role': 'trader','name':'Matt'},
    {'id': 4, 'role': 'Investor','name':'Homer','degree': [
        {'id': 1,'created_at': '2023-09-02T00:00:00','type_degree':'expert'}
    ]},
]

class DegreeType (Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree:DegreeType

class User(BaseModel):
    id:int
    role: str
    name:str
    degree:Optional[List[Degree]] = []
# Получения данных о конкретном пользователе(параметры пути)
@app.get('/users/{user_id}',response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id')==user_id]

# БД
fake_trades = [
    {'id':1,'user_id':1,'currency': 'BTC','side':'buy','price':123,'amount':2.12},
    {'id':2,'user_id':1,'currency': 'BTC','side':'sell','price':125,'amount':2.12},
]
# Валидация данных которые нам отправляет пользователь( в строке Price мы выдаем ошибку если число отрицательное)
class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}

