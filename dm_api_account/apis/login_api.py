from restclient.client import RestClient


class LoginApi(RestClient):
    def post_v1_account_login(self, json_data):
        """
        User authorization

        Args:
            json_data (json)
        """

        response = self.post(path=f"/v1/account/login", json=json_data)
        return response

    
    def delete_v1_account_login(self, token=None):
        """
        Logout as current user

        Args:
            json_data (json)
        """
        
        headers = {
            "X-Dm-Auth-Token": token
        }
        
        response = self.delete(path=f"/v1/account/login", headers=headers)
        return response
    
    def delete_v1_account_login_all(self, token=None):
        """
        Logout as current user

        Args:
            json_data (json)
        """
        
        headers = {
            "X-Dm-Auth-Token": token
        }
        
        response = self.delete(path=f"/v1/account/login/all", headers=headers)
        return response
    