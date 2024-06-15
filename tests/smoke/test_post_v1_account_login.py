from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from json import loads
from mimesis import Person
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                        # sort_keys=True
                                          )
    ]
)

def test_post_v1_account_login():
    """
    Авторизация пользователя с валидными и не валидными логопасс
    """
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
    mailhog_configuration = MailhogConfiguration(host="http://5.63.153.31:5025", disable_log=True)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog_api=mailhog)
    
    fake = Person()
    login = fake.username()
    email = f"{login}@mailforspam.com"
    password = "kukusik"
    
    # Регистрация пользователя
    account_helper.register_mew_user(login=login, password=password, email=email)

    # # Авторизация пользователя с НЕвалидными логопасс
    # login_inv = login+"inv",
    # password_inv = password+"inv",
    # rememberMe = False

    # account_helper.user_login(login=login_inv, password=password_inv)
    
    # Авторизация пользователя с валидными логопасс
    account_helper.user_login(login=login, password=password)