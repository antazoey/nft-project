from pathlib import Path
from typing import List, Optional

from nft_project import IPinning, Pin
from pinata.api_key import get_key_manager
from pinata.clients.data import DataClient
from pinata.clients.pinning import PinningClient
from pinata.exceptions import (
    NoContentError,
    PinataBadRequestError,
    PinataInternalServiceError,
    PinError,
)
from pinata.session import PinataAPISession


class Pinata(IPinning):
    def __init__(self, pinning_client: PinningClient, data_client: DataClient):
        self.pinning = pinning_client
        self.data = data_client

    @classmethod
    def from_profile_name(cls, profile_name: str) -> "Pinata":
        """
        Create an instance of the Pinata SDK from a stored profile name.

        Args:
            profile_name (str): The name of the API key profile to use.
        """
        key_manager = get_key_manager()
        api_key, api_secret = key_manager.get_key_pair(profile_name)
        return cls.from_api_key(api_key, api_secret)

    @classmethod
    def from_api_key(cls, api_key: str, api_secret: str) -> "Pinata":
        """
        Create an instance of the Pinata SDK from an API key.
        `Guide on API key <https://docs.pinata.cloud/user/generate-api-key>`__.

        Args:
            api_key (str): The API key.
            api_secret (str): The API secret.
        """
        session = PinataAPISession.from_api_key(api_key, api_secret)
        pinning_client = PinningClient(session)
        data_client = DataClient(session)
        return cls(pinning_client, data_client)

    def get_pins(self) -> List[Pin]:
        """
        Get all pins.

        Returns:
            List[``Pin``]
        """

        pins = self.data.search_pins(status="pinned")["rows"]
        return [Pin(content_hash=p["ipfs_pin_hash"], file_name=p["metadata"]["name"]) for p in pins]

    def get_hash(self, file_name: str) -> Optional[str]:
        """
        Get the hash of a pinned file by file name.
        **NOTE**: Returns the first hash it finds for the given name.

        Args:
            file_name (str): The name of the file.

        Returns:
            Optional[str]: The content IPFS hash str.
        """

        pins = self.get_pins()
        for pin in pins:
            if pin.file_name == file_name:
                return pin.content_hash

        return None

    def pin_file(self, file_path: Path) -> str:
        """
        Add and pin any file, or directory, to Pinata's IPFS nodes.

        Args:
            file_path (pathlib.Path): The path to the file to pin.

        Returns:
            :class:`~pinata.response.PinataResponse`
        """

        is_json = file_path.suffix == ".json"
        try:
            response = (
                self.pinning.pin_json(file_path) if is_json else self.pinning.pin_file(file_path)
            )
        except PinataBadRequestError as err:
            raise PinError(file_path) from err

        return response.data["IpfsHash"]

    def unpin(self, content_hash: str, ignore_errors: bool = False):
        """
        Unpin content they previously uploaded to Pinata's IPFS nodes.

        Args:
            content_hash (str): The hash of the content to stop pinning.
            ignore_errors (bool): Ignore known errors.

        Returns:
            :class:`~pinata.response.PinataResponse`
        """
        try:
            self.pinning.unpin(content_hash)
        except PinataInternalServiceError as err:
            if ignore_errors:
                return

            raise NoContentError(content_hash) from err
