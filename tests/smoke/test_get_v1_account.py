from checkers.http_checkers import check_status_code_http
from datetime import datetime
from dm_api_account.models.user_details_envelope import UserRole
from helpers.account_helper import AccountHelper
from assertpy import assert_that, soft_assertions
# from hamcrest import (
#     assert_that,
#     equal_to,
#     has_property,
#     instance_of,
#     starts_with,
#     all_of,
#     has_properties,
#     has_items
# )


def test_get_v1_account_auth(auth_account_helper: AccountHelper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    
    # ========= Отключил проверки Pyhamcrest, потому что конфликтует с soft_assertions =========
    # Проверки Pyhamcrest
    # assert_that(response,
    #     all_of(
    #         has_property("resource", has_property("login", starts_with("vadimko"))),
    #         has_property("resource", has_property("settings", has_property("color_schema", equal_to("Modern")))),
    #         has_property(
    #             "resource",
    #             has_property(
    #                 "settings",
    #                 has_property(
    #                     "paging",
    #                     has_properties(
    #                         {
    #                             "posts_per_page": equal_to(10),
    #                             "comments_per_page": equal_to(10),
    #                             "topics_per_page": equal_to(10),
    #                             "messages_per_page": equal_to(10),
    #                             "entities_per_page": equal_to(10),
    #                         }
    #                     ),
    #                 ),
    #             ),
    #         ),
    #         has_property("resource", has_property("roles", has_items("Guest", "Player"))),
    #         has_property("resource", has_property("online", instance_of(datetime)))
    #     )
    # )   

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
