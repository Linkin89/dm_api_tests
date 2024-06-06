from json import loads
from time import sleep
from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from pprint import pprint


def test_put_v1_account_email():
    """
    Изменение email, активация нового email и авторизация с изменённым email
    """
    account_api = AccountApi(host="http://5.63.153.31:5051")
    login_api = LoginApi(host="http://5.63.153.31:5051")
    mailhog_api = MailhogApi(host="http://5.63.153.31:5025")

    login = "super_pupsik10"
    email = f"{login}edited@mailforspam.com"
    password = "kukusik"

    json_data = {
        "login": login,
        "email": email,
        "password": password,
    }

    # Изменение email
    change_email = account_api.put_v1_account_email(json_data)

    pprint(change_email.status_code)
    assert change_email.status_code == 200, "Не удалось изменить email"
    
    # Получение писем из почты
    response = mailhog_api.get_api_v2_messages()

    assert response.status_code == 200, "Письма не были получены"


    # Получение токена для подтверждения нового email
    user_data = response.json()["items"]
    user_token = get_token_for_activate_new_email(email, user_data)

    # Активация после смены email
    response = account_api.put_v1_account_token(user_token)

    print(response.status_code)
    assert response.status_code == 200, "Пользователь не активирован"

    # Авторизация после изменения email
    json_data = {
            "login": login,
            "password": password,
            "rememberMe": True,
        }

    response_after_change_email = login_api.post_v1_account_login(json_data)

    print(response_after_change_email.status_code)
    assert response_after_change_email.status_code == 200, "Авторизоваться не удалось"

# Получение токена для подтверждения нового email
def get_token_for_activate_new_email(email, user_data):
    for item in user_data:
        all_new_emais = item["Raw"]["To"]
        for new_email in all_new_emais  :
            if new_email == email:
                user_token = loads(item['Content']['Body'])['ConfirmationLinkUrl'].split("/")[-1]
                return user_token
