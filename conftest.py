from collections import namedtuple
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


@fixture(scope="session")
def mailhog_api():
  mailhog_configuration = MailHogConfiguration(host="http://5.63.153.31:5025", disable_log=True)
  mailhog = MailHogApi(configuration=mailhog_configuration)
  return mailhog
  
  
@fixture(scope="session")
def account_api():
  dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
  account = DMApiAccount(configuration=dm_api_configuration)
  return account  


@fixture(scope="session")
def account_helper(account_api, mailhog_api):
  account_helper = AccountHelper(dm_account_api=account_api, mailhog_api=mailhog_api)
  return account_helper


@fixture(scope="function")
def auth_account_helper(mailhog_api, prepare_user):
  login = prepare_user.login
  password = prepare_user.password
  email = prepare_user.email
  
  dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
  account = DMApiAccount(configuration=dm_api_configuration)
  account_helper = AccountHelper(dm_account_api=account, mailhog_api=mailhog_api)
  
  account_helper.register_new_user(login=login, password=password, email=email)
  account_helper.auth_client(login=login, password=password)
  return account_helper


@fixture(scope="function")
def prepare_user():
  fake = Person()
  login = f"{fake.username()}"
  email = f"{login}@mailforspam.com"
  password = "kukusik"
  new_password = f"new_{password}"
  User = namedtuple("User", ["login", "password", "email", "new_password"])
  user = User(login=login, password=password, email=email, new_password=new_password)
  return user