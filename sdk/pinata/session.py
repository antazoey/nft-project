from urllib.parse import urljoin, urlparse

from requests import HTTPError
from requests.sessions import HTTPAdapter, Request, Session

from pinata.auth import PinataAuth
from pinata.exceptions import MissingResponseError, raise_pinata_http_error
from pinata.logger import logger
from pinata.response import PinataResponse
from pinata.utils import format_dict


class PinataAPISession:
    def __init__(self, url: str, auth: PinataAuth, session: Session):
        self._url = url
        self._auth = auth
        self._session = session
        self._headers = self._session.headers.copy()

    @classmethod
    def from_api_key(
        cls,
        api_key: str,
        api_secret: str,
        host_address: str = "https://api.pinata.cloud/",
    ) -> "PinataAPISession":
        adapter = HTTPAdapter(pool_connections=200, pool_maxsize=4, pool_block=True)
        session = Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers = {
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        auth = PinataAuth(api_key, api_secret)
        return PinataAPISession(host_address, auth, session)

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def options(self, url, **kwargs):
        return self.request("OPTIONS", url, **kwargs)

    def head(self, url, **kwargs):
        return self.request("HEAD", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request("POST", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, json=None, **kwargs):
        return self.request("PUT", url, data=data, json=json, **kwargs)

    def patch(self, url, data=None, json=None, **kwargs):
        return self.request("PATCH", url, data=data, json=json, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        json=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        hooks=None,
        stream=False,
        timeout=60,
        cert=None,
        proxies=None,
    ):
        request = self._prepare_request(
            method,
            url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            hooks=hooks,
        )
        response = self._session.send(
            request,
            stream=stream,
            timeout=timeout,
            verify=True,
            cert=cert,
            proxies=proxies,
        )

        if response is not None:
            logger.debug(f"Response status: {response.status_code}")
            if not stream:
                # setting this manually speeds up read times
                response.encoding = "utf-8"
                logger.debug(f"Response data: {response.text}")
            else:
                logger.debug("Response data: <streamed>")

            if 200 <= response.status_code <= 399:
                return PinataResponse(response)

        else:
            logger.debug("ERROR: Could not retrieve response.")

        # If we get here, an error has occurred.
        _handle_error(method, url, response)

    def _prepare_request(
        self,
        method,
        url,
        params=None,
        data=None,
        json=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        hooks=None,
    ):
        url = urljoin(self._url, url)
        self._session.verify = True

        headers = headers or {}
        headers.update(self._headers)
        if data and "Content-Type" not in headers:
            headers.update({"Content-Type": "application/json"})
        if "Accept" not in headers:
            headers.update({"Accept": "application/json"})

        headers = _create_user_headers(headers)

        _print_request(method, url, params=params, data=data, json=json)

        if isinstance(data, str):
            data = data.encode("utf-8")

        request = Request(
            method=method,
            url=url,
            headers=headers,
            files=files,
            data=data,
            json=json,
            params=params,
            auth=auth or self._auth,
            cookies=cookies,
            hooks=hooks,
        )

        return self._session.prepare_request(request)

    def _init_host_info(self, host):
        if not host.startswith("http://") and not host.startswith("https://"):
            host = f"https://{host}"

        parsed_host = urlparse(host)
        self._headers["Host"] = parsed_host.netloc
        self._host_address = host


def _create_user_headers(headers):
    user_headers = {"User-Agent": "py-pinata"}
    if headers:
        user_headers.update(headers)

    return user_headers


def _handle_error(method, url, response):
    if response is None:
        raise MissingResponseError(method, url)

    try:
        response.raise_for_status()
    except HTTPError as err:
        raise_pinata_http_error(err)


def _print_request(method, url, params=None, data=None, json=None):
    logger.debug(f"{method.ljust(8)}{url}")
    if params:
        logger.debug(format_dict(params, "  params"))
    if json:
        logger.debug(format_dict(json, "  json"))
    if data:
        logger.debug(data, "  data")
