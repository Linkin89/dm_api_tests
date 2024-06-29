from collections import namedtuple
from pathlib import Path
from vyper import v
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

options = (
	'service.dm_api_account',
	'service.mailhog',
	'user.login',
	'user.password',
)
@fixture(scope="session", autouse=True)
def set_config(request):
	config = Path(__file__).joinpath("../../").joinpath("config")
	config_name = request.config.getoption("--env")
	v.set_config_name(config_name)
	v.add_config_path(config)
	v.read_in_config()
  
	for option in options:
		v.set(f"{option}", request.config.getoption(f"--{option}"))
  

def pytest_addoption(parser):
	parser.addoption("--env", action="store", default="stage", help="run stage")
	for option in options:
		parser.addoption(f"--{option}", action="store", default=None)

@fixture(scope="session")
def mailhog_api():
	mailhog_configuration = MailHogConfiguration(host=v.get("service.mailhog"), disable_log=True)
	mailhog = MailHogApi(configuration=mailhog_configuration)
	return mailhog
  
  
@fixture(scope="session")
def account_api():
	dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
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
  
	dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
	account = DMApiAccount(configuration=dm_api_configuration)
	account_helper = AccountHelper(dm_account_api=account, mailhog_api=mailhog_api)
	
	account_helper.register_new_user(login=login, password=password, email=email)
	account_helper.auth_client(login=v.get("user.login"), password=v.get("user.password"))
	return account_helper


@fixture(scope="function")
def prepare_user():
	fake = Person()
	login = f"vadimko_{fake.username()}"
	email = f"{login}@mailforspam.com"
	password = v.get("user.password")
	new_password = f"new_{password}"
	User = namedtuple("User", ["login", "password", "email", "new_password"])
	user = User(login=login, password=password, email=email, new_password=new_password)
	return user