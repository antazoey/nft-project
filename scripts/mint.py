from ape import project

from ._utils import get_account, get_poofpoof_address, get_token_receivers


def mint():
    account = get_account(prompt="Select an account to use")
    contract_address = get_poofpoof_address()
    contract = project.PoofPoof.at(contract_address)

    # receivers = get_token_receivers()
    receivers = ["0xE3747e6341E0d3430e6Ea9e2346cdDCc2F8a4b5b"]
    token_id = 0
    for receiver in receivers:
        contract.safeMint(receiver, f"{token_id}.json", sender=account)
        token_id += 1


def main():
    mint()
