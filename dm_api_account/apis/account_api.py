from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient
import allure

class AccountApi(RestClient):
    # @allure.step("Регистрация пользователя")
    def post_v1_account(self, registration: Registration):
        """
        Register new user

        Args:
            json_data (json)
        """
        response = self.post(path=f"/v1/account", json=registration.model_dump(exclude_none=True, by_alias=True))
        return response

    # @allure.step("Активация пользователя")
    def put_v1_account_token(self, user_token, validate_response=True):
        """
        Activate registered user

        Args:
            user_token (str)
        """

        response = self.put(path=f"/v1/account/{user_token}")
        
        if validate_response:
            return UserEnvelope(**response.json())
            
        return response


    @allure.step("Изменение почты")
    def put_v1_account_email(self, change_email: ChangeEmail, validate_response=True):
        """
        Change registered user email

        Args:
            json_data (json)
        """
        response = self.put(path=f"/v1/account/email", json=change_email.model_dump(exclude_none=True, by_alias=True))
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    
    @allure.step("Получение данных пользователя")
    def get_v1_account(self, validate_response=True, **kwargs):
        """
        Get current user

        Args:
            json_data (json)
        """
        response = self.get(path=f"/v1/account", **kwargs)
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response
    
    
    @allure.step("Сброс пароля")
    def post_v1_account_password(self, reset_password: ResetPassword):
        """
        Reset registered user password
        """
        
        response = self.post(path=f"/v1/account/password", json=reset_password.model_dump(exclude_none=True, by_alias=True))
        if response.status_code == 201:
            return UserEnvelope(**response.json())
        return response
    
    
    @allure.step("Изменение пароля")
    def put_v1_account_password(self, change_password: ChangePassword, headers, validate_response=True):
        """
        Change registered user password
        """
        response = self.put(path=f"/v1/account/password", json=change_password.model_dump(exclude_none=True, by_alias=True), headers=headers)
        if validate_response:
            return UserEnvelope(**response.json())
        return response