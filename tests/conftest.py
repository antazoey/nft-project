import ape
import pytest

from sdk import sdk


@pytest.fixture(scope="session")
def metadata_cid(sdk):
    return sdk.metadata_cid


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def token_receiver(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def poofpoof_address(owner, project, metadata_cid):
    return owner.deploy(project.PoofPoof, metadata_cid).address


@pytest.fixture(scope="session")
def poofpoof(poofpoof_address):
    return ape.Contract(poofpoof_address)
