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
    access_token: string
        Mapbox access token string (optional).
    env: dict or None

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
    """Service base class."""

    default_host = 'api.mapbox.com'
    api_name = 'hors service'
    api_version = 'v0'

    def __init__(self, access_token=None, host=None, cache=None):
        """Constructs a Service object.

        :param access_token: Mapbox access token string.
        :param cache: CacheControl cache instance (Dict or FileCache).
        :param host: Mapbox API host (advanced usage only).
        """
        self.session = Session(access_token)
        self.host = host or os.environ.get('MAPBOX_HOST', self.default_host)
        if cache:
            self.session = CacheControl(self.session, cache=cache)

    @property
    def baseuri(self):
        return 'https://{0}/{1}/{2}'.format(
            self.host, self.api_name, self.api_version)

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

    def handle_http_error(self, response, custom_messages=None):        
        if custom_messages\
            and isinstance(custom_messages, dict)\
                and response.status_code in custom_messages:
                    raise errors.HTTPError(custom_messages[response.status_code])
      
        else:  
            if 400 <= response.status_code < 500:
                response_body = response.json()
                
                status_message = response_body["code"]
        
                if status_message == "InvalidInput":
                    status_message = status_message + ":" + response_body["message"]
            
                raise errors.HTTPError(status_message)
        
            elif response.status_code >= 500:
                response.raise_for_status()
