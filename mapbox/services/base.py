"""Base Service class"""

import base64
import json
import os

from cachecontrol import CacheControl
import requests

from .. import __version__
from mapbox import errors


def Session(access_token=None, env=None):
    """Create an HTTP session.

    Parameters
    ----------
    access_token : str
        Mapbox access token string (optional).
    env : dict, optional
        A dict that subsitutes for os.environ.

    Returns
    -------
    requests.Session
    """
    if env is None:
        env = os.environ.copy()
    access_token = (
        access_token or
        env.get('MapboxAccessToken') or
        env.get('MAPBOX_ACCESS_TOKEN'))
    session = requests.Session()
    session.params.update(access_token=access_token)
    session.headers.update({
        'User-Agent': 'mapbox-sdk-py/{0} {1}'.format(
            __version__, requests.utils.default_user_agent())})
    return session


class Service(object):
    """Service base class

    Attributes
    ----------
    default_host : str
        Default service hostname: api.mapbox.com.
    api_name : str
        Mapbox API name.
    api_version : str
        API version string such as "v1" or "v5".
    baseuri
    username

    Methods
    -------
    handle_http_errors(response, custom_messages=None, raise_for_status=False)
        Converts service errors to Python exceptions.
    """

    default_host = 'api.mapbox.com'
    api_name = 'hors service'
    api_version = 'v0'

    def __init__(self, access_token=None, host=None, cache=None):
        """Constructs a Service object

        This method should be overridden by subclasses.

        Parameters
        ----------
        access_token : str
            Mapbox access token string.
        host : str, optional
            Mapbox API host (advanced usage only).
        cache : CacheControl cache instance (Dict or FileCache), optional
            Optional caching, not generally needed.

        Returns
        -------
        Service
        """
        self.session = Session(access_token)
        self.host = host or os.environ.get('MAPBOX_HOST', self.default_host)
        if cache:
            self.session = CacheControl(self.session, cache=cache)

    @property
    def baseuri(self):
        """The service's base URI

        Returns
        -------
        str
        """
        return 'https://{0}/{1}/{2}'.format(
            self.host, self.api_name, self.api_version)

    @property
    def username(self):
        """The username in the service's access token

        Returns
        -------
        str
        """
        token = self.session.params.get('access_token')
        if not token:
            raise errors.TokenError(
                "session does not have a valid access_token param")
        data = token.split('.')[1]
        # replace url chars and add padding
        # (https://gist.github.com/perrygeo/ee7c65bb1541ff6ac770)
        data = data.replace('-', '+').replace('_', '/') + "==="
        try:
            return json.loads(base64.b64decode(data).decode('utf-8'))['u']
        except (ValueError, KeyError):
            raise errors.TokenError(
                "access_token does not contain username")

    def handle_http_error(self, response, custom_messages=None,
                          raise_for_status=False):
        """Converts service errors to Python exceptions

        Parameters
        ----------
        response : requests.Response
            A service response.
        custom_messages : dict, optional
            A mapping of custom exception messages to HTTP status codes.
        raise_for_status : bool, optional
            If True, the requests library provides Python exceptions.

        Returns
        -------
        None
        """
        if not custom_messages:
            custom_messages = {}
        if response.status_code in custom_messages.keys():
            raise errors.HTTPError(custom_messages[response.status_code])
        if raise_for_status:
            response.raise_for_status()
