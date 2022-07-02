from ape.api.networks import LOCAL_NETWORK_NAME

from sdk import sdk


def ape_init_extras(accounts, networks):
    extra_data = {"sdk": sdk}

    if networks.provider.name == LOCAL_NETWORK_NAME:
        # Mimic fixtures in tests/conftest.py
        extra_data["owner"] = accounts.test_accounts[0]
        extra_data["token_receiver"] = accounts.test_accounts[1]
    
    return extra_data
