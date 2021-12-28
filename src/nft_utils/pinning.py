from pathlib import Path
from typing import Dict, Optional

from pinata import Pinata
from pinata.api_key import set_keys_from_prompt

PINATA_API_KEY_PROFILE_NAME = "poofpoof"


class PinataWrapper:
    def __init__(self) -> None:
        pinata_sdk = Pinata.from_profile_name(PINATA_API_KEY_PROFILE_NAME)

        if not pinata_sdk:
            set_keys_from_prompt(PINATA_API_KEY_PROFILE_NAME)

        self._sdk = pinata_sdk

    def deploy_artwork(self) -> Dict:
        artwork_hashes = {}

        for artwork_file_path in Path("artwork").iterdir():
            content_hash = self.get_hash(artwork_file_path.name)
            if not content_hash:
                # Pin artwork if it is not already pinned.
                response = self._sdk.pin_file(artwork_file_path)
                content_hash = response.data["IpfsHash"]

            artwork_hashes[artwork_file_path.name] = content_hash

        return artwork_hashes

    def get_hash(self, artwork_name: str) -> Optional[str]:
        response = self._sdk.data.search_pins(status="pinned")
        pins = response["rows"]
        for pin in pins:
            name = pin["metadata"]["name"]
            if name == artwork_name:
                return pin["ipfs_pin_hash"]

        return None
