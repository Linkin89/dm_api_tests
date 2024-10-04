from helpers.account_helper import AccountHelper

def test_put_v1_account_email(account_helper: AccountHelper, prepare_user):
    """
    Регистрация нового пользователя, активация и авторизация.
    Изменение email, активация нового email и авторизация с изменённым email
    """
    
    login=prepare_user.login
    password=prepare_user.password
    email=prepare_user.email

    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    
    # Изменение email
    account_helper.change_email(login=login, password=password, email=email)

    # Авторизация после смены email
    account_helper.user_login(login=login, password=password)