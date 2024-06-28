from contextlib import contextmanager
import requests
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(expected_status_code: requests.codes = requests.codes.ok,
    expected_message: str = "User must be authenticated"):
    try:
        yield
        if expected_status_code != requests.codes.ok:
            raise AssertionError(
                f"Ожидаемый статус код должен быть {expected_status_code}")
        if expected_message:
            raise AssertionError(f"Должно быть получено сообщение '{expected_message}', но запрос прошёл успешно")
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()["title"] == expected_message