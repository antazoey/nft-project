from typing import List

from pydantic import BaseModel, validator


class NFT(BaseModel):
    """
    An NFT model, containing the expected token ID, image ID, name, and attributes.
    """

    image: str
    tokenId: int
    name: str
    attributes: List = []

    @validator("image")
    def image_must_be_cid(cls, v):
        if not v.startswith("ipfs://"):
            raise ValueError("Image CID must start with 'ipfs://'.")
        if not len(v) == 53:
            raise ValueError("CID must be 53 characters long.")

        return v


class Pin(BaseModel):
    """
    A model of a Pin, containing the file name and content hash.
    """

    content_hash: str
    file_name: str


__all__ = ["NFT", "Pin"]
