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


    def register_new_user(self, login: str, password: str, email: str):
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
      
      
    def user_logout(self, login: str, password: str):
        """
        Logout user from single device
        """
    
        token = self.get_authorization_token(login, password)
        
        # Выход из аккаунта
        response = self.dm_account_api.login_api.delete_v1_account_login(token=token)
        assert response.status_code == 204, "Не удалось выйти из аккаунта"
        return response


    def user_logout_all(self, login: str, password: str):
        """
        Logout user from all devices
        """
    
        token = self.get_authorization_token(login, password)
        
        # Выход из всех аккаунтов
        response = self.dm_account_api.login_api.delete_v1_account_login_all(token=token)
        assert response.status_code == 204, "Не удалось выйти из аккаунта"
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
    
    
    def change_password(self, login: str, password: str, new_password: str, email: str):
        """
        Reset and change registered user password
        """
        
        json_data = {
        "login": login,
        "email": email,
        }
        
        # Cброс пароля
        response = self.dm_account_api.account_api.post_v1_account_password(json_data)
        assert response.status_code == 200, f"Не удалось сбросить пароль для пользователя {login}"
        
        json_data = {
        "login": login,
        "token": self.get_token_for_reset_password(login),
        "oldPassword": password,
        "newPassword": new_password,
        }
        
        headers = {
            "X-Dm-Auth-Token": self.get_authorization_token(login, password)
        }
        
        # Изменение пароля
        response = self.dm_account_api.account_api.put_v1_account_password(json_data=json_data, headers=headers)
        assert response.status_code == 200, "Не удалось изменить пароль"
        return response
        
    
    def auth_client(self, login: str, password: str):
        response = self.user_login(login=login, password=password)
        
        token = {
            "x-dm-auth-token": response.headers['X-Dm-Auth-Token']
        }
        
        # Установка хедера с токеном для авторизованного пользователя
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)
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
        for item in response.json()["items"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            if user_login == login and user_data.get("ConfirmationLinkUrl"):
                user_token = user_data["ConfirmationLinkUrl"].split("/")[-1]
                return user_token
            return None
            
    
    # Функция Получение авторизационного токена
    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_authorization_token(self, login: str, password: str):
        response = self.user_login(login=login, password=password)
        token = response.headers["X-Dm-Auth-Token"]
        return token

    
    # Функция Получение токена для сброса пароля
    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_token_for_reset_password(self, login: str):
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        for item in response.json()["items"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            if user_login == login and user_data.get("ConfirmationLinkUri"):
                token = user_data["ConfirmationLinkUri"].split("/")[-1]
                return token
            return None
