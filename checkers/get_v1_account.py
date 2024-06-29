from datetime import datetime
from hamcrest import all_of, assert_that, equal_to, has_items, has_properties, has_property, instance_of, starts_with


class GetV1Account:
    @classmethod
    def check_response_values(cls, response):
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
