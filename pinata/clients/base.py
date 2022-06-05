from pinata.response import PinataResponse
from pinata.session import PinataAPISession


class PinataClient:
    def __init__(self, session: PinataAPISession, api_namespace: str):
        self.session = session
        self._prefix = api_namespace

    def _post(self, uri, *args, **kwargs) -> PinataResponse:
        return self.session.post(self._uri(uri), *args, **kwargs)

    def _get(self, uri, *args, **kwargs) -> PinataResponse:
        return self.session.get(self._uri(uri), *args, **kwargs)

    def _delete(self, uri, *args, **kwargs) -> PinataResponse:
        return self.session.delete(self._uri(uri), *args, **kwargs)

    def _uri(self, uri: str) -> str:
        return f"/{self._prefix}/{uri}"


__all__ = ["PinataClient"]
