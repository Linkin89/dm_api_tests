from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from json import loads
from mimesis import Person

def test_post_v1_account_login():
    """
    Авторизация пользователя с валидными и не валидными логопасс
    """
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host="http://5.63.153.31:5025", disable_log=True)
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=True)

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    fake = Person()
    login = fake.username()
    email = f"{login}@mailforspam.com"
    password = "kukusik"

    json_data = {
        "login": login,
        "email": email,
        "password": password,
    }

    response = account_api.post_v1_account(json_data)
    assert (response.status_code == 201), f"Пользователь с таким именем уже существует {response.json()}"

    # Получить письма из почтового ящика

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены"

    # Получение авторизационного токена
    user_token = get_activation_token_by_login(login, response)

    assert user_token is not None, f"Токен для пользвателя {login} не найден"

    # Активация пользователя
    response = account_api.put_v1_account_token(user_token=user_token)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация пользователя с НЕвалидными логопасс
    json_data = {
        "login": login+"1",
        "password": password+"1",
        "rememberMe": True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 400, "Пользователь смог авторизоваться с НЕВАЛИДНЫМИ данными"

    # Авторизация пользователя с валидными логопасс
    json_data = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"


def get_activation_token_by_login(login, response):
    user_token = None
    for item in response.json()["items"]:
        user_data = loads(item["Content"]["Body"])
        user_login = user_data["Login"]

        if user_login == login:
            user_token = user_data["ConfirmationLinkUrl"].split("/")[-1]
    return user_token