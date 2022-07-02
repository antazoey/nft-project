from requests.auth import AuthBase


class PinataAuth(AuthBase):
    def __init__(self, api_key, secret):
        self.__api_key = api_key
        self.__secret = secret

    def __call__(self, r):
        r.headers["pinata_api_key"] = self.__api_key
        r.headers["pinata_secret_api_key"] = self.__secret
        return r


__all__ = ["PinataAuth"]
