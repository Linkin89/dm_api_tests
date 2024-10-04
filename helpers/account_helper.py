from json import loads
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry


def retry_if_result_none(result):
    return result is None

class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog_api: MailHogApi):
        """
        Inicialization
        """
        self.dm_account_api = dm_account_api
        self.mailhog_api = mailhog_api


    def register_mew_user(self, login: str, password: str, email: str):
        """
        Registration new user
        """

        json_data = {
        "login": login,
        "email": email,
        "password": password,
        }

        # Регистрация пользователя
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не создан {response.json()}"
               
        # Получение авторизационного токена из письма
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользвателя {login} не найден"

        # Активация пользователя 
        response = self.dm_account_api.account_api.put_v1_account_token(user_token=token)
        assert response.status_code == 200, "Пользователь не был активирован"
        return response


    def user_login(self, login: str, password: str, remember_me: bool = True):
        """
        Login user
        """

        json_data = {
        "login": login,
        "password": password,
        "rememberMe": remember_me,
        }
        
        # Авторизация пользователя
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Пользователь не смог авторизоваться"
        return response
    

    def change_email(self, login: str, password: str, email: str):
        """
        Change email
        """

        json_data = {
        "login": login,
        "password": password,
        "email": email,
        }

        # Изменение email
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, "Не удалось изменить email"

        # Получение писем из почты
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"

        # Получение токена для подтверждения нового email
        token = self.get_token_for_activate_new_email(email=email)
        assert token is not None, f"Токен для пользвателя {login} не найден"

        # Активация после смены email
        response = self.dm_account_api.account_api.put_v1_account_token(user_token=token)
        assert response.status_code == 200, "Пользователь не активирован"
        
        return response


    # Функция Получение токена для подтверждения нового email
    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_token_for_activate_new_email(self, email):
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        user_data = response.json()["items"]
        for item in user_data:

            if email in item["Raw"]["To"]:
                user_token = loads(item['Content']['Body'])['ConfirmationLinkUrl'].split("/")[-1]
                return user_token
        return None
            


    # Функция Получение токена для подтверждения email
    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login: str):
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        user_token = None
        for item in response.json()["items"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            if user_login == login:
                user_token = user_data["ConfirmationLinkUrl"].split("/")[-1]
        return user_token