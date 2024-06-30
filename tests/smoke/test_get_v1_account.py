from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole
from helpers.account_helper import AccountHelper
from assertpy import assert_that, soft_assertions
import allure

@allure.suite("Тесты проверки метода GET v1/account")
@allure.sub_suite("Получение данных авторизованного пользователя")
def test_get_v1_account_auth(auth_account_helper: AccountHelper):
    """
    Получение информации авторизованного пользователя
    """
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    
    # Проверки Pyhamcrest
    with allure.step("Проверка тела ответа c помощью PyHamcrest"):
        GetV1Account.check_response_values(response)   

    # Проверки Soft Assertions
    with allure.step("Проверка тела ответа c помощью Soft Assertios"):
        with soft_assertions():
            assert_that(response.resource.login).starts_with("vadimko")
            print("Проверили логин")
            assert_that(response.resource.settings.color_schema).is_equal_to("Modern")
            print("Проверили Color Schema")
            assert_that(response.resource.roles).contains(UserRole.Guest, UserRole.Player)
            print("Проверили роли")



@allure.suite("Тесты проверки метода GET v1/account")
@allure.sub_suite("Получение данных неавторизованного пользователя")
def test_get_v1_account_no_auth(account_helper: AccountHelper):
    """
    Получение информации неавторизованного пользователя
    """
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account()
