from pathlib import Path
from typing import IO, Dict, Union

from pinata.clients.base import PinataClient
from pinata.response import PinataResponse
from pinata.session import PinataAPISession
from pinata.utils import json_to_dict


class PinningClient(PinataClient):
    def __init__(self, session: PinataAPISession):
        super().__init__(session, "pinning")

    def pin_file(self, file_path: Path) -> PinataResponse:
        """
        Add and pin any file, or directory, to Pinata's IPFS nodes.

        Args:
            file_path (pathlib.Path): The path to the file to pin.

        Returns:
            :class:`~pinata.response.PinataResponse`
        """
        paths = [f for f in file_path.iterdir()] if file_path.is_dir() else [file_path]
        files = (
            [("file", (str(path), open(path, "rb"))) for path in paths]
            if file_path.is_dir()
            else [("file", open(path, "rb")) for path in paths]
        )
        return self._post("pinFileToIPFS", files=files)

    def pin_json(self, json_arg: Union[Path, IO, Dict]) -> PinataResponse:
        """
        Add and pin any JSON object they wish to Pinata's IPFS nodes. This endpoint is
        specifically optimized to only handle JSON content.

        Args:
            json_arg (pathlib.Path): Either the path to a JSON file, a python dictionary,
              or an IO stream of an opened JSON file.

        Returns:
            :class:`~pinata.response.PinataResponse`
        """
        json_data = json_to_dict(json_arg)
        data = {"pinataContent": json_data}
        return self._post("pinJSONToIPFS", json=data)

    def pin_hash(self, hash_: str) -> PinataResponse:
        """
        Add a hash to Pinata for asynchronous pinning. Content added through this endpoint
        is pinned in the background and will show up in your pinned items once the content
        has been found/pinned. **For this operation to succeed, the content for the hash you
        provide must already be pinned by another node on the IPFS network.**

        Args:
            hash_: The hash to pin.

        Returns:
            :class:`~pinata.response.PinataResponse`
        """
        data = {"hashToPin": hash_}
        return self._post("addHashToPinQueue", json=data)

    def unpin(self, content_hash: str) -> PinataResponse:
        """
        Unpin content they previously uploaded to Pinata's IPFS nodes.

        Args:
            content_hash (str): The hash of the content to stop pinning.

        Returns:
            :class:`~pinata.response.PinataResponse`
        """
        return self._delete(f"unpin/{content_hash}")


__all__ = ["PinningClient"]
