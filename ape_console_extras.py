from ape.api.networks import LOCAL_NETWORK_NAME

from sdk import sdk


def ape_init_extras(accounts, networks):
    if networks.provider.name == LOCAL_NETWORK_NAME:
        # Mimic fixtures in tests/conftest.py
        return {
            "owner": accounts.test_accounts[0],
            "token_receiver": accounts.test_accounts[1],
            "metadata_cid": sdk.metadata_cid,
        }
