"""Base Service class"""

import base64
import json
import os

import requests

from .. import __version__
from mapbox import errors


class Service:
    """Service mixin class

    Requires that sub-classes have a "session" property with value of
    `requests.Session()`.
    """

    def get_session(self, token=None, env=None):
        access_token = (
            token or
            (env or os.environ).get('MapboxAccessToken') or
            (env or os.environ).get('MAPBOX_ACCESS_TOKEN'))
        session = requests.Session()
        session.params.update(access_token=access_token)
        session.headers.update(
            {'User-Agent': ' '.join(
                [self.product_token, requests.utils.default_user_agent()])})
        return session

    @property
    def product_token(self):
        """A product token for use in User-Agent headers."""
        return 'mapbox-sdk-py/{0}'.format(__version__)

    @property
    def username(self):
        """Get username from access token
        Token contains base64 encoded json object with username"""
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
