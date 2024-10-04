from helpers.account_helper import AccountHelper


def test_get_v1_account_auth(auth_account_helper: AccountHelper):
    auth_account_helper.dm_account_api.account_api.get_v1_account()