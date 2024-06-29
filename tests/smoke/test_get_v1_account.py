from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole
from helpers.account_helper import AccountHelper
from assertpy import assert_that, soft_assertions



def test_get_v1_account_auth(auth_account_helper: AccountHelper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    
    # Проверки Pyhamcrest
    GetV1Account.check_response_values(response)   

    # Проверки Sofr Assertions
    with soft_assertions():
        assert_that(response.resource.login).starts_with("vadimko")
        print("Проверили логин")
        assert_that(response.resource.settings.color_schema).is_equal_to("Modern")
        print("Проверили Color Schema")
        assert_that(response.resource.roles).contains(UserRole.Guest, UserRole.Player)
        print("Проверили роли")



def test_get_v1_account_no_auth(account_helper: AccountHelper):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account()
