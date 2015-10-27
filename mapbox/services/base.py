import os
import requests

class Service:
    """Base service class"""

    def get_session(self, token=None, env=None):
        access_token = (
            token or
            (env or os.environ).get('MapboxAccessToken') or
            (env or os.environ).get('MAPBOX_ACCESS_TOKEN'))
        session = requests.Session()
        session.params.update(access_token=access_token)
        return session

    def handle_http_error(self, response, custom_messages=None,
                          raise_for_status=False):
        if not custom_messages:
            custom_messages = {}
        if response.status_code in custom_messages.keys():
            raise requests.exceptions.HTTPError(
                custom_messages[response.status_code])
        if raise_for_status:
            response.raise_for_status()
