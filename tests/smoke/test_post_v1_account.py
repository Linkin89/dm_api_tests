from checkers.http_checkers import check_status_code_http
import pytest
from checkers.post_v1_account import PostV1Account
from helpers.account_helper import AccountHelper
import allure


@allure.suite("Тесты проверки метода POST v1/account")
@allure.sub_suite("Позитивные тесты")
class TestsPostV1Account:
    @allure.title("Проверка метода регистрации пользователя ")
    def test_post_v1_account(self, account_helper: AccountHelper, prepare_user):
        """
        Регистрация и авторизация нового пользователя c валидными данными
        """

        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        # Регистрация пользователя
        account_helper.register_new_user(login=login, password=password, email=email)

        # Авторизация пользователя
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1Account.check_response_values(response)


@allure.suite("Тесты проверки метода POST v1/account")
@allure.sub_suite("Проверка регистрации пользователя с невалидными данными")
@pytest.mark.parametrize("login, password, email, status_code, message",[
            # Короткий пароль
        (   
            "vadimko_user1",
            "kuku",
            "vadimko_user1@mailforspam.com",
            400,
            "Validation failed",
        ),  
            # Неправильный адрес почты
        (
            "vadimko_user2",
            "kukusik",
            "vadimko_user2mailforspam.com",
            400,
            "Validation failed",
        ),  
            # Короткий логин
        (
            "v", 
            "kukusik", 
            "vadimko_user3@mailforspam.com", 
            400, 
            "Validation failed"
        ),
    ],
)  
def test_post_v1_account_invalid_logopass(
    account_helper: AccountHelper, login, password, email, status_code, message
):
    """
    Регистрация нового пользователя с невалидными данными
    """

    # Регистрация пользователя
    with check_status_code_http(status_code, message):
        account_helper.register_new_user(login=login, password=password, email=email)
