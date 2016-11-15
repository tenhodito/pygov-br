# -*- coding: utf-8 -*-
from requests.exceptions import HTTPError


class ClientError(HTTPError):
    """ A generic error while attempting to communicate with the server """


class ClientServerError(ClientError):
    """ The server encountered an error while processing the request """


class MissingParameterError(Exception):
    """ Some parameter is missing """
