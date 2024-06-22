from helpers.account_helper import AccountHelper

def test_delete_v1_account_login(auth_account_helper: AccountHelper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    
    # Логаут пользователя со всех учетных записей
    auth_account_helper.user_logout_all(login=login, password=password)