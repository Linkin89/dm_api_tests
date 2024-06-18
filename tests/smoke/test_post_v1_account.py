from collections import namedtuple
from datetime import datetime
import email
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailHogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from mimesis import Person
from pytest import fixture
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                        # sort_keys=True
                                          )
    ]
)

@fixture
def mailhog_api():
  mailhog_configuration = MailHogConfiguration(host="http://5.63.153.31:5025", disable_log=True)
  mailhog = MailHogApi(configuration=mailhog_configuration)
  return mailhog
  
@fixture
def account_api():
  dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
  account = DMApiAccount(configuration=dm_api_configuration)
  return account  


@fixture
def account_helper(account_api, mailhog_api):
  account_helper = AccountHelper(dm_account_api=account_api, mailhog_api=mailhog_api)
  return account_helper


@fixture
def prepare_user():
  now = datetime.now()
  data = now.strftime("%d_%m_%Y_%H_%M_%S")
  fake = Person()
  login = f"{fake.username()}_{data}"
  email = f"{login}@mailforspam.com"
  password = "kukusik"
  User = namedtuple("User", ["login", "password", "email"])
  user = User(login=login, password=password, email=email)
  return user

def test_post_v1_account(account_helper, prepare_user):
  """
  Регистрация нового пользователя
  """
  
  login = prepare_user.login
  password = prepare_user.password
  email = prepare_user.email
  
  # Регистрация пользователя
  account_helper.register_new_user(login=login, password=password, email=email)

  # Авторизация пользователя
  account_helper.user_login(login=login, password=password)