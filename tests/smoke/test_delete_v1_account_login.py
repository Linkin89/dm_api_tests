from helpers.account_helper import AccountHelper
import allure

@allure.suite("Тесты проверки метода DELETE v1/account/login")
def test_delete_v1_account_login(auth_account_helper: AccountHelper, prepare_user):
    """
    Логаут пользователя с устройства
    """
    login = prepare_user.login
    password = prepare_user.password
    
    # Получаем токен для логаута пользователя
    token = auth_account_helper.get_authorization_token(login=login, password=password)
    
    # Логаут пользователя
    auth_account_helper.user_logout(token=token)