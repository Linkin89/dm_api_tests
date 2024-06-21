from restclient.configuration import Configuration as MailHogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
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
  dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=True)
  account = DMApiAccount(configuration=dm_api_configuration)
  return account  