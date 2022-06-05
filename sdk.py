from typing import Iterator, List, Optional

from pathlib import Path
import click
from nft_project import NFTProject
from pinata import create_pinata

from ape import accounts, config, networks
from ape.api import AccountAPI
from ape.cli import get_user_selected_account
from aep.types import AddressType
from ape.utils import cached_property
from ape_accounts import KeyfileAccount


class PoofPoofPass:
    def __init__(self, name: str = "poofpoof", artwork_path: Path = Path("artwork")) -> None:
        self.name = name
        self.pinata = create_pinata(self.name)
        self.nft_project = NFTProject(self.name, self.pinata)
        self.artwork_path = artwork_path

    @property
    def network_name(self) -> str:
        return networks.provider.network.name

    @property
    def artwork_file_paths(self) -> List[Path]:
        return [a for a in self.artwork_path.iterdir()]

    @cached_property
    def metadata_cid(self) -> str:
        """
        Return existing metadata CID for folder. If folder not
        yet pinned, will pin it. Additionally, if any artwork is
        not pinned, it will pin those now as well.

        Returns:
            str: The CID of the metadata JSONs folder.
        """
        content_hash_map = self.nft_project.pin_artwork(self.artwork_path)
        content_hashes = [f"ipfs://{cid}" for _, cid in content_hash_map.items()]
        nft_metadata_list = self.nft_project.create_nft_data(content_hashes)
        folder_cid = self.nft_project.pin_metadata(nft_metadata_list)
        folder_cid = f"ipfs://{folder_cid}/"
        return folder_cid

    def get_account(self, prompt: Optional[str] = None) -> AccountAPI:
        prompt = prompt or "Select an account"
        if self.network_name == "local":
            return accounts.test_accounts[0]

        return get_user_selected_account(cls=KeyfileAccount, prompt_message=prompt)

    def get_poofpoof_address(self) -> Optional[AddressType]:
        network_deployments = config.deployments["ethereum"].get(self.network_name) or []
        if network_deployments:
            return [d for d in network_deployments if d["contract_type"] == "PoofPoof"][0]["address"]
        else:
            click.echo(f"No address for network '{self.network_name}'.", err=True)

    def get_token_receivers(self, token_id: int) -> Iterator[str]:
        # TODO: Figure out how to populate token receivers list.
        _ = token_id
        receivers = {"lester": "0x4e3b9a9f52d66E62f596A7b8A258Aff9AeeB15C2"}
        yield from receivers.values()
    
    def clean_pins(self):
        directory_pin = sdk.pinata.get_hash(self.name)
        image_pins = [self.pinata.get_hash(a.name) for a in self.artwork_file_paths]
        self.pinata.unpin(directory_pin, ignore_errors=True)
        for pin in image_pins:
            self.pinata.unpin(pin, ignore_errors=True)



sdk = PoofPoofPass()
