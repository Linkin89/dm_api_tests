from helpers.account_helper import AccountHelper
import allure


@allure.suite("Тесты проверки метода PUT v1/account/password")
@allure.sub_suite("Изменение пароля на валидный пароль")
def test_put_v1_account_password(account_helper: AccountHelper, prepare_user):
    """
    Регистрация нового пользователя, активация и авторизация.
    Изменение пароля и авторизация с изменённым паролем.
    """
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = prepare_user.new_password
    
    # Регистрация и активация нового пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
       
    # Авторизация пользователя
    account_helper.user_login(login=login, password=password)
    
    # Изменение пароля пользователя
    account_helper.change_password(login=login, password=password, new_password=new_password, email=email)
    
    # Авторизация после смены пароля
    account_helper.user_login(login=login, password=new_password)
    
    
    