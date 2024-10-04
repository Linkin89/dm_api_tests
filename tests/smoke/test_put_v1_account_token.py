from helpers.account_helper import AccountHelper
import allure

@allure.suite("Тесты проверки метода PUT v1/account/token")
@allure.sub_suite("Активация пользователя")
def test_put_v1_account_token(account_helper: AccountHelper, prepare_user):
    """
    Проверка активации пользователя
    """
    
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация пользователя
    account_helper.user_login(login=login, password=password)