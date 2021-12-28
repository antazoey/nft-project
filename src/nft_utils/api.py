from abc import abstractmethod
from pathlib import Path
from typing import List

from nft_utils.models import Pin

# TODO: figure out how to get this into `ape`.


class PinningAPI:
    @abstractmethod
    def get_pins(self) -> List[Pin]:
        ...

    # This method requires some sort of content-mgmt outside of IPFS.
    @abstractmethod
    def get_hash(self, file_name: str):
        ...

    @abstractmethod
    def pin_file(self, file_path: Path) -> str:
        ...

    @abstractmethod
    def unpin(self, ipfs_hash: str):
        ...
