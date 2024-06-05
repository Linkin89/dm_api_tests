import requests


class AccountApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data):
        """Register new user

        Args:
            json_data (json)
        """
        response = requests.post(url=f"{self.host}/v1/account", json=json_data)
        return response

    def put_v1_account_token(self, user_token):
        """Activate registered user

        Args:
            user_token (str)
        """
        headers = {
            "accept": "text/plain",
        }

        response = requests.put(
            url=f"{self.host}/v1/account/{user_token}", headers=headers
        )
        return response
