from checkers.http_checkers import check_status_code_http
from datetime import datetime
from helpers.account_helper import AccountHelper
from hamcrest import (
    assert_that,
    equal_to,
    has_property,
    starts_with,
    all_of,
    has_properties,
)


def test_get_v1_account_auth(auth_account_helper: AccountHelper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()

    # Проверки
    assert_that(
        all_of(
            response,
            has_property("resource", has_property("login", starts_with("vadimko"))),
            has_property(
                "resource",
                has_property(
                    "setting", has_property("colorSchema", equal_to("Modern"))
                ),
            ),
            has_property(
                "resource",
                has_property(
                    "setting",
                    has_property(
                        "paging",
                        has_properties(
                            {
                                "postsPerPage": equal_to(10),
                                "commentsPerPage": equal_to(10),
                                "topicsPerPage": equal_to(10),
                                "messagesPerPage": equal_to(10),
                                "entitiesPerPage": equal_to(10),
                            }
                        ),
                    ),
                ),
            ),
            has_property(
                "resource", has_property("roles", has_properties("Guest", "Player"))
            ),
            has_property(
                "resource",
                has_property("online", starts_with(datetime.now().strftime("%Y-%m"))),
            ),
        )
    )


def test_get_v1_account_no_auth(account_helper: AccountHelper):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account()
