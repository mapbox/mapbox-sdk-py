"""Base Service class"""

import base64
import json
import os

from cachecontrol import CacheControl
import requests

from .. import __version__
from mapbox import errors


def Session(access_token=None, env=os.environ):
    """Returns an HTTP session.

    :param access_token: Mapbox access token string (optional).
    :param env: a dict.
    """
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
    """Service base class."""

    default_host = 'api.mapbox.com'

    def __init__(self, access_token=None, host=None, cache=None):
        """Constructs a Service object.

        :param access_token: Mapbox access token string.
        :param cache: CacheControl cache instance (Dict or FileCache).
        """
        self.session = Session(access_token)
        self.host = host or os.environ.get('MAPBOX_HOST', self.default_host)
        if cache:
            self.session = CacheControl(self.session, cache=cache)

    @property
    def username(self):
        """Get username from access token.

        Token contains base64 encoded json object with username.
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
        if not custom_messages:
            custom_messages = {}
        if response.status_code in custom_messages.keys():
            raise errors.HTTPError(custom_messages[response.status_code])
        if raise_for_status:
            response.raise_for_status()
