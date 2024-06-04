import pprint
import requests
import pytest

def test_post_v1_account():
    # Регистрация пользователя

    login = 'vadimko'
    email = f'{login}@mailforspam.com'
    password = 'kukusik'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    
    print(response.status_code)
    print(response.text)

    # Получить письма из почтового ящика

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)


    # Активация пользователя
    headers = {
    'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/ac493220-8731-4a0a-958c-83294aef455f', headers=headers)
    
    print(response.status_code)
    print(response.text)


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
    print(response.text)