from requests.exceptions import HTTPError


class ClientError(HTTPError):
    """ A generic error while attempting to communicate with Discourse """


class ClientServerError(ClientError):
    """ The server encountered an error while processing the request """
