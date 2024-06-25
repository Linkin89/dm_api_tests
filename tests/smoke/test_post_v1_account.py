from urllib import response
from helpers.account_helper import AccountHelper


def test_post_v1_account(account_helper: AccountHelper, prepare_user):
  """
  Регистрация нового пользователя
  """
  
  login = prepare_user.login
  password = prepare_user.password
  email = prepare_user.email
  
  # Регистрация пользователя
  response = account_helper.register_new_user(login=login, password=password, email=email)
  print(response)

  # Авторизация пользователя
  account_helper.user_login(login=login, password=password) 