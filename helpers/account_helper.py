from json import loads
import time
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
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

        registration = Registration(
            login=login,
            password=password,
            email=email
            )

        # Регистрация пользователя
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не создан {response.json()}"
        
        # Получение авторизационного токена из письма
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, f"Время ожидания составило {end_time - start_time} секунд" 
        assert token is not None, f"Токен для пользвателя {login} не найден"

        # Активация пользователя 
        response = self.dm_account_api.account_api.put_v1_account_token(user_token=token)
        return response


    def user_login(self, login: str, password: str, remember_me: bool = True, validate_response=False, validate_headers=False):
        """
        Login user
        """

        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
            )
            
        
        # Авторизация пользователя
        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials, validate_response=validate_response)
        if validate_headers:
            assert response.headers["X-Dm-Auth-Token"], f"Токен для пользователя {login} не найден"
        return response
      
      
    def user_logout(self, token: str):
        """
        Logout user from single device
        """
        
        headers = {
            "X-Dm-Auth-Token": token
        }
        
        # Выход из аккаунта
        response = self.dm_account_api.login_api.delete_v1_account_login(headers=headers)
        assert response.status_code == 204, "Не удалось выйти из аккаунта"
        return response


    def user_logout_all(self, token: str):
        """
        Logout user from all devices
        """
        headers = {
            "X-Dm-Auth-Token": token
        }
        
        # Выход из всех аккаунтов
        response = self.dm_account_api.login_api.delete_v1_account_login_all(headers=headers)
        assert response.status_code == 204, "Не удалось выйти из аккаунта"
        return response


    def change_email(self, login: str, password: str, email: str):
        """
        Change email
        """

        change_email = ChangeEmail(
            login=login,
            password=password,
            email=email
        )

        # Изменение email
        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email, validate_response=False)
        assert response.status_code == 200, "Не удалось изменить email"

        # Получение писем из почты
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"

        # Получение токена для подтверждения нового email
        token = self.get_token_for_activate_new_email(email=email)

        # Активация после смены email
        response = self.dm_account_api.account_api.put_v1_account_token(user_token=token)
        return response
    
    
    def change_password(self, login: str, password: str, new_password: str, email: str):
        """
        Reset and change registered user password
        """
        
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        
        # Cброс пароля
        response = self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)        
        
        change_password = ChangePassword(
            login=login,
            token = self.get_token_for_reset_password(login),
            oldPassword=password,
            newPassword=new_password
        )
        
        headers = {
            "X-Dm-Auth-Token": self.get_authorization_token(login, password)
        }
        
        # Изменение пароля
        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password, headers=headers)
        return response
        
    
    def auth_client(self, login: str, password: str):
        """
        Authorized client
        """
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
