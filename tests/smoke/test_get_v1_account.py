from checkers.http_checkers import check_status_code_http
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
    has_items
)


def test_get_v1_account_auth(auth_account_helper: AccountHelper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    
    # Проверки
    assert_that(response,
        all_of(
            has_property("resource", has_property("login", starts_with("vadimko"))),
            has_property("resource", has_property("settings", has_property("color_schema", equal_to("Modern")))),
            has_property(
                "resource",
                has_property(
                    "settings",
                    has_property(
                        "paging",
                        has_properties(
                            {
                                "posts_per_page": equal_to(10),
                                "comments_per_page": equal_to(10),
                                "topics_per_page": equal_to(10),
                                "messages_per_page": equal_to(10),
                                "entities_per_page": equal_to(10),
                            }
                        ),
                    ),
                ),
            ),
            has_property("resource", has_property("roles", has_items("Guest", "Player"))),
            has_property("resource", has_property("online", instance_of(datetime)))
        )
    )   


def test_get_v1_account_no_auth(account_helper: AccountHelper):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account()
