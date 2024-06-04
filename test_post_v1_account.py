import pprint
import requests
import pytest
from json import loads


def test_post_v1_account():
    # Регистрация пользователя

    login = 'vadimko2'
    email = f'{login}@mailforspam.com'
    password = 'kukusik'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    
    print(response.status_code)
    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    # Получить письма из почтового ящика

    params = {
        'limit': '5',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    assert response.status_code == 200, "Письма не были получены"

    # Получение авторизационного токена
    user_token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']

        if user_login == login:
            user_token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(user_login, user_token)
    assert user_token is not None, f"Токен для пользвателя {user_login} не найден"

    # Активация пользователя
    headers = {
    'accept': 'text/plain',
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{user_token}', headers=headers)
    
    print(response.status_code)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация пользователя
    headers = {
    'accept': 'text/plain',
    'Content-Type': 'application/json',
    }

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', headers=headers, json=json_data)

    print(response.status_code)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"