"""Base Service class"""

import os

import requests

from .. import __version__


class Service:
    """Base service class"""

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

    def handle_http_error(self, response, custom_messages=None,
                          raise_for_status=False):
        if not custom_messages:
            custom_messages = {}
        if response.status_code in custom_messages.keys():
            raise requests.exceptions.HTTPError(
                custom_messages[response.status_code])
        if raise_for_status:
            response.raise_for_status()
