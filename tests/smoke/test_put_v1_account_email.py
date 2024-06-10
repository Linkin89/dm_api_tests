from json import loads
from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from mimesis import Person


def test_put_v1_account_email():
    """
    Регистрация нового пользователя, активация и авторизация.
    Изменение email, активация нового email и авторизация с изменённым email
    """
    fake = Person()
    account_api = AccountApi(host="http://5.63.153.31:5051")
    login_api = LoginApi(host="http://5.63.153.31:5051")
    mailhog_api = MailhogApi(host="http://5.63.153.31:5025")

    login = fake.username()
    email = f"{login}edited@mailforspam.com"
    password = "kukusik"

    json_data = {
        "login": login,
        "email": email,
        "password": password,
    }
    response = account_api.post_v1_account(json_data)
    assert response.status_code == 201, f"Пользователь не создан {response.json()}"

    # Получить письма из почтового ящика
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены"

    # Получение авторизационного токена
    user_token = get_activation_token_by_login(login, response)
    assert user_token is not None, f"Токен для пользвателя {login} не найден"

    # Активация пользователя
    response = account_api.put_v1_account_token(user_token)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация пользователя
    json_authorizatin_data = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = login_api.post_v1_account_login(json_authorizatin_data)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    # Изменение email
    change_email = account_api.put_v1_account_email(json_data)
    assert change_email.status_code == 200, "Не удалось изменить email"

    # Получение писем из почты
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены"

    # Получение токена для подтверждения нового email
    user_data = response.json()["items"]
    user_token = get_token_for_activate_new_email(email, user_data)

    # Активация после смены email
    response = account_api.put_v1_account_token(user_token)
    assert response.status_code == 200, "Пользователь не активирован"

    # Авторизация после изменения email
    response_after_change_email = login_api.post_v1_account_login(json_data)
    assert response_after_change_email.status_code == 200, "Авторизоваться не удалось"


# Получение токена для подтверждения нового email
def get_token_for_activate_new_email(email, user_data):
    for item in user_data:
        if email in item["Raw"]["To"]:
            user_token = loads(item['Content']['Body'])['ConfirmationLinkUrl'].split("/")[-1]
            return user_token


# Получение токена для подтверждения email
def get_activation_token_by_login(login, response):
    user_token = None
    for item in response.json()["items"]:
        user_data = loads(item["Content"]["Body"])
        user_login = user_data["Login"]
        if user_login == login:
            user_token = user_data["ConfirmationLinkUrl"].split("/")[-1]
    return user_token
