import json
import shutil
import os
import tempfile
from pathlib import Path
from typing import Callable, Dict, List, Union, Optional

from project_nft.api import PinningAPI
from project_nft.models import NFT

ARTWORK_DIRECTORY = "artwork"


class NFTProjectError(Exception):
    """
    Raised when an error occurs related to the NFT project.
    """


class MetadataFileNameError(NFTProjectError):
    """
    Raised when unable to craft a metadata.json file name.
    """
    def __init__(self, pattern: str):
        super().__init__(f"Was unable to form file name from pattern {pattern}.")


class NFTProject:
    """
    A class representing the active NFT project.
    """

    def __init__(
        self,
        name: str,
        ipfs_client: PinningAPI,
        metadata_file_pattern: str = "{token_id}.json",
        nft_data_modifier: Optional[Callable[[NFT], NFT]] = None
    ) -> None:
        self._name = name
        self._ipfs = ipfs_client
        self._metadata_file_pattern = metadata_file_pattern
        self._nft_data_modifier = nft_data_modifier

    def create_nft_data(self, content_hashes: List[str]) -> List[NFT]:
        """
        Create a list of NFT objects from already-pinned content hashes.

        Args:
            content_hashes (List[str]): Content hashes from pinned metadata files.

        Returns:
            List[:class:`~project_nft.models.NFT`]: A list of NFT pydantic models.
        """

        token_id = 0
        nft_data = []
        for cid in content_hashes:
            nft_metadata_dict = self.create_nft(cid, token_id)
            nft_data.append(nft_metadata_dict)

        return nft_data

    def create_nft(self, cid: str, index: int, attributes: Dict = None) -> NFT:
        """
        Create an NFT model object.

        Args:
            cid (str): The content IPFS hash.
            index (int): The index or token ID.
            attributes (Dict): A dictionary of attributes.

        Returns:
            :class:`~project_nft.models.NFT`
        """

        artwork_name = f"{self._name} Number {index}"
        attributes = attributes or []
        nft = NFT(image=cid, tokenId=index, name=artwork_name, attributes=attributes)

        if self._nft_data_modifier:
            nft = self._nft_data_modifier(nft)

        return nft

    def pin_artwork(self, artwork_path: Optional[Union[str, Path]] = ARTWORK_DIRECTORY) -> Dict:
        """
        Pin your artwork to IPFS.

        Args:
            artwork_path (Union[str, Path]): The path to the artwork file or list of files.
              If list contains directories, they will be flattened to files. This method
              does not pin directories.

        Returns:
            Dict: A dictionary of file names to their content IPFS hashes.
        """

        artwork_path = Path(artwork_path)
        artwork_hashes = {}
        artwork_paths = (
            list(artwork_path.rglob("*.*")) if artwork_path.is_dir() else [artwork_path]
        )

        for artwork_path in artwork_paths:
            content_hash = self._ipfs.get_hash(artwork_path.name)
            if not content_hash:
                # Pin artwork if it is not already pinned.
                content_hash = self._ipfs.pin_file(artwork_path)

            artwork_hashes[artwork_path.name] = content_hash

        return artwork_hashes

    def pin_metadata(self, nft_data: List[NFT]) -> str:
        """
        Pin NFT metadata. Provide it a list of :class:`project_nft.models.NFT` objects
        and it will create a temporary directory containing equivalent JSON files and
        then it will pin the whole directory to IPFS.

        Args:
            nft_data (List[:class:`project_nft.models.NFT`]): The list of NFT models.

        Returns:
            str: The content IPFS hash of the newly pinned directory.
        """

        content_hash = self._ipfs.get_hash(self._name)
        if content_hash:
            return content_hash

        # Create and pin metadata JSON files to IPFS
        with tempfile.TemporaryDirectory() as temp_dir:
            owd = os.getcwd()

            try:
                os.chdir(temp_dir)
                project_path = Path(self._name)
                shutil.rmtree(project_path, ignore_errors=True)
                project_path.mkdir()

                for nft in nft_data:
                    metadata_file_name = self._metadata_file_pattern.format(
                        token_id=nft.tokenId
                    )
                    if not metadata_file_name:
                        raise MetadataFileNameError(self._metadata_file_pattern)

                    metadata_file_path = project_path / metadata_file_name
                    metadata_file_path.write_text(json.dumps(nft.dict()))
                
                content_hash = self._ipfs.pin_file(project_path)

            finally:
                os.chdir(owd)

        return content_hash
