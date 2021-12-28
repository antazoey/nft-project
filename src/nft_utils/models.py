from typing import Dict

from pydantic import BaseModel


class NFT(BaseModel):
    image: str
    tokenId: int
    name: str
    attributes: Dict = {}


class Pin(BaseModel):
    content_hash: str
    file_name: str


__all__ = ["NFT", "Pin"]
