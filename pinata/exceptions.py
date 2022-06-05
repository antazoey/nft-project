from typing import Dict, Union

from requests.exceptions import HTTPError


class PinataException(Exception):
    """
    A base-exceptions class in 'py-pinata'.
    """


class PinataMissingAPIKeyError(PinataException):
    """
    Raised when an API key or secret is suddenly missing.
    """

    def __init__(self, profile_name: str):
        super().__init__(f"API key or secret for profile '{profile_name}' is missing.")


class PinError(PinataException):
    """
    Raised when unable to pin a file.
    """

    def __init__(self, file_name: str):
        super().__init__(f"Unable to pin file '{file_name}'.")


class PinataResponseKeyError(KeyError, PinataException):
    """
    An error raised when trying to access the wrong key from a response.
    """

    def __init__(self, key: Union[int, str], response_data: Dict):
        message = f"Key '{key}' not found in response ({response_data})."
        super().__init__(message)


class MissingResponseError(PinataException):
    """
    An error raised when a response was not given.
    """

    def __init__(self, method: str, url: str):
        msg = f"No response was returned for {method} request to {url}."
        super().__init__(msg)


class PinataHTTPError(PinataException):
    """
    An error raised when an HTTP request fails.
    """


class PinataBadRequestError(PinataHTTPError):
    """
    An error raised when receiving the 400 error code.
    """


class PinataUnauthorizedError(PinataHTTPError):
    """
    An error raised when receiving the 401 error code.
    """


class PinataForbiddenError(PinataHTTPError):
    """
    An error raised when receiving the 403 error code.
    """


class PinataNotFoundError(PinataHTTPError):
    """
    An error raised when receiving the 404 error code.
    """


class PinataTooManyRequestsError(PinataHTTPError):
    """
    An error raised when receiving the 429 error code.
    """


class PinataInternalServiceError(PinataHTTPError):
    """
    An error raised when receiving the 429 error code.
    """


class NoContentError(PinataException):
    """
    An error raised when trying to unpin content that does not exist.
    """

    def __init__(self, content_hash: str):
        super().__init__(f"No pinned content found with hash '{content_hash}'.")


def raise_pinata_http_error(raised_error: HTTPError):
    """
    Raise the appropriate :class:`pinata.exceptions.PinataHTTPError` based on the given
    HTTPError's response status code.
    """
    if raised_error.response.status_code == 400:
        raise PinataBadRequestError(raised_error)
    elif raised_error.response.status_code == 401:
        raise PinataUnauthorizedError(raised_error)
    elif raised_error.response.status_code == 403:
        raise PinataForbiddenError(raised_error)
    elif raised_error.response.status_code == 404:
        raise PinataNotFoundError(raised_error)
    elif raised_error.response.status_code == 429:
        raise PinataTooManyRequestsError(raised_error)
    elif 500 <= raised_error.response.status_code < 600:
        raise PinataInternalServiceError(raised_error)
    else:
        raise PinataHTTPError(raised_error)
