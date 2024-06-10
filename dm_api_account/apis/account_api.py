import requests
from restclient.client import RestClient


class AccountApi(RestClient):
    def post_v1_account(self, json_data):
        """
        Register new user

        Args:
            json_data (json)
        """
        response = self.post(path=f"/v1/account", json=json_data)
        return response

    def put_v1_account_token(self, user_token):
        """
        Activate registered user

        Args:
            user_token (str)
        """

        response = self.put(path=f"/v1/account/{user_token}")
        return response

    def put_v1_account_email(self, json_data):
        """
        Change registered user email

        Args:
            json_data (json)
        """
        response = self.put(path=f"/v1/account/email", json=json_data)
        return response
