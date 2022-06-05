from ape import accounts, project
from ape.api.networks import LOCAL_NETWORK_NAME

from sdk import sdk


def gambit():
    assert sdk.network_name == LOCAL_NETWORK_NAME
    account = accounts.load("metamask0")
    contract = account.deploy(project.PoofPoof, sdk.metadata_cid)
    contract.safeMint(account.address, "0.json", sender=account)


def main():
    gambit()
