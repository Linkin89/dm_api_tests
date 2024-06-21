from helpers.account_helper import AccountHelper

def test_delete_v1_account_login(auth_account_helper: AccountHelper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    
    # Регистрация и активация нового пользователя
    auth_account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация пользователя
    auth_account_helper.user_login(login=login, password=password)
    
    # Логаут пользователя
    auth_account_helper.dm_account_api.login_api.delete_v1_account_login()
    
    