from typing import Optional

from pinata.clients.base import PinataClient
from pinata.response import PinataResponse
from pinata.session import PinataAPISession


class DataClient(PinataClient):
    def __init__(self, session: PinataAPISession):
        super().__init__(session, "data")

    def search_pins(
        self,
        hash_contains: Optional[str] = None,
        pin_start: Optional[str] = None,
        pin_end: Optional[str] = None,
        unpin_start: Optional[str] = None,
        unpin_end: Optional[str] = None,
        pin_size_min: Optional[int] = None,
        pin_size_max: Optional[int] = None,
        status: Optional[str] = None,
    ) -> PinataResponse:
        """
        Search pins.

        Args:
            hash_contains (str): Filter on alphanumeric characters inside of pin hashes.
              Hashes which do not include the characters passed in will not be returned.
            pin_start (str): ISO_8601 format date str for excluding pin records that were
              pinned before this date.
            pin_end (str): ISO_8601 format date str for excluding pin records that were
              pinned after this date.
            unpin_start (str): ISO_8601 format date str for excluding pin records that were
              unpinned before this date.
            unpin_end (str): ISO_8601 format date str for excluding pin records that were
              unpinned after this date.
            pin_size_min (int): The minimum byte size that pin record you're looking for
              can have.
            pin_size_max (int): The maximum byte size that pin record you're looking for
              can have.
            status (str): Pass in ``"all"`` for both pinned and unpinned records. Pass in
              ``"pinned"`` for just pinned records (hashes that are currently pinned). Pass
              in ``"unpinned"`` for just unpinned records (previous hashes that are no longer
              being pinned on pinata).

        Returns:
            :class:`~pinata.response.PinataResponse`
        """
        params = {
            "hashContains": hash_contains,
            "pinStart": pin_start,
            "pinEnd": pin_end,
            "unpinStart": unpin_start,
            "unpinEnd": unpin_end,
            "pinSizeMin": pin_size_min,
            "pinSizeMax": pin_size_max,
            "status": status,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("pinList", params=params)


__all__ = ["DataClient"]
