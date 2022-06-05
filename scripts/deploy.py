import click
from ape import project
from ape.cli import NetworkBoundCommand, network_option

from sdk import sdk


@click.command("deploy", cls=NetworkBoundCommand)
@network_option()
def cli(network):
    _ = network  # Needed for 'NetworkBoundCommand'.
    account = sdk.get_account(prompt="Select an account to use")
    account.deploy(project.PoofPoof, sdk.metadata_cid)
