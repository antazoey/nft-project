import json

from pinata.exceptions import PinataResponseKeyError


class PinataResponse:
    def __init__(self, requests_response):
        self._response = requests_response
        self._data = None

    @property
    def data(self):
        try:
            self._data = self._data or json.loads(self._response.text)
        except ValueError:
            self._data = self._response.text or ""

        return self._data

    def __getitem__(self, key):
        try:
            return self.data[key]
        except (KeyError, TypeError):
            raise PinataResponseKeyError(key, self._data)


__all__ = ["PinataResponse"]
