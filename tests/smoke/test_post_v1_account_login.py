from helpers.account_helper import AccountHelper
import allure


@allure.suite("Тесты проверки метода POST v1/account/login")
def test_post_v1_account_login(account_helper: AccountHelper, prepare_user):
    """
    Проверка авторизации пользователя
    """
    
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    
    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    
    # Авторизация пользователя с валидными логопасс
    account_helper.user_login(login=login, password=password)