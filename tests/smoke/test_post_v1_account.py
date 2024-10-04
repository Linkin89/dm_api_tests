from datetime import datetime
from helpers.account_helper import AccountHelper
from hamcrest import (
    assert_that,
    equal_to,
    has_property,
    instance_of,
    starts_with,
    all_of,
    has_properties,
)


def test_post_v1_account(account_helper: AccountHelper, prepare_user):
    """
    Регистрация нового пользователя
    """

    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация пользователя
    response = account_helper.user_login(login=login, password=password, validate_response=True)

    assert_that(
        response,
        all_of(
            has_property("resource", has_property("login", starts_with("vadimko"))),
            has_property("resource", has_property("registration", instance_of(datetime))),
            has_property(
                "resource",
                has_properties(
                    {
                        "rating": has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0),
                            }
                        )
                    }
                ),
            ),
        ),
    )
    # print(response)
