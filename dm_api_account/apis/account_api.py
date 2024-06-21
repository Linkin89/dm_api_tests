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

    
    def get_v1_account(self, **kwargs):
        """
        Get current user

        Args:
            json_data (json)
        """
        response = self.get(path=f"/v1/account", **kwargs)
        return response
    
    
    def post_v1_account_password(self, json_data):
        """
        Reset registered user password
        """
        response = self.post(path=f"/v1/account/password", json=json_data)
        return response
    
    
    def put_v1_account_password(self, json_data, headers):
        """
        Change registered user password
        """
        response = self.put(path=f"/v1/account/password", json=json_data, headers=headers)
        return response