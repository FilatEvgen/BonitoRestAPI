from fastapi import FastAPI

app = FastAPI(
        title='Trading APP'
)
# база данных(массив из строк)
fake_users = [
    {'id': 1, 'role': 'admin','name':'Bob'},
    {'id': 2, 'role': 'Investor','name':'John'},
    {'id': 3, 'role': 'trader','name':'Matt'},
]

# Получения данных о конкретном пользователе(параметры пути)
@app.get('/users/{user_id}')
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id')==user_id]

# БД
fake_trades = [
    {'id':1,'user_id':1,'currency': 'BTC','side':'buy','price':123,'amount':2.12},
    {'id':2,'user_id':1,'currency': 'BTC','side':'sell','price':125,'amount':2.12},
]
# Лимиторванные параметры запроса(ограничен список сделок)
@app.get('/traders')
def get_traders(limit: int= 1,offset: int=0):
    return fake_trades[offset:][:limit]

# комбинирование запросов
# бд
fake_users2 = [
    {'id': 1, 'role': 'admin','name':'Bob'},
    {'id': 2, 'role': 'Investor','name':'John'},
    {'id': 3, 'role': 'trader','name':'Matt'},
]

#запрос пользователя на смену имени и ответ ему
@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get('id')==user_id, fake_users2))[0]
    current_user['name']= new_name
    return {'status':200,'data': current_user}


