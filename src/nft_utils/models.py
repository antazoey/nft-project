from typing import Dict

from pydantic import BaseModel


class NFTModel(BaseModel):
    image: str
    tokenId: int
    name: str
    attributes: Dict = {}
