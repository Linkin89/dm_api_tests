from restclient.client import RestClient
import allure

class MailhogApi(RestClient):
    @allure.step("Получение всех писем")
    def get_api_v2_messages(self, limit=50):
        """
        Get Users emails
        """

        params = {
            "limit": limit,
        }

        response = self.get(path=f"/api/v2/messages", params=params, verify=False)
        return response
