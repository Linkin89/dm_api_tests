from helpers.account_helper import AccountHelper
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from json import loads
from mimesis import Person


def test_put_v1_account_token():
    """
    Проверка авторизации пользователя до активации
    """
    mailhog_configuration = MailhogConfiguration(host="http://5.63.153.31:5025", disable_log=True)
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=True)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog_api=mailhog)

    fake = Person()
    login = fake.username()
    email = f"{login}@mailforspam.com"
    password = "kukusik"

    json_data = {
        "login": login,
        "email": email,
        "password": password,
    }

    # Регистрация пользователя
    response = account_helper.dm_account_api.account_api.post_v1_account(json_data=json_data)
    assert (response.status_code == 201), f"Пользователь с таким именем уже существует {response.json()}"

    # Получить письма из почтового ящика
    response = account_helper.mailhog_api.mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены"

    # Получение авторизационного токена
    user_token = account_helper.get_activation_token_by_login(login)
    assert user_token is not None, f"Токен для пользователя {login} не найден"

    # Попытка авторизации пользователя ДО АКТИВАЦИИ
    json_data = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = account_helper.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, "Пользователь смог авторизоваться без активации, АЛЯРМА!!!"

    # Активация пользователя
    response = account_helper.dm_account_api.account_api.put_v1_account_token(user_token=user_token)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация пользователя после активации
    response = account_helper.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"