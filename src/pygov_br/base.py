from urllib.parse import urljoin
from pygov_br.exceptions import ClientError, ClientServerError
import logging
import requests

log = logging.getLogger('pygov_br.client')


class Client(object):
    """Base class to interact with API"""

    def __init__(self, host, timeout=None):
        self.host = host
        self.timeout = timeout

    def _get(self, path, **kwargs):
        return self._request('GET', path, kwargs)

    def _put(self, path, **kwargs):
        return self._request('PUT', path, kwargs)

    def _post(self, path, **kwargs):
        return self._request('POST', path, kwargs)

    def _delete(self, path, **kwargs):
        return self._request('DELETE', path, kwargs)

    def _request(self, verb, path, params):
        url = urljoin(self.host, path)

        response = requests.request(verb, url, params=params,
                                    timeout=self.timeout)
        log.debug('Response [{}]: {}'.format(response.status_code,
                                             repr(response.text)))

        if not response.ok:
            msg = "[{}]: {}".format(response.status_code, response.reason)
            if 400 <= response.status_code < 500:
                raise ClientError(msg, response=response)
            else:
                raise ClientServerError(msg, response=response)

        return response.text
