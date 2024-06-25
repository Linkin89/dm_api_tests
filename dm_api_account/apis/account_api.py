from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):
    def post_v1_account(self, registration: Registration):
        """
        Register new user

        Args:
            json_data (json)
        """
        response = self.post(path=f"/v1/account", json=registration.model_dump(exclude_none=True, by_alias=True))
        return response


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

    
    def get_v1_account(self, **kwargs):
        """
        Get current user

        Args:
            json_data (json)
        """
        response = self.get(path=f"/v1/account", **kwargs)
        return response
    
    
    def post_v1_account_password(self, reset_password: ResetPassword):
        """
        Reset registered user password
        """
        
        response = self.post(path=f"/v1/account/password", json=reset_password.model_dump(exclude_none=True, by_alias=True))
        if response.status_code == 201:
            return UserEnvelope(**response.json())
        return response
    
    
    def put_v1_account_password(self, change_password: ChangePassword, headers, validate_response=True):
        """
        Change registered user password
        """
        response = self.put(path=f"/v1/account/password", json=change_password.model_dump(exclude_none=True, by_alias=True), headers=headers)
        return response