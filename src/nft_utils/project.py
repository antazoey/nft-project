from pathlib import Path
from typing import Dict

from nft_utils.api import PinningAPI


class Project:
    def __init__(
        self,
        ipfs_client: PinningAPI,
        project_directory: Path = Path("artwork"),
    ) -> None:
        self._path = project_directory
        self._ipfs = ipfs_client

    def deploy_artwork(self) -> Dict:
        artwork_hashes = {}

        for artwork_file_path in self._path.iterdir():
            content_hash = self._ipfs.get_hash(artwork_file_path.name)
            if not content_hash:
                # Pin artwork if it is not already pinned.
                content_hash = self._ipfs.pin_file(artwork_file_path)

            artwork_hashes[artwork_file_path.name] = content_hash

        return artwork_hashes
